
# Overview

KOTASTU is an innovative device designed to assist individuals with hand disabilities in controlling home appliances and computers using their feet. The system includes a foot-controlled mouse and a chair with advanced features such as voice control and facial recognition.

## Source Code Description

### Part 1: App Voice Recording

This application captures user voice input and sends commands to control devices or input text into a computer via the internet (Blynk server). The app is written in Python and developed using Visual Studio Code. To export the application to an executable file (.exe), use the following command in the terminal:

```bash
pyinstaller --onefile --noconsole --icon=[file name icon] [file name program].py
```

The resulting .exe file is then compressed into a .zip file using RAR and packaged into an installer file using NSIS.

### Part 2: Web Control Device

This web application allows users to control devices, schedule automatic on/off times, and make calls to optional phone numbers. Data is sent to the Blynk server. The web interface is developed using HTML, CSS, and JavaScript in Visual Studio Code. It can be run locally or hosted publicly on GitHub.

## Ownership

This source code is owned and authored by SevKan (Khuu Trieu Minh Khang).
