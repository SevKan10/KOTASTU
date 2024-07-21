# Khai báo thư viện
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyperclip
import pyautogui
import pygame.mixer
import requests
import keyboard
import threading

#----------------------------------------------------------------------------------------------------------------------------------

# Khởi tạo các đối tượng chỉ khi cần thiết
recognizer = None
mic = None

def initialize_recognizer():
    global recognizer, mic
    if not recognizer or not mic:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

#----------------------------------------------------------------------------------------------------------------------------------

# Hàm thực hiện copy paste
def pasteString(message):
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    print("Đã dán tin nhắn: ", message)

#----------------------------------------------------------------------------------------------------------------------------------

# Hàm in dấu câu
def printSign(signDef):
    if signDef == " ":
        pyautogui.press('space')
        pygame.mixer.music.load("Ok_1.wav")
        pygame.mixer.music.play()
    else:
        pasteString(signDef)
        pygame.mixer.music.load("Ok_1.wav")
        pygame.mixer.music.play()
    status_label.config(text="Văn bản của bạn: " + signDef)

#----------------------------------------------------------------------------------------------------------------------------------

# Hàm xử lý click đúp vào danh bạ
def onDoubleClick(event):
    selected = phone_listbox.curselection()
    if selected:
        entry = phone_listbox.get(selected[0])
        name, phone_number = entry.split(":")
        sendPhoneNumber(phone_number.strip())

#----------------------------------------------------------------------------------------------------------------------------------

# Hàm gửi số điện thoại lên Blynk
def sendPhoneNumber(phone_number):
    def send_request(phone_number):
        print(phone_number)
        url = f"https://sgp1.blynk.cloud/external/api/update?token=s4IEZXPS6DFlYAACZC_6z-rNmdU1erLH&v2={phone_number}"
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"Số điện thoại {phone_number} đã được gửi thành công.")
            status_label.config(text=f"Số điện thoại {phone_number} đã được gọi thành công.")
            pygame.mixer.music.load("call.wav")
            pygame.mixer.music.play()
        else:
            print("Có lỗi xảy ra:", response.status_code, response.text)
            status_label.config(text=f"Có lỗi xảy ra khi gửi số điện thoại {phone_number}: {response.status_code} {response.text}")
        phone_number = ""
    
    threading.Thread(target=send_request, args=(phone_number,)).start()

#----------------------------------------------------------------------------------------------------------------------------------

# Hàm gửi dữ liệu lên Blynk
def sendData(pin, value, i):
    def send_request(pin, value, i):
        url = f"https://sgp1.blynk.cloud/external/api/update?token=s4IEZXPS6DFlYAACZC_6z-rNmdU1erLH&{pin}={value}"
        response = requests.get(url)
        
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
    
    threading.Thread(target=send_request, args=(pin, value, i)).start()

#----------------------------------------------------------------------------------------------------------------------------------

# Hàm nghe và điền
def listenAndEnter():
    initialize_recognizer()
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
            "dấu cộng"          : ("+") ,
            "dấu trừ"           : ("-") ,
            "dấu sao"           : ("*") ,
            "dấu nhân"          : ("x") ,
            "dấu chia"          : (":") ,
            "dấu mũ"            : ("^") ,
            "dấu gạch chéo"     : ("/") , 
            "dấu gạch ngang"    : ("-") ,
            "dấu phần trăm"     : ("%") ,
            "dấu thăng"         : ("#") ,
            "dấu a vòng"        : ("@") ,
            "dấu a dòng"        : ("@") ,
            "dấu a còng"        : ("@") ,
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
    initialize_recognizer()
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

# Hàm lưu tên và số điện thoại vào tệp
def savePhoneNumber():
    def on_submit():
        name = name_entry.get()
        phone_number = phone_entry.get()
        if name and phone_number:
            try:
                with open("Contact.txt", "a", encoding="utf-8") as file:
                    file.write(f"{name}:{phone_number}\n")
                loadPhoneNumbers()
                status_label.config(text="Tên và số điện thoại đã được lưu.")
                top.destroy()
            except Exception as e:
                print(f"Lỗi khi lưu dữ liệu: {e}")
                status_label.config(text=f"Có lỗi xảy ra khi lưu dữ liệu: {e}")
        else:
            messagebox.showwarning("Cảnh báo", "Tên và số điện thoại không thể để trống.", parent=top)

    top = tk.Toplevel(root)
    top.title("Nhập thông tin liên lạc")
    top.geometry("400x300")
    top.configure(bg='#97CADB')

    tk.Label(top, text="Nhập tên:", bg='#97CADB', font=('Helvetica', 12, 'bold')).pack(pady=10)
    name_entry = tk.Entry(top, width=40)
    name_entry.pack(pady=5)

    tk.Label(top, text="Nhập số điện thoại:", bg='#97CADB', font=('Helvetica', 12, 'bold')).pack(pady=10)
    phone_entry = tk.Entry(top, width=40)
    phone_entry.pack(pady=5)

    tk.Button(top, text="Lưu", command=on_submit, bg='#018ABE', fg='#D6E8EE', font=('Helvetica', 12, 'bold')).pack(pady=10)

#----------------------------------------------------------------------------------------------------------------------------------

# Hàm tải danh bạ từ tệp
def loadPhoneNumbers():
    phone_listbox.delete(0, tk.END)
    try:
        with open("Contact.txt", "r", encoding="utf-8") as file:
            contacts = file.readlines()
            for contact in contacts:
                phone_listbox.insert(tk.END, contact.strip())
    except FileNotFoundError:
        open("Contact.txt", "w", encoding="utf-8").close()
    except Exception as e:
        print(f"Error loading contacts: {e}")
        status_label.config(text=f"Error loading contacts: {e}")

#----------------------------------------------------------------------------------------------------------------------------------

# Hàm gọi số điện thoại
def callPhoneNumber():
    top = tk.Toplevel(root)
    top.title("Nhập số điện thoại")
    top.geometry("400x200")
    top.configure(bg='#97CADB')

    tk.Label(top, text="Vui lòng nhập số điện thoại:", bg='#97CADB', font=('Helvetica', 12, 'bold')).pack(pady=10)
    phone_entry = tk.Entry(top, width=40)
    phone_entry.pack(pady=10)

    def on_submit():
        phone_number = phone_entry.get()
        if phone_number:
            sendPhoneNumber(phone_number)
            top.destroy()
        else:
            messagebox.showwarning("Cảnh báo", "Số điện thoại không thể để trống.", parent=top)

    tk.Button(top, text="Gọi", command=on_submit, bg='#018ABE', fg='#D6E8EE', font=('Helvetica', 12, 'bold')).pack(pady=10)

#----------------------------------------------------------------------------------------------------------------------------------

# Khởi tạo giao diện đồ họa
root = tk.Tk()
root.geometry("500x400")
root.title("Voice Typing and Control Device")
root.configure(bg='#97CADB')

status_label = tk.Label(root, text="Nhấn nút để soạn thảo và điều khiển", bg='#97CADB', font=('Helvetica', 12))
status_label.pack(pady=10)

tk.Button(root, text="Lưu tên và số điện thoại", command=savePhoneNumber, bg='#018ABE', fg='#D6E8EE', font=('Helvetica', 12, 'bold')).pack(pady=10)
tk.Button(root, text="Gọi", command=callPhoneNumber, bg='#018ABE', fg='#D6E8EE', font=('Helvetica', 12, 'bold')).pack(pady=10)

phone_listbox = tk.Listbox(root, width=60, height=10, font=('Helvetica', 12))
phone_listbox.pack(pady=10)
phone_listbox.bind("<Double-1>", onDoubleClick)

loadPhoneNumbers()

#----------------------------------------------------------------------------------------------------------------------------------

# Khởi tạo mic và phát âm
pygame.mixer.init()

# Tạo phím tắt
keyboard.add_hotkey('windows+ctrl+alt+shift+m', listenAndEnter) 
keyboard.add_hotkey('windows+ctrl+alt+shift+h', listenAndControl)

root.mainloop()

#----------------------------------------------------------------------------------------------------------------------------------
