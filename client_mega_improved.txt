import sys
import os
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
import sounddevice as sd
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
CONNECTION_WINDOW_WIDTH = int(MONITOR_WIDTH*0.625)
CONNECTION_WINDOW_HEIGHT = int(MONITOR_HEIGHT*0.0872)

TCP_IP = socket.gethostbyname(socket.gethostname()) 
# TCP_IP = "192.168.1.25"

TCP_PORT = 7777 
BUFFER_SIZE = 1048576
camera = True
open_ = False
testing_ = False
global options
options = []
options.append(camera)
options.append(open_)
options.append(testing_)
global current_path
current_path = os.getcwd().replace("\\","/")
global Files 
Files = []
folder_dir = f"{current_path}/recievedIconsAndImages"

try:
    f = open(folder_dir)
except FileNotFoundError:
    os.mkdir(path = './recievedIconsAndImages')
except PermissionError:
    pass
else:
    pass

class Connection_Window(QDialog):                          
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(f'{folder_dir}/img4.png'))
        self.setFixedSize(CONNECTION_WINDOW_WIDTH , CONNECTION_WINDOW_HEIGHT)
        self.move(10,10)
        self.closeEvent
        self.setWindowTitle("Connect")
        self.setStyleSheet("""
        background-color: #702cab;
        color: #FFFFFF;
        font-family: Aharoni;
        font-size: 36px;

        QPushButton {
        background-color: #2ABf9E;
        padding: 20px;
        font-size: 36px; 

        .monospace {
        font-family: "Lucida Console", Courier, monospace;
        }
        }
        """)

        self.name=QLineEdit(self)
        self.name.setFixedSize(INI_WIDTH + int(MONITOR_WIDTH*0.07),INI_HEIGHT)
        self.name.setMaxLength(117)
        self.name.setPlaceholderText("Enter your name")
        self.name.setStyleSheet("""
        background-color: #7918cc;
        """)

        self.btnOK = QPushButton("Ok",self)
        self.btnOK.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.btnOK.move(200,460)
        self.btnOK.clicked.connect(self.ok)
        self.btnOK.setStyleSheet("""
        border: 2px solid white;
        background-color: #7918cc;
        """)

        anim=threading.Thread(target=self.animation, args=(self.name,))
        
        anim.start()

        self.grid_layout = QGridLayout(self)

        self.setLayout(self.grid_layout)
        self.grid_layout.setContentsMargins(20,20,10,10) 

        self.grid_layout.addWidget(self.name, 2, 1, alignment=Qt.AlignmentFlag.AlignAbsolute | Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.addWidget(self.btnOK, 2, 2, alignment=Qt.AlignmentFlag.AlignAbsolute | Qt.AlignmentFlag.AlignCenter)
        
    def closeEvent(self, event):
        global name
        text = self.name.text()
        if len(text) > 0:
            name = text
            return
        reply = QMessageBox.question(self, 'Exit', 'Program will exit',
            QMessageBox.Ok) 
        os._exit(1)

    def animation(self, name):
        data = ["e","n","t","e","r"," ","y","o","u","r"," ","n","a","m","e"]
        while True:
            for x in range(len(data)):
                old = data[x]
                data[x] = old.upper()
                text = "".join(data)
                self.name.setPlaceholderText(text)
                data[x] = old
                time.sleep(0.2)
            text = "".join(data)
            self.name.setPlaceholderText(text)

    def ok(self):
        global name
        text=self.name.text()
        if self.name.text() == "" or self.name.text() == "exit::EXIT_CODE_":
            reply = QMessageBox.question(self, 'Error', 'Invalid name',
                    QMessageBox.Ok)
            return
        else:
            name = text
            self.close()

class Settings(QDialog):
    def __init__(self):
        super().__init__()
        self.background_list = ["Default", "Black", "Grey", "Green"]
        self.font_list = ["Arial", "Times", "Calibri", "David"]

        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(f'{folder_dir}/img5.png'))
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

        self.layout.addWidget(self.background_text, 0, 0)
        self.layout.addWidget(self.background_box, 0, 1)
        self.layout.addWidget(self.font_text, 1, 0)
        self.layout.addWidget(self.font_box, 1, 1)
        self.layout.addWidget(self.camera_text, 2, 0)
        self.layout.addWidget(self.camera_button_, 2, 1)

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
        options[2] = True
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
        time.sleep(0.2)
        options[2] = False

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
        self.setting = []
        self.buttons = []
        self.threads = [] 
        self.setFixedSize(MONITOR_WIDTH , MONITOR_HEIGHT)
        self.setWindowTitle("Client")
        self.setWindowIcon(QIcon(f'{folder_dir}/img1.png'))
        self.closeEvent
        self.reconnecting = False
        self.recieving = False
        self.setStyleSheet("""
        background-color: #7918cc;
        color: #FFFFFF;
        font-family: Aharoni;
        font-size: 36px;

        QPushButton {
        background-color: #2ABf9E;
        padding: 20px;
        font-size: 36px; 

        .monospace {
        font-family: "Lucida Console", Courier, monospace;
        }
        }
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
        self.btnSend.move(200,460)
        self.btnSend.clicked.connect(self.send)
        self.btnSend.setStyleSheet("""
        border: 2px solid white;
        """)
        self.buttons.append(self.btnSend)

        self.stn_button = QPushButton("",self)
        self.stn_button.setIcon(QIcon(f'{folder_dir}/img6.png'))
        self.stn_button.setIconSize(QSize(BUTTON_HEIGHT - 20,BUTTON_HEIGHT - 20))
        self.stn_button.setFixedSize(BUTTON_HEIGHT, BUTTON_HEIGHT)
        self.stn_button.move(20,20)
        self.stn_button.setStyleSheet("""
        border: 2px solid white;
        """)
        self.stn_button.clicked.connect(self.settings)
        self.buttons.append(self.stn_button)

        self.chat = QTextEdit()
        self.chat.setFixedSize(int(MONITOR_WIDTH*0.6),int(MONITOR_HEIGHT*0.48))
        self.chat.setStyleSheet("""
        border: 2px solid white;
        font-family: Arial; font-size: 26px;
        background-color: #4e4f45;
        """)
        self.chat.setReadOnly(True)

        self.cls_button = QPushButton("Clear")
        self.cls_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.cls_button.clicked.connect(self.clear)
        self.cls_button.setStyleSheet("""
        border: 2px solid white;
        """)
        self.buttons.append(self.cls_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setStyleSheet("""
        border: 2px solid white;
        """)
        self.buttons.append(self.exit_button)

        self.camera_button = QPushButton("",self)
        self.camera_button.setIcon(QIcon(f'{folder_dir}/img0.png'))
        self.camera_button.setIconSize(QSize(BUTTON_HEIGHT,BUTTON_HEIGHT))
        self.camera_button.setFixedSize(BUTTON_HEIGHT, BUTTON_HEIGHT)
        self.camera_button.move(20,MESSAGE_START)
        self.camera_button.setStyleSheet("""
        border: 2px solid white;
        """)
        self.camera_button.clicked.connect(self.camera)
        self.buttons.append(self.camera_button)

        self.FeedLabel = QLabel(self)
        self.FeedLabel.setFixedSize(int(MONITOR_WIDTH*0.445), int(MONITOR_HEIGHT*0.35))
        self.FeedLabel.setStyleSheet("""
        border: 2px solid white;
        """)
        self.img = QPixmap(f'{folder_dir}/img3.png')
        self.FeedLabel.setPixmap(self.img)
        self.FeedLabel.resize(int(MONITOR_WIDTH*0.445), int(MONITOR_HEIGHT*0.35))
        self.buttons.append(self.FeedLabel)

        self.grid_layout = QGridLayout(self)

        self.setLayout(self.grid_layout)
        self.grid_layout.setContentsMargins(20,20,10,10) 

        self.grid_layout.addWidget(self.btnSend, 7, 1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(self.chat, 6 ,1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.addWidget(self.chatTextField, 7, 1, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.cls_button, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.grid_layout.addWidget(self.exit_button, 4, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(self.FeedLabel, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.clientThread = ClientThread(self)

        self.clientThread.change_pixmap_signal.connect(self.update_image)

        self.clientThread.start()

        anim=threading.Thread(target=self.animation)
        
        anim.start()

    def settings(self,):
        if options[1]: 
           pass
        elif not options[1]:
            s = Settings()   
            self.setting.append(s)
            s.show()
            options[1] = True

    def camera(self,):
        if not options[0]:
            self.camera_button.setIcon(QIcon(f'{folder_dir}/img0.png'))
            self.camera_button.setIconSize(QSize(BUTTON_HEIGHT,BUTTON_HEIGHT))
            options[0] = True
        elif options[0]:
            self.camera_button.setIcon(QIcon(f'{folder_dir}/img2.png'))
            self.camera_button.setIconSize(QSize(BUTTON_HEIGHT,BUTTON_HEIGHT))
            options[0] = False

    def closeEvent(self, event):
        if self.reconnecting:
            reply = QMessageBox.question(self, 'Window Close', 'Client is reconnecting',
                    QMessageBox.Ok)
            event.ignore() 
        elif self.recieving:
            reply = QMessageBox.question(self, 'Window Close', 'Client is recieving files, please wait',
                    QMessageBox.Ok)
            event.ignore() 
        else:
            event.accept()
            self.exit_button.click()

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

    def send(self):
        text=self.chatTextField.text()
        if text == "": 
            self.chat.append(f"Can't send empty message")
            return
        elif text[-1] == '_': 
            self.chat.append(f"Illigal message")
            return
        else:
            try:
                tcpClientA.send(rsa.encrypt(text.encode("utf-8"), public_partner))
                self.chat.append(f"[{socket.gethostbyname(socket.gethostname())}] Your message> "+text)
                self.chatTextField.setText("")
            except:
                self.chat.append(f"There's no one home")
        self.chatTextField.setText("")

    def clear(self):
        self.chat.setText("")
        self.chat.update()

    def exit(self):
        try:
            options[0] = False
            time.sleep(0.2)
            tcpClientA.send(rsa.encrypt("exit::EXIT_CODE_".encode("utf-8"), public_partner))
            time.sleep(0.2)
            tcpClientA.close()
            os._exit(1)
        except:
            os._exit(1)
               
class ClientThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, window):
        super().__init__() 
        self.window=window

    def get_vid(self, data):
        try:
            buff = np.frombuffer(data, np.uint8)
            buff = buff.reshape(1, -1)
            img = cv2.imdecode(buff, cv2.IMREAD_COLOR)
            self.change_pixmap_signal.emit(img)
        except TypeError:
            None

    def ImageUpdateSlot(self, Image):
        window.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def connect(self, tcpClientA):
        DELAY3 = 3
        DELAY5 = 5
        retries = 0
        while True:
            try:
                tcpClientA.connect((TCP_IP, TCP_PORT))
                break
            except ConnectionRefusedError:
                window.reconnecting = True
                if retries < 3:
                    window.chat.append(f"Server is currently offline retrying in {str(DELAY3)} seconds")
                    time.sleep(int(DELAY3))
                elif retries < 5:
                    window.chat.append(f"Server is currently offline retrying in {str(DELAY5)} seconds")
                    time.sleep(int(DELAY5))
                else:
                    window.chat.append(f"Server seems to be down... exiting")
                    time.sleep(2)
                    window.exit()
                retries += 1
                window.cls_button.click()

    def recv_files(self, lenght):
            tcpClientA.send(rsa.encrypt("missing".encode("utf-8"), public_partner))
            window.recieving = True
            window.exit_button.setDisabled(True)
            window.btnSend.setDisabled(True)

            window.chat.append(f"Receiving {lenght} files...")
            complete = True
            i = 0
            while complete:
                try:
                    for i in range(lenght):
                        data = tcpClientA.recv(BUFFER_SIZE)
                        image_data = data
                        image = Image.open(io.BytesIO(image_data))
                        image.save(f"{folder_dir}/img{i}.png")
                        Files.append(f"img{i}.png")
                        window.chat.append(f"received {i + 1}/{lenght} files")
                        tcpClientA.send(rsa.encrypt("Ok".encode("utf-8"), public_partner))
                    tcpClientA.send(rsa.encrypt("Ok".encode("utf-8"), public_partner))
                except:
                    window.chat.append(f"Error has accured... Retrying")
                    tcpClientA.send(rsa.encrypt("Retry".encode("utf-8"), public_partner))
                    i = 0
                    continue
                if i == lenght - 1:
                    window.chat.append(f"All files transmitted succesfully")
                    window.update()
                    tcpClientA.send(rsa.encrypt("Ok".encode("utf-8"), public_partner))
                    complete = False

                window.recieving = False
                window.exit_button.setDisabled(False)
                window.btnSend.setDisabled(False)

                window.camera_button.setIcon(QIcon(f'{folder_dir}/img0.png'))
                window.camera_button.setIconSize(QSize(BUTTON_HEIGHT,BUTTON_HEIGHT))
                window.setWindowIcon(QIcon(f'{folder_dir}/img1.png'))
                window.stn_button.setIcon(QIcon(f'{folder_dir}/img6.png'))
                window.stn_button.setIconSize(QSize(BUTTON_HEIGHT,BUTTON_HEIGHT))

    def run(self):
        global public_key, private_key
        global public_partner
        global tcpClientA
        global data
        global name

        public_key, private_key = rsa.newkeys(1024)
        public_partner = None

        BUFFER_SIZE = 1048576 
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.connect(tcpClientA)

        public_partner = rsa.PublicKey.load_pkcs1(tcpClientA.recv(1024))
        tcpClientA.send(public_key.save_pkcs1("PEM"))

        data = tcpClientA.recv(BUFFER_SIZE)
        window.chat.append(f"Connected to ["+rsa.decrypt(data, private_key).decode("utf-8")+"]")

        tcpClientA.send(rsa.encrypt(name.encode("utf-8"), public_partner))

        server_msg = rsa.decrypt(tcpClientA.recv(BUFFER_SIZE), private_key).decode("utf-8")
        if server_msg == 'Ban':
            window.chat.append(f"Server said> Client ~{name}~ tried to connect but is banned by the server")
            time.sleep(4)
            os._exit(1)
        elif server_msg == 'Ok':
            window.chat.append(f"Server said> Client ~{name}~ connected")

        lenght = int(rsa.decrypt(tcpClientA.recv(BUFFER_SIZE), private_key).decode("utf-8"))

        all_ = True
        for i in range(lenght):
            if not os.path.isfile(f'{folder_dir}/img{i}.png'):
                self.recv_files(lenght)
                all_ = False
                break
        if all_:
            tcpClientA.send(rsa.encrypt("Ok".encode("utf-8"), public_partner))

        image = Image.open(f'{folder_dir}/img3.png')
        im_resize = image.resize((int(MONITOR_WIDTH*0.445), int(MONITOR_HEIGHT*0.35)))
        buf = io.BytesIO()
        im_resize.save(buf, format='PNG')
        byte_im = buf.getvalue()

        self.Worker1 = Worker1()              #WebCam handler
        self.Worker1.start()                  #<==============
        
        while True:
            try:
                data = tcpClientA.recv(BUFFER_SIZE)
                if len(data) < 2_000:
                    if rsa.decrypt(data, private_key).decode("utf-8") == "exit::EXIT_CODE_":
                        self.get_vid(byte_im)
                        window.chat.append(f"Server has shut down")
                        time.sleep(2)
                        window.chat.append(f"EXITTING")
                        tcpClientA.close() 
                        break
                    elif rsa.decrypt(data, private_key).decode("utf-8") == "kick::KICK_CODE_":
                        self.get_vid(byte_im)
                        window.chat.append(f"Server has kicked you")
                        time.sleep(2)
                        window.chat.append(f"Exiting") 
                        break
                    elif rsa.decrypt(data, private_key).decode("utf-8") == "camera::CAMERA_CODE_":
                        self.get_vid(byte_im)
                    elif rsa.decrypt(data, private_key).decode("utf-8") == "ban::BAN_CODE_":
                        self.get_vid(byte_im)
                        window.chat.append(f"Server has banned you")
                        time.sleep(2)
                        window.chat.append(f"Exiting") 
                        break
                    else:   
                        data = rsa.decrypt(data, private_key).decode("utf-8")
                        window.chat.append(f"[{TCP_IP}] Server message> " +data)
                else:
                        try:
                            self.get_vid(data)
                        except TypeError:
                            continue
            except:
                continue

        time.sleep(1)
        os._exit(1)

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):   
        time.sleep(0.5)
        while True:
            Capture = cv2.VideoCapture(0)
            while options[0] and not options[2]:
                try:
                    ret, frame = Capture.read()  
                    if ret:
                        image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
                        tcpClientA.send(image_bytes)
                except ConnectionResetError:
                    window.chat.append(f"Server connection got terminated")
                    time.sleep(2)
                    window.exit()
                except:
                    continue
            try:
                tcpClientA.send(rsa.encrypt("camera::CAMERA_CODE_".encode("utf-8"), public_partner))
            except ConnectionResetError:
                window.chat.append(f"Server connection got terminated")
                time.sleep(2)
                window.exit()

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
    connection_Window = Connection_Window()
    connection_Window.exec()
    window = Window()
    window.show()
    sys.exit(app.exec_())