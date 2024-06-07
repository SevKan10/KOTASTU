#include "esp_camera.h"
#include <WiFi.h>
#include "fb_gfx.h"
#include "fd_forward.h"
#include "fr_forward.h"
#include "esp_http_server.h"

// WiFi credentials
const char* ssid = "Khang nè";
const char* password = "12345678@";

// Relay pin
#define RELAY_PIN 2

// Camera model
#define CAMERA_MODEL_AI_THINKER

#include "camera_pins.h"

// Face ID storage
typedef struct {
    dl_matrix3d_t *features;
    int id;
} face_id_t;

#define MAX_FACE_ID_SAVE 10
face_id_t known_faces[MAX_FACE_ID_SAVE];
int face_id_count = 0;
int next_id = 1;

// Forward declarations
void startCameraServer();
void enroll_face(dl_matrix3du_t *aligned_face);
bool recognize_face(dl_matrix3du_t *aligned_face);
dl_matrix3d_t* get_face_features(dl_matrix3du_t *aligned_face);
float calculate_similarity(dl_matrix3d_t *f1, dl_matrix3d_t *f2);

// Setup function
void setup() {
    Serial.begin(115200);
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW);

    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sccb_sda = SIOD_GPIO_NUM;
    config.pin_sccb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.frame_size = FRAMESIZE_UXGA;
    config.pixel_format = PIXFORMAT_JPEG; // for streaming
    config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    config.jpeg_quality = 12;
    config.fb_count = 1;

    if (psramFound()) {
        config.jpeg_quality = 10;
        config.fb_count = 2;
        config.grab_mode = CAMERA_GRAB_LATEST;
    } else {
        config.frame_size = FRAMESIZE_SVGA;
        config.fb_location = CAMERA_FB_IN_DRAM;
    }

    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("Camera init failed with error 0x%x", err);
        return;
    }

    sensor_t *s = esp_camera_sensor_get();
    if (s->id.PID == OV3660_PID) {
        s->set_vflip(s, 1); 
        s->set_brightness(s, 1);
        s->set_saturation(s, -2);
    }
    s->set_framesize(s, FRAMESIZE_QVGA);

    WiFi.begin(ssid, password);
    WiFi.setSleep(false);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");

    startCameraServer();

    Serial.print("Camera Ready! Use 'http://");
    Serial.print(WiFi.localIP());
    Serial.println("' to connect");
}

// Loop function
void loop() {
    delay(10000);
}

// Enroll face function
void enroll_face(dl_matrix3du_t *aligned_face) {
    if (face_id_count >= MAX_FACE_ID_SAVE) {
        Serial.println("Face ID storage is full");
        return;
    }

    dl_matrix3d_t *features = get_face_features(aligned_face);
    known_faces[face_id_count].features = features;
    known_faces[face_id_count].id = next_id++;
    face_id_count++;
    Serial.println("Face enrolled successfully");
}

// Recognize face function
bool recognize_face(dl_matrix3du_t *aligned_face) {
    if (face_id_count == 0) return false;

    dl_matrix3d_t *features = get_face_features(aligned_face);
    float min_distance = 999.0;
    int matched_id = -1;

    for (int i = 0; i < face_id_count; i++) {
        float distance = calculate_similarity(features, known_faces[i].features);
        if (distance < min_distance) {
            min_distance = distance;
            matched_id = known_faces[i].id;
        }
    }

    dl_matrix3d_free(features);
    return (matched_id != -1 && min_distance < 0.6); // Threshold tùy chỉnh
}

// Get face features function
dl_matrix3d_t* get_face_features(dl_matrix3du_t *aligned_face) {
    return fr_forward(aligned_face);
}

// Calculate similarity function
float calculate_similarity(dl_matrix3d_t *f1, dl_matrix3d_t *f2) {
    float distance = 0.0;
    for (int i = 0; i < f1->n; i++) {
        float diff = f1->item[i] - f2->item[i];
        distance += diff * diff;
    }
    return sqrt(distance);
}

// Stream handler function
esp_err_t stream_handler(httpd_req_t *req) {
    camera_fb_t * fb = NULL;
    esp_err_t res = ESP_OK;
    size_t _jpg_buf_len = 0;
    uint8_t * _jpg_buf = NULL;
    char * part_buf[64];
    static int64_t last_frame = 0;
    if (!last_frame) {
        last_frame = esp_timer_get_time();
    }

    res = httpd_resp_set_type(req, "multipart/x-mixed-replace;boundary=frame");
    if (res != ESP_OK) {
        return res;
    }

    while (true) {
        fb = esp_camera_fb_get();
        if (!fb) {
            Serial.println("Camera capture failed");
            res = ESP_FAIL;
        } else {
            if (fb->format != PIXFORMAT_JPEG) {
                bool converted = frame2jpg(fb, 80, &_jpg_buf, &_jpg_buf_len);
                if (!converted) {
                    Serial.println("JPEG compression failed");
                    esp_camera_fb_return(fb);
                    res = ESP_FAIL;
                }
            } else {
                _jpg_buf_len = fb->len;
                _jpg_buf = fb->buf;
            }
        }
        if (res == ESP_OK) {
            size_t hlen = snprintf((char *)part_buf, 64, "Content-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n", _jpg_buf_len);
            res = httpd_resp_send_chunk(req, (const char *)part_buf, hlen);
        }
        if (res == ESP_OK) {
            res = httpd_resp_send_chunk(req, (const char *)_jpg_buf, _jpg_buf_len);
        }
        if (res == ESP_OK) {
            res = httpd_resp_send_chunk(req, "\r\n--frame\r\n", 12);
        }
        if (fb->format != PIXFORMAT_JPEG) {
            free(_jpg_buf);
        }
        esp_camera_fb_return(fb);
        if (res != ESP_OK) {
            break;
        }

        // Thực hiện nhận diện khuôn mặt
        dl_matrix3du_t *aligned_face = fb->buf;
        bool recognized = recognize_face(aligned_face);
        if (recognized) {
            digitalWrite(RELAY_PIN, HIGH);
        } else {
            digitalWrite(RELAY_PIN, LOW);
        }
    }
    last_frame = esp_timer_get_time();
    return res;
}

// Start camera server function
void startCameraServer() {
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();

    httpd_uri_t stream_uri = {
        .uri       = "/",
        .method    = HTTP_GET,
        .handler   = stream_handler,
        .user_ctx  = NULL
    };

    if (httpd_start(&config, &config) == ESP_OK) {
        httpd_register_uri_handler(config, &stream_uri);
    }
}
