import sys
import os
from os import listdir
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import socket
import threading
from threading import Thread
from screeninfo import get_monitors
import cv2, pickle, struct, imutils
from PIL import Image
import turtle as t
import io
import numpy as np
import pyttsx3
import time
import rsa
import numpy
assert numpy

for m in get_monitors():
    strt = str(m)
MONITOR_WIDTH = int(int((strt.split(",")[2]).replace("width=","")) * 0.5)
MONITOR_HEIGHT = int(int((strt.split(",")[3]).replace("height=","")) * 0.85)

engine = pyttsx3.init()
engine.setProperty('rate', 180)
BUTTON_WIDTH = int(MONITOR_WIDTH*0.175)
BUTTON_HEIGHT = int(MONITOR_HEIGHT*0.058)
INI_WIDTH = int(MONITOR_WIDTH*0.35)
INI_HEIGHT = int(MONITOR_HEIGHT*0.058)
START_WIDTH = int(MONITOR_WIDTH*0.2035)
MESSAGE_START = int(MONITOR_HEIGHT*0.9245)
START_GAP = int(MONITOR_HEIGHT*0.015)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
TCP_IP = s.getsockname()[0]
s.close()

# TCP_IP = socket.gethostbyname(socket.gethostname()) 

TCP_PORT = 8080 
BUFFER_SIZE = 1048576
camera = True
open_ = False
voice_ = False
testing_ = False
global options
options = []
options.append(camera)
options.append(open_)
options.append(voice_)
options.append(testing_)
global Files 
Files = []
global current_path
current_path = os.getcwd().replace("\\","/")
global folder_dir
folder_dir = f"{current_path}/iconsAndImages"
for images in os.listdir(folder_dir):
    if (images.endswith(".png")):
        Files.append(images)

class Camera_Window(QDialog):           
    change_pixmap_signal = pyqtSignal(np.ndarray)               
    def __init__(self):
        super().__init__()
        self.move(10,10)
        self.closeEvent
        self.setWindowTitle("Video")
        self.setWindowIcon(QIcon(f"{current_path}/camera_icon.png"))
        self.FeedLabel = QLabel(self)
        self.FeedLabel.setFixedSize(int(MONITOR_WIDTH*0.44), int(MONITOR_HEIGHT*0.345))
        self.FeedLabel.setStyleSheet("border: 2px solid white")
        self.change_pixmap_signal.connect(self.update_image)
        
        self.show() 

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'YOU CANNOT CLOSE THIS WINDOW',
				QMessageBox.Ok)
        event.ignore()   

    def get_vid(self, data):
        try:
            buff = np.frombuffer(data, np.uint8)
            buff = buff.reshape(1, -1)
            img = cv2.imdecode(buff, cv2.IMREAD_COLOR)
            self.change_pixmap_signal.emit(img)
        except TypeError:
            None

    def show_vid(self):
        Capture = cv2.VideoCapture(0)
        while True:
            ret, frame = Capture.read()  
            if ret:
                cv2.imshow('frame', frame)
      
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        self.close()

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.FeedLabel.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(int(MONITOR_WIDTH*0.445), int(MONITOR_HEIGHT*0.35), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
class Settings(QDialog):
    def __init__(self):
        super().__init__()
        self.background_list = ["Default", "Black", "Grey", "Green"]
        self.font_list = ["Arial", "Times", "Calibri", "David"]

        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(f'{folder_dir}/settings-dark.png'))
        self.resize(int(MONITOR_WIDTH*0.445), int(MONITOR_HEIGHT*0.35))

        self.layout = QGridLayout()

        self.background_box = QComboBox()
        self.background_box.setFixedSize(200,40)

        self.background_text = QLabel("Select your background")
        self.background_text.setFixedSize(400,40)

        self.font_box = QComboBox()
        self.font_box.setFixedSize(200,40)

        self.font_text = QLabel("Select your font")
        self.font_text.setFixedSize(400,40)

        self.camera_text = QLabel("Test camera")
        self.camera_text.setFixedSize(400,40)

        self.camera_button_ = QPushButton("Test camera")
        self.camera_button_.setFixedSize(200,40)

        self.tip_text = QLabel("Tip:")
        self.tip_text.setFixedSize(400,40)

        self.tip_label = QLabel("!HELP")
        self.tip_label.setFixedSize(200,40)

        self.layout.addWidget(self.background_text, 0, 0)
        self.layout.addWidget(self.background_box, 0, 1)
        self.layout.addWidget(self.font_text, 1, 0)
        self.layout.addWidget(self.font_box, 1, 1)
        self.layout.addWidget(self.camera_text, 2, 0)
        self.layout.addWidget(self.camera_button_, 2, 1)
        self.layout.addWidget(self.tip_text, 3, 0)
        self.layout.addWidget(self.tip_label, 3, 1)

        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        for back in self.background_list:
            self.background_box.addItem(back.title())

        for ft in self.font_list:
            self.font_box.addItem(ft.title())

        self.background_box.currentTextChanged.connect(self.background_changed)
        self.font_box.currentTextChanged.connect(self.font_changed) 
        self.camera_button_.clicked.connect(self.start_test)

    def start_test(self):
        t = threading.Thread(target=self.test)
        t.start()

    def test(self):
        self.camera_button_.setText("(Loading...)")
        window.camera_button.setDisabled(True)
        options[3] = True
        Capture = cv2.VideoCapture(0)
        self.camera_button_.setText("(Testing...)")
        while True:
            ret, frame = Capture.read()  
            if ret:
                cv2.imshow('Press ~e~ to exit', frame)
                if cv2.waitKey(1) & 0xFF == ord('e'):
                    break
        Capture.release()
        self.camera_button_.setText("Test camera")
        window.camera_button.setDisabled(False)
        options[3] = False

        cv2.destroyAllWindows()

    def background_changed(self, s):
        match s:
            case 'Default':
                for button in window.buttons:
                    button.setStyleSheet(f"""
            background-color: #7918cc;
            color: #FFFFFF;
            border: 2px solid white;
            """)
                window.setStyleSheet(f"""
            background-color: #702cab;
            color: #FFFFFF;
            font-family: Aharoni;
            font-size: 36px;
            """)
            case 'Green':
                for button in window.buttons:
                    button.setStyleSheet(f"""
            background: #71f088;
            border: 2px solid white;
            """)
                window.setStyleSheet(f"""
            background-color: #0ffa3a;
            color: #FFFFFF;
            font-family: Aharoni;
            font-size: 36px;
            background-position: center;
            """)
            case 'Black':
                for button in window.buttons:
                    button.setStyleSheet(f"""
            border: 2px solid white;
            background-color: #160224
            """)
                window.setStyleSheet(f"""
            background-color: #000000;
            color: #FFFFFF;
            font-family: Aharoni;
            font-size: 36px;
            background-position: center;
            """)
            case 'Grey':
                for button in window.buttons:
                    button.setStyleSheet(f"""
            background: #676469;
            border: 2px solid white;
            """)
                window.setStyleSheet(f"""
            background-color: #444245;
            color: #FFFFFF;
            font-family: Aharoni;
            font-size: 36px;
            background-position: center;
            """)

    def font_changed(self, s):  
        window.chat.setStyleSheet(f"""
        border: 2px solid white;
        font-family: {s}; font-size: 26px;
        background-color: #4e4f45;
        """)   

    def closeEvent(self, event):
        event.accept()
        window.setting.remove(self)
        options[1] = False
                
class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.clients = []
        self.names = []
        self.FeedLabels = []
        self.setting = []
        self.buttons = []
        self.cameras = []
        self.threads = [] 
        self.camera_test = []
        self.setFixedSize(MONITOR_WIDTH , MONITOR_HEIGHT)
        self.setWindowTitle("Server")
        self.setWindowIcon(QIcon(f'{folder_dir}/server.png'))
        self.setStyleSheet("""
        background-color: #702cab;
        color: #FFFFFF;
        font-family: Aharoni;
        font-size: 36px;
        """)
        
        self.chatTextField=QLineEdit(self)
        self.chatTextField.setFixedSize(INI_WIDTH + int(MONITOR_WIDTH*0.07),INI_HEIGHT)
        self.chatTextField.setMaxLength(117)
        self.chatTextField.setStyleSheet("""
        background-color: #4e4f45;
        """)
        self.buttons.append(self.chatTextField)

        self.btnSend = QPushButton("SEND",self)
        self.btnSend.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.btnSend.setStyleSheet("""
        border: 2px solid white;
        """)
        self.btnSend.clicked.connect(self.send)
        self.buttons.append(self.btnSend)

        self.stn_button = QPushButton("",self)
        self.stn_button.setIcon(QIcon(f'{folder_dir}/settings.png'))
        self.stn_button.setIconSize(QSize(BUTTON_HEIGHT - 20,BUTTON_HEIGHT - 20))
        self.stn_button.setFixedSize(BUTTON_HEIGHT, BUTTON_HEIGHT)
        self.stn_button.move(START_GAP,START_GAP)
        self.stn_button.setStyleSheet("""
        border: 2px solid white;
        """)
        self.stn_button.clicked.connect(self.settings)
        self.buttons.append(self.stn_button)

        self.chat = QTextEdit()
        self.chat.setFixedSize(int(MONITOR_WIDTH*0.6),1150)
        self.chat.setStyleSheet("""
        border: 2px solid white;
        font-family: Arial; font-size: 26px;
        background-color: #4e4f45;
        """)
        self.chat.setReadOnly(True)

        self.cls_button = QPushButton("Clear")
        self.cls_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.cls_button.setStyleSheet("""
        border: 2px solid white;
        """)
        self.cls_button.clicked.connect(self.clear)
        self.buttons.append(self.cls_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.exit_button.setStyleSheet("""
        border: 2px solid white;
        """)
        self.exit_button.clicked.connect(self.exit)
        self.buttons.append(self.exit_button)

        self.camera_button = QPushButton("",self)
        self.camera_button.setIcon(QIcon(f'{folder_dir}/camera_on.png'))
        self.camera_button.setIconSize(QSize(BUTTON_HEIGHT,BUTTON_HEIGHT))
        self.camera_button.setFixedSize(BUTTON_HEIGHT, BUTTON_HEIGHT)
        self.camera_button.move(START_GAP,MESSAGE_START)
        self.camera_button.setStyleSheet("""
        border: 2px solid white;
        """)
        self.camera_button.clicked.connect(self.camera)
        self.buttons.append(self.camera_button)

        self.conn_button = QPushButton()
        self.conn_button.hide()
        self.conn_button.clicked.connect(self.camera_window)

        self.grid_layout = QGridLayout(self)

        self.setLayout(self.grid_layout)
        self.grid_layout.setContentsMargins(20,20,10,10) 

        self.grid_layout.addWidget(self.btnSend, 7, 1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(self.chat, 6 ,1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.addWidget(self.chatTextField, 7, 1, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.cls_button, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.grid_layout.addWidget(self.exit_button, 4, 1, alignment=Qt.AlignmentFlag.AlignRight)

        self.serverThread=ServerThread(self)

        self.serverThread.start()

        anim=threading.Thread(target=self.animation)
        
        anim.start()

    def camera(self,):
        if not options[0]:
            self.camera_button.setIcon(QIcon(f'{folder_dir}/camera_on.png'))
            self.camera_button.setIconSize(QSize(BUTTON_HEIGHT,BUTTON_HEIGHT))
            options[0] = True
        elif options[0]:
            self.camera_button.setIcon(QIcon(f'{folder_dir}/line.png'))
            self.camera_button.setIconSize(QSize(BUTTON_HEIGHT,BUTTON_HEIGHT))
            options[0] = False

    def closeEvent(self, event):
        event.accept()
        self.exit_button.click()

    def camera_window(self,):
        w = Camera_Window()
        self.FeedLabels.append(w)
        index = self.FeedLabels.index(w)
        w.setWindowTitle(f"Video for client ~{self.names[index]}~")
        
    def settings(self,):
        if options[1]: 
           pass
        elif not options[1]:
            s = Settings()   
            self.setting.append(s)
            s.show()
            options[1] = True

    def code(self, data, index, conn, name):
        try:
            if data == "exit::EXIT_CODE_": 
                self.FeedLabels.pop(index)
                self.chat.append(f"[{conn.getpeername()[0]}] Client ~{name}~ has disconnected")
                for client in self.clients:
                    if conn.getpeername()[1] == self.clients[index].getpeername()[1]:
                        self.clients[index].close()
                        self.clients.remove(client)
                        self.threads.pop(index)
                        self.names.pop(index)
                        self.FeedLabels.pop(index)
                return True  
            return False
        except:
            return False

    def illigal_messages(self, text):
        if text == "exit::EXIT_CODE_": 
            self.chat.append(f"Illigal message")
            self.chatTextField.setText("")
        elif text == "kick::KICK_CODE_": 
            self.chat.append(f"Illigal message")
            self.chatTextField.setText("")
        elif text == "ban::BAN_CODE_": 
            self.chat.append(f"Illigal message")
            self.chatTextField.setText("")
        elif text == "camera::CAMERA_CODE_": 
            self.chat.append(f"Illigal message")
            self.chatTextField.setText("")
        self.chatTextField.setText("")
        return
        
    def special_commands(self, text):
        if text.lower() == "!clients":
            self.chat.append(f"-"*80)
            self.chat.append(f"Number of clients: {len(self.clients)}")
            for client in self.clients:
                index = self.clients.index(client)
                self.chat.append(f"-"*80)
                self.chat.append(f"Name: ~{self.names[index]}~ \nConnection: {client} \nCamera: {self.cameras[index]}")
            self.chat.append(f"-"*80)

        elif text.lower()[0:6] == "!clear":
            self.chat.setText("")

        elif text.lower()[0:5] == "!kick" and text[0:6] != "!kick!":
            try:
                self.chat.append(f"-"*80)
                with open('bans.txt', 'r') as f:
                    bans = f.readlines()
                name = str(text[6:None])
                if name+'\n' in bans:
                    self.chat.append(f"Client ~{name}~ got banned from the server")
                    self.chat.append(f"-"*80)
                    window.chatTextField.clear()
                    return
                name = str(text[6:None])
                index = self.names.index(name)
                for client in self.clients:
                    if index == self.clients.index(client):
                        client.send(rsa.encrypt("kick::KICK_CODE_".encode("utf-8"), public_partner))
                        client.close()
                        self.clients.remove(client)
                        self.FeedLabels.pop(index)
                        self.threads.pop(index)
                        self.chat.append(f"Client ~{self.names[index]}~ has been kicked")
                        self.names.pop(index)
                self.chat.append(f"-"*80)
            except:
               self.chat.append(f"Client ~{text[6:None]}~ deos not exist") 
               self.chat.append(f"-"*80)

        elif text.lower()[0:6] == "!kick!":
            try:
                self.chat.append(f"-"*80)
                name = str(text[7:None])
                index = self.names.index(name)
                for client in self.clients:
                    if index == self.clients.index(client):
                        client.close()
                        self.clients.remove(client)
                        self.FeedLabels.pop(index)
                        self.threads.pop(index)
                        self.chat.append(f"Client ~{self.names[index]}~ connection got terminated")
                        self.names.pop(index)
                self.chat.append(f"-"*80)
            except:
               pass

        elif text.lower()[0:5] == "!vban":
            try:
                self.chat.append(f"-"*80)
                with open('bans.txt', 'r') as f:
                    bans = f.readlines()
                    self.chat.append(f"Users that has been banned by the server")
                    for ban in bans:
                        if ban[0:-2] != '':
                            self.chat.append(f"-"*80)
                            self.chat.append(f"Client ~{ban[0:-1]}~")
                    self.chat.append(f"-"*80)
            except:
                pass

        elif text.lower()[0:9] == "!voice on":
            options[2] = True

        elif text.lower()[0:10] == "!voice off":
            options[2] = False

        elif text.lower()[0:5] == "!send":
            try:
                self.chat.append(f"-"*80)
                name = ''
                msg = ''
                i = 6
                while True:
                    if text[i] == '-':
                        break
                    else:
                        name = name+f'{text[i]}'
                    i += 1
                msg = text[i+1:None]
                index = self.names.index(name[0:-1])
                for client in self.clients:
                    if index == self.clients.index(client):
                        client.send(rsa.encrypt(msg.encode("utf-8"), public_partner))
                        self.chat.append(f"Client ~{self.names[index]}~ recieved special message: {msg}")
                self.chat.append(f"-"*80)
            except:
               self.chat.append(f"Client ~{text[6:None]}~ deos not exist") 
               self.chat.append(f"-"*80)

        elif text.lower()[0:4] == "!ban":
            try:
                self.chat.append(f"-"*80)
                with open('bans.txt', 'r') as f:
                    bans = f.readlines()
                name = str(text[5:None])
                if name+'\n' in bans:
                    self.chat.append(f"Client ~{name}~ already banned")
                    self.chat.append(f"-"*80)
                    return
                else:
                    with open('bans.txt', 'a') as f:
                        f.write(name+'\n')
                    index = self.names.index(name)
                    for client in self.clients:
                        if index == self.clients.index(client):
                            client.send(rsa.encrypt("ban::BAN_CODE_".encode("utf-8"), public_partner))
                            client.close()
                            self.clients.remove(client)
                            self.FeedLabels.pop(index)
                            self.threads.pop(index)
                            self.chat.append(f"Client ~{self.names[index]}~ has been banned")
                            self.names.pop(index)
                    self.chat.append(f"-"*80)
            except:
                self.chat.append(f"Client ~{text[5:None]}~ deos not exist") 
                self.chat.append(f"-"*80)
                window.chatTextField.clear()

        elif text.lower()[0:5] == "!help":
            command = text[6:None]
            self.chat.append(f"-"*80)
            if command == "clients":
                self.chat.append("CLIENTS\tList the number of clients connected follow by information \t\t\tabout them.")
                self.chat.append("type !CLIENTS to view all clients.")
            elif command == "clear":
                self.chat.append("CLEAR\t\tClear the chat.")
                self.chat.append("type !CLEAR to clear the chat.")
            elif command == "kick":
                self.chat.append("KICK\t\tKick a user out of the server.")
                self.chat.append("type !KICK [username] to kick a user.")
            elif command == "ban":
                self.chat.append("BAN\t\tBan a user out of the server.")
                self.chat.append("type !BAN [username] to ban a user.")
            elif command == "vban":
                 self.chat.append("VBAN\t\tShow banned users.")
                 self.chat.append("type !VBAN to view all banned users.")
            elif command == "voice":
                self.chat.append("VOICE\t\tChange auto voice settings.")
                self.chat.append("type !VOICE [on/off] to turn on or off the autovoice")
            elif command == "send":
                self.chat.append("SEND\t\tSend a message to to a specific user.")
                self.chat.append("type !SEND [username] to send a message")
            elif command == "":
                self.chat.append(f"To specify a command, Add ![command-name] before your command")
                self.chat.append(f"For more information on a specific command, type !HELP command-name")
                self.chat.append("HELP\t\tDisplay available commands.")
                self.chat.append("CLIENTS\tList the number of clients connected follow by information \t\t\tabout them.")
                self.chat.append("CLEAR\tClear the chat.")
                self.chat.append("KICK\t\tKick a user out of the server.")
                self.chat.append("BAN\t\tBan a user out of the server.")
                self.chat.append("VBAN\t\tShow banned user.")
                self.chat.append("VOICE\t\tChange auto voice settings.")
                self.chat.append("SEND\t\tSend a message to to a specific user.")
            self.chat.append(f"-"*80)

        else:
            self.chat.append(f"-"*80)
            self.chat.append(f"'{text[1:None]}' is not recognized as an internal or external command")
            self.chat.append(f"-"*80)

        self.chatTextField.setText("")
        return

    def send(self):
        text=self.chatTextField.text()
        if text == "": 
            self.chat.append(f"Can't send empty message")
            return
        elif text[0] == '!':
            t = threading.Thread(target=self.special_commands(text))
            t.start()
            return
        elif text[-1] == '_':
            self.illigal_messages(text)
            return
        elif window.clients:
            for client in self.clients:
                client.send(rsa.encrypt(text.encode("utf-8"), public_partner))
            self.chat.append(f"[{TCP_IP}] Server message> "+text)
        else:
            self.chat.append(f"There's no one home")
        self.chatTextField.setText("")
    
    def clear(self):
        self.chat.setText("")
        self.chat.update()

    def exit(self):
        try:
            for client in self.clients:
                client.send(rsa.encrypt("exit::EXIT_CODE_".encode("utf-8"), public_partner))
            os._exit(1)
        except:
            os._exit(1)

    def animation(self):
        data = ["e","n","t","e","r"," ","y","o","u","r"," ","m","e","s","s","a","g","e"]
        while True:
            for x in range(len(data)):
                old = data[x]
                data[x] = old.upper()
                text = "".join(data)
                self.chatTextField.setPlaceholderText(text)
                data[x] = old
                time.sleep(0.2)
            text = "".join(data)
            self.chatTextField.setPlaceholderText(text)

class ServerThread(QThread):
    def __init__(self,window): 
        super().__init__() 
        self.window=window
        self.ip = ''

    def send_files(self, Files, conn):
        window.chat.append(f"Sending {len(Files)} files...")
        complete = True
        i = 0
        while complete:
            try:
                for i in range(len(Files)):
                    msg = ""
                    try:
                        im = Image.open(f'{folder_dir}'+f'/{str(Files[i])}')
                        width, height = im.size
                        im_resize = im.resize((width, height))
                        buf = io.BytesIO()
                        im_resize.save(buf, format='png')
                        byte_im = buf.getvalue()
                        conn.send(byte_im)
                        i +=1
                        window.chat.append(f"Sent {i}/{len(Files)} files")
                        msg = rsa.decrypt(self.conn.recv(BUFFER_SIZE), private_key).decode("utf-8")
                        if msg[0:5] == "Ok":
                            continue
                        elif msg[0:5] == "Retry":
                            self.send_files(Files, self.conn)
                            return
                    except:
                        continue
                msg = rsa.decrypt(self.conn.recv(BUFFER_SIZE), private_key).decode("utf-8")
                if msg[0:2] == 'Ok':
                    window.chat.append(f"All files transmitted succesfully")
                    return
                elif msg[0:5] == 'Retry':
                    self.send_files(Files, self.conn)
            except ConnectionAbortedError:
                    complete = False
            except:
                window.chat.append(f"[{self.conn.getpeername()[0]}] Client appeared to disconnect")
                return

    def run(self):
        global public_key, private_key
        global public_partner
        public_key, private_key = rsa.newkeys(1024)
        public_partner = None
        
        image = Image.open(f'{folder_dir}/pngtree.png')
        im_resize = image.resize((int(MONITOR_WIDTH*0.445), int(MONITOR_HEIGHT*0.35)))
        buf = io.BytesIO()
        im_resize.save(buf, format='PNG')
        byte_im = buf.getvalue()

        global window  
        TCPServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        TCPServer.bind((TCP_IP, TCP_PORT)) 
        while True:
            try:
                window.chat.append("Started TCP server on ["+str(TCP_IP)+"], ("+str(TCP_PORT)+")")
                break
            except NameError:
                continue

        self.Worker1 = Worker1()              #WebCam handler
        self.Worker1.start()                  #<==============
        
        TCPServer.listen(4) 
        while True:
            window.chat.append("Waiting for connections from TCP clients...") 
            global addr
            self.conn,addr = TCPServer.accept()

            self.conn.send(public_key.save_pkcs1("PEM"))
            public_partner = rsa.PublicKey.load_pkcs1(self.conn.recv(1024))

            self.conn.send(rsa.encrypt(TCP_IP.encode("utf-8"), public_partner))

            self.name = rsa.decrypt(self.conn.recv(BUFFER_SIZE), private_key).decode("utf-8")

            with open('bans.txt', 'r') as f:
                bans = f.readlines()
            resume = True
            if self.name+'\n' in bans:
                window.chat.append(f"Client ~{self.name}~ tried to connect but is banned by the server")
                self.conn.send(rsa.encrypt('Ban'.encode("utf-8"), public_partner))
                self.conn.close()
                resume = False
            else:
                self.conn.send(rsa.encrypt('Ok'.encode("utf-8"), public_partner))
            if resume:
                window.names.append(self.name)
                window.cameras.append(False)

                self.conn.send(rsa.encrypt(str(len(Files)).encode("utf-8"), public_partner))

                self.missing = rsa.decrypt(self.conn.recv(BUFFER_SIZE), private_key).decode("utf-8")

                if self.missing == 'missing': 
                    window.chat.append(f"[{self.conn.getpeername()[0]}] Client ~{self.name}~ said> {self.missing}") 
                    self.send_files(Files, self.conn)
                else:
                    window.chat.append(f"[{self.conn.getpeername()[0]}] Client ~{self.name}~ said> {self.missing}") 

                window.conn_button.click()
                window.clients.append(self.conn)
                (self.ip, self.port) = addr
                newthread = ClientThread(self.ip ,self.port ,self.conn , self.name, byte_im) 
                window.threads.append(newthread)
                newthread.start()  
    
class ClientThread(QThread): 
    change_pixmap_signal = pyqtSignal(np.ndarray)
 
    def __init__(self,ip,port,conn,name, img): 
        super().__init__() 
        self.ip = ip 
        self.port = port 
        self.conn = conn
        self.name = name
        self.img = img
        window.chat.append(f"[+] New server socket thread started for ~{self.name}~ at " + ip + ":" + str(self.port)) 
      
    def run(self): 
        while True: 
            try:   
                self.data = self.conn.recv(BUFFER_SIZE) 
                index = window.clients.index(self.conn)
                if len(self.data) < 2_000:
                    if rsa.decrypt(self.data, private_key).decode("utf-8") == "camera::CAMERA_CODE_":
                        window.FeedLabels[index].get_vid(self.img)
                        window.cameras[index] = False
                    self.data = rsa.decrypt(self.data, private_key).decode("utf-8")
                    if self.data[-1] == '_': 
                        self.end = window.code(self.data, index, self.conn, self.name)
                        time.sleep(0.2)
                        if self.end:
                            break
                    else:
                        window.chat.append(f"[{self.conn.getpeername()[0]}] Client ~{self.name}~ message> " +self.data)
                        if options[2]:
                            engine.say(self.data)
                            engine.runAndWait()
                else:
                    try:
                        window.FeedLabels[index].get_vid(self.data)   
                        window.cameras[index] = True                     
                    except OSError:
                        continue
            except:
                continue

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):   
        time.sleep(0.5)
        while True:
            Capture = cv2.VideoCapture(0)
            while options[0] and not options[3] and window.clients:
                try:
                    ret, frame = Capture.read()  
                    if ret:
                        frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5)
                        image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
                        for client in window.clients:
                            client.send(image_bytes)
                except ConnectionResetError:
                    window.special_commands(f"!kick! {window.names[window.clients.index(client)]}")
                except:
                    continue
            for client in window.clients:
                try:
                    client.send(rsa.encrypt("camera::CAMERA_CODE_".encode("utf-8"), public_partner))
                except ConnectionResetError:
                    window.special_commands(f"!kick! {window.names[window.clients.index(client)]}")

def purpleCylinder():
    t.setposition(0, 250)
    t.write("PurpleCylinder", font=("Aharoni",30, "normal"), align="center")
    t.setposition(0, 0)
    cursor_size = 20

    rad, heigh = [200, 500] 

    t.shape('square')
    t.shapesize(rad*2 / cursor_size, heigh / cursor_size)
    t.fillcolor('#7918cc')
    t.stamp()

    t.shape('circle')
    t.shapesize(stretch_len=rad / cursor_size)
    t.backward(heigh/2)
    t.stamp()

    t.forward(5)
    t.pencolor('#7918cc')
    t.stamp()

    t.forward(heigh - 5)
    t.color('black')
    t.stamp()
    time.sleep(2)
    t.bye()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    global window
    purpleCylinder()
    window = Window()
    window.show()
    sys.exit(app.exec_())
