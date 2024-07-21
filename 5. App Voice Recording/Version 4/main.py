# Khai báo thư viện
import tkinter as tk
import speech_recognition as sr
import keyboard
import pyperclip
import pyautogui
import pygame.mixer
import requests
#----------------------------------------------------------------------------------------------------------------------------------

# Hàm thực hiện copy paste
def pasteString(message):
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    print("Đã dán tin nhắn: ", message)
#----------------------------------------------------------------------------------------------------------------------------------

# Hàm gửi dữ liệu lên Blynk
def sendData(pin, value, i): 
    url = f"https://sgp1.blynk.cloud/external/api/update?token=s4IEZXPS6DFlYAACZC_6z-rNmdU1erLH&{pin}={value}"
    response = requests.get(url)
    
    # Kiểm tra tín hiệu request
    if response.status_code == 200:
        print(f"Dữ liệu đã được gửi thành công. Đèn {i} đã được {value}")
        status_label.config(text=f"Đèn {i} đã được {value}")
        status = value[:2]

        if "On" in status:
            pygame.mixer.music.load("on.wav")
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.load("off.wav")
            pygame.mixer.music.play()

    else:
        print("Có lỗi xảy ra:", response.status_code, response.text)
        status_label.config(text=f"Có lỗi xảy ra khi thay đổi đèn {i}: {response.status_code} {response.text}")
#----------------------------------------------------------------------------------------------------------------------------------

# Hàm in dấu câu
def printSign(signDef):
    pasteString(signDef)
    status_label.config(text="Văn bản của bạn: " + signDef)
#----------------------------------------------------------------------------------------------------------------------------------

# Hàm nghe và điền
def listenAndEnter():
    status_label.config(text="Vui lòng nhập văn bản...")
    pygame.mixer.music.load("Input.wav")
    pygame.mixer.music.play()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

    try:
        status_label.config(text="Đang nhận dạng giọng nói...")
        message = recognizer.recognize_google(audio_data, language="vi")

        signs = {
            "dấu phẩy"          : (",") ,
            "dấu chấm"          : (".") , 
            "dấu chấm than"     : ("!") ,
            "dấu chấm hỏi"      : ("?") ,
            "dấu hai chấm"      : (":") ,
            "dấu chấm phẩy"     : (";") ,
            "dấu gạch ngang"    : ("-") ,
            "dấu cộng"          : ("+") ,
            "dấu trừ"           : ("-") ,
            "dấu sao"           : ("*") ,
            "dấu nhân"          : ("x") ,
            "dấu chia"          : (":") ,
            "dấu mũ"            : ("^") ,
            "dấu gạch chéo"     : ("/") ,
            "dấu phần trăm"     : ("%") ,
            "dấu thăng"         : ("#") ,
            "dấu a vòng"        : ("@") ,
            "dấu a dòng"        : ("@") ,
            "dấu ngoặc đơn mở"  : ("(") ,
            "dấu ngoặc đơn đóng": (")") ,
            "dấu ngoặc kép mở"  : ("\""),
            "dấu ngoặc kép đóng": ("\""),
            "dấu cách"          : (" ") ,
        }

        sign = signs.get(message.lower())

        if sign:
            printSign(*sign)   
        else:
            status_label.config(text="Văn bản của bạn: " + message)
            pasteString(message)
            pygame.mixer.music.load("Ok_1.wav")
            pygame.mixer.music.play()
    except sr.UnknownValueError:
        status_label.config(text="Không thể nhận dạng giọng nói")
        pygame.mixer.music.load("Error.wav")
        pygame.mixer.music.play()
    except sr.RequestError as e:
        status_label.config(text="Lỗi kết nối; {0}".format(e))
        pygame.mixer.music.load("noise.wav")
        pygame.mixer.music.play()
#----------------------------------------------------------------------------------------------------------------------------------

# Hàm nghe và điều khiển thiết bị
def listenAndControl():
    status_label.config(text="Vui lòng nhập lệnh điều khiển...")
    pygame.mixer.music.load("Input.wav")
    pygame.mixer.music.play()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

    try:
        status_label.config(text="Đang nhận dạng giọng nói...")
        text = recognizer.recognize_google(audio_data, language="vi")
        status_label.config(text="Bạn: " + text)

        commands = {
            "mở thiết bị 1"   : ("v0", "On1", 1),
            "tắt thiết bị 1"  : ("v0", "Off1",1),
            "mở thiết bị 2"   : ("v0", "On2", 2),
            "mở thiết bị hay" : ("v0", "On2", 2),
            "tắt thiết bị 2"  : ("v0", "Off2",2),
            "tắt thiết bị hay": ("v0", "Off2",2),
            "mở thiết bị 3"   : ("v0", "On3", 3),
            "tắt thiết bị 3"  : ("v0", "Off3",3),
            "mở thiết bị 4"   : ("v0", "On4", 4),
            "tắt thiết bị 4"  : ("v0", "Off4",4),
            "mở thiết bị 5"   : ("v0", "On5", 5),
            "tắt thiết bị 5"  : ("v0", "Off5",5),
            "mở thiết bị 6"   : ("v0", "On6", 6),
            "tắt thiết bị 6"  : ("v0", "Off6",6),
            "mở thiết bị 7"   : ("v0", "On7", 7),
            "tắt thiết bị 7"  : ("v0", "Off7",7),
            "mở thiết bị 8"   : ("v0", "On8", 8),
            "tắt thiết bị 8"  : ("v0", "Off8",8),
        }
        
        command = commands.get(text.lower())

        if command:
            sendData(*command)
        else:
            status_label.config(text="Không hiểu lệnh điều khiển")
            pygame.mixer.music.load("error control.wav")
            pygame.mixer.music.play()
    except sr.UnknownValueError:
        status_label.config(text="Không thể nhận dạng giọng nói")
        pygame.mixer.music.load("Error.wav")
        pygame.mixer.music.play()
    except sr.RequestError as e:
        status_label.config(text=f"Lỗi kết nối; {e}")
        pygame.mixer.music.load("noise.wav")
        pygame.mixer.music.play()
#----------------------------------------------------------------------------------------------------------------------------------

# Khởi tạo giao diện đồ họa
root = tk.Tk()
root.geometry("400x200")
root.title("Voice Typing and Control Device")
status_label = tk.Label(root, text="Nhấn nút để soạn thảo và điều khiển")
status_label.pack(pady=10)
#----------------------------------------------------------------------------------------------------------------------------------

# Khởi tạo mic và phát âm
recognizer = sr.Recognizer()
mic = sr.Microphone()
pygame.mixer.init()
#----------------------------------------------------------------------------------------------------------------------------------

# Tạo phím tắt
keyboard.add_hotkey('windows+ctrl+alt+shift+m', listenAndEnter) 
keyboard.add_hotkey('windows+ctrl+alt+shift+h', listenAndControl)

root.mainloop()
#----------------------------------------------------------------------------------------------------------------------------------