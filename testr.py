import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from vidstream import *
import socket
import threading
from threading import Thread
from screeninfo import get_monitors
import cv2, pickle, struct, imutils
from PIL import Image
import io
import numpy as np
import pyttsx3
import time
import rsa
import sounddevice as sd
import numpy
assert numpy
import tqdm

# CHUNK = 2**5
# RATE = 44100
# LEN = 10

# p = pyaudio.PyAudio()

# stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
# player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)


# for i in range(int(LEN*RATE/CHUNK)): #go for a LEN seconds
#     data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
#     player.write(data,CHUNK)


# stream.stop_stream()
# stream.close()
# p.terminate()
#-----------------------------------------------------------------
# import pyaudio
# import numpy as np

# CHUNK = 2**5
# RATE = 44100
# LEN = 10

# p = pyaudio.PyAudio()

# stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
# player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)

# for i in range(int(LEN*RATE/CHUNK)): #go for a LEN seconds
#     data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
#     player.write(data,CHUNK)

# stream.stop_stream()
# stream.close()
# p.terminate()
#-----------------------------------------------------------------
# import sys

# import pyaudio

# RECORD_SECONDS = 5
# CHUNK = 1024
# RATE = 44100

# p = pyaudio.PyAudio()
# stream = p.open(format=p.get_format_from_width(2),
#                 channels=1 if sys.platform == 'darwin' else 2,
#                 rate=RATE,
#                 input=True,
#                 output=True,
#                 frames_per_buffer=CHUNK)

# print('* recording')
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     stream.write(stream.read(CHUNK))
# print('* done')

# stream.close()
# p.terminate()
#-----------------------------------------------------------------
# import sys
# from PyQt5 import QtGui
# from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
#                              QToolTip, QMessageBox, QLabel)

# class Window2(QMainWindow):                           # <===
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Window22222")

# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.arr = []

#         self.title = "First Window"
#         self.top = 100
#         self.left = 100
#         self.width = 680
#         self.height = 500

#         self.pushButton = QPushButton("Start", self)
#         self.pushButton.move(275, 200)
#         self.pushButton.setToolTip("<h3>Start the Session</h3>")

#         self.pushButton.clicked.connect(self.window2)              # <===

#         self.main_window()

#     def main_window(self):
#         self.label = QLabel("Manager", self)
#         self.label.move(285, 175)
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.top, self.left, self.width, self.height)
#         self.show()

#     def window2(self):                                             # <===
#         self.w = Window2()
#         self.arr.append(self.w)
#         self.w.show()
#         # self.hide()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Window()
#     sys.exit(app.exec())
#-----------------------------------------------------------------
# class AnotherWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         self.label = QLabel()
#         self.setWindowTitle("Zmiana tła")
#         layout.addWidget(self.label)
#         self.setLayout(layout)

#         self.combo_box = QComboBox()
#         layout.addWidget(self.combo_box)

#         geek_list = ["red", "green", "yellow", "blue"]

#         model = self.combo_box.model()
#         for row, color in enumerate(geek_list):
#             self.combo_box.addItem(color.title())
#             model.setData(model.index(row, 0), QColor(color), Qt.BackgroundRole)

#         self.combo_box.activated.connect(self.accept)

#     def color(self):
#         return self.combo_box.currentData(Qt.BackgroundRole)

#     def colorName(self):
#         return self.combo_box.currentText()


# class Window(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.setWindowTitle("Dialogi")
#         actionFile = self.menuBar().addMenu("Dialog")
#         action = actionFile.addAction("New")
#         action.triggered.connect(self.selectColor)
#         actionFile.addAction("Open")

#     def selectColor(self):
#         dialog = AnotherWindow()
#         if dialog.exec_():
#             print(dialog.color())
#             print(dialog.colorName())

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = AnotherWindow()
#     window.show()
#     sys.exit(app.exec_())
#-----------------------------------------------------------------
# import argparse

# import sounddevice as sd
# import numpy  # Make sure NumPy is loaded before it is used in the callback
# assert numpy  # avoid "imported but unused" message (W0611)

# def callback(indata, outdata, frames, time, status):
#     outdata[:] = indata             #<====== Data conventer:Output
#     # print(indata.tobytes())
#     # print(len(indata.tobytes()))

# try:
#     with sd.Stream(callback=callback):
#         print('#' * 80)
#         print('press Return to quit')
#         print('#' * 80)
#         input()
# except:
#     os._exit(1)

# import sounddevice as sd
# import sys

# CHUNK = 4096

# stream = sd.Stream(
#   samplerate=44100,
#   channels=2,
#   blocksize=CHUNK)

# def main(argv):
#     stream.start() # <––––––– This was missing
#     while True:
#         indata, overflowed = stream.read(CHUNK)
#         # sending data to socket server
#         # doing some processing in the server
#         # data returned from the socket is written  to the outputstream(speaker)
#         stream.write(indata)

# if __name__ == "__main__":
#   main(sys.argv)

# import cv2
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
# print(width, height)
# ---------------------------------------------------------------

# TCP_IP = "192.168.1.25"
# TCP_IP = "192.168.1.71"
# TCP_PORT = 7777 
# BUFFER_SIZE = 1048576
# SEPARATOR = "<SEPARATOR>"
# camera = True
# open = False
# global options
# options = []
# options.append(camera)
# options.append(open)
# global Files 
# Files = []
# # Files.append('black.jpg')
# # Files.append('grey.jpg')
# # Files.append('hacker.jpg')
# Files.append('line.png')
# Files.append('camera_on.png')
# Files.append('settings.png')
# Files.append('settings-dark.png')
# Files.append('hacker-icon.png')
# Files.append('pngtree.png')

# TCPServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# TCPServer.bind((TCP_IP, TCP_PORT)) 
# # self.Worker1 = Worker1()              #WebCam handler
# # self.Worker1.start()                  #<==============

# TCPServer.listen(4) 
# while True:
#     print("listening...")
#     global addr
#     conn,addr = TCPServer.accept()
#     print(f'{conn} connected')

#     conn.send(str(len(Files)).encode("utf-8"))

#     # conn.send("hello".encode("utf-8"))
#     def send_files(Files, conn):
#         complete = True
#         i = 0
#         while complete:
#             try:
#                 for i in range(len(Files)):
#                     msg = ""
#                     try:
#                         im = Image.open(str(Files[i]))
#                         im_resize = im.resize((500, 500))
#                         buf = io.BytesIO()
#                         im_resize.save(buf, format='png')
#                         byte_im = buf.getvalue()
#                         conn.send(byte_im)
#                         print(i)
#                         time.sleep(1.5)
#                         i +=1
#                     except:
#                         i = 0
#                         continue
#                 msg = conn.recv(BUFFER_SIZE).decode("utf-8")
#                 print(msg[0:5])
#                 if msg[0:5] == "RETRY":
#                     send_files(Files, conn)
#                 if msg[0:5] == "OK":
#                     complete = False
#                 print(i, len(Files))
#             except ConnectionAbortedError:
#                     complete = False

#     send_files(Files, conn)

    # im = Image.open('settings.png')
    # im_resize = im.resize((500, 500))
    # buf = io.BytesIO()
    # im_resize.save(buf, format='PNG')
    # byte_im = buf.getvalue()


    # for filename in Files:
    #     filesize = os.path.getsize(filename)
    #     conn.send(f"{filename}{SEPARATOR}{filesize}".encode())
    #     progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    #     with open(filename, "rb") as f:
    #         while True:
    #             # read the bytes from the file
    #             bytes_read = f.read(BUFFER_SIZE)
    #             if not bytes_read:
    #                 # file transmitting is done
    #                 break
    #             # we use sendall to assure transimission in 
    #             # busy networks
    #             conn.sendall(bytes_read)
    #             # update the progress bar
    #             progress.update(len(bytes_read))
# -----------------------------------------------------------------------------------------
# import socket
# # IP = socket.gethostbyname(socket.gethostname())
# IP = "192.168.9.185"
# PORT = 4455
# ADDR = (IP, PORT)
# SIZE = 1024
# FORMAT = "utf-8"
# def main():
#     print("[STARTING] Server is starting.")

#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     server.bind(ADDR)

#     server.listen()
#     print("[LISTENING] Server is listening.")
#     while True:

#         conn, addr = server.accept()
#         print(f"[NEW CONNECTION] {addr} connected.")

#         filename = conn.recv(SIZE).decode(FORMAT)
#         print(f"[RECV] Receiving the filename.")
#         file = open(filename, "w")
#         conn.send("Filename received.".encode(FORMAT))

#         data = conn.recv(SIZE).decode(FORMAT)
#         print(f"[RECV] Receiving the file data.")
#         file.write(data)
#         conn.send("File data received".encode(FORMAT))

#         file.close()

#         conn.close()
#         print(f"[DISCONNECTED] {addr} disconnected.")
# if __name__ == "__main__":
    # main()
# --------------------------------------------------------------
# with open('bans.txt', 'r') as f:
#     bans = f.readlines()
# print(bans)
# name = input("name>")
# if name+'\n' in bans:
#     print(f"{name} already banned")
# else:
#     with open('bans.txt', 'a') as f:
#         f.write(name+'\n')

# import os
# print(os.system('ipconfig'))

# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])
# s.close()
# -----------------------------------------------------
# import os
# from os import listdir
# global Files
# Files = []
# folder_dir = "C:/Prog/python/test/iconsAndImages"
# for images in os.listdir(folder_dir):
 
#     # check if the image ends with png
#     if (images.endswith(".png")):
#         Files.append(images)
#         # print(images)
# print(os.getcwd())
# print(os.getcwd().replace("\\","/"))
# --------------------------------------------------------
# global current_path
# current_path = os.getcwd().replace("\\","/")
# path = './projects'
# global Files 
# Files = []
# folder_dir = f"{current_path}/recievedIconsAndImages"

# try:
#     f = open(folder_dir)
# except FileNotFoundError:
#     os.mkdir(path = './recievedIconsAndImages')
# except PermissionError:
#     pass
# else:
#     pass
# --------------------------------------------------------
# SERVER_HOST = 'localhost'
# SERVER_PORT = 5000

# # Create a socket object
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((SERVER_HOST, SERVER_PORT))
# print('Connected to the server')

# # Function to receive and display the frame
# def receive_frame():
#     frame_size = int.from_bytes(client_socket.recv(4), byteorder='big')
#     frame_data = b''

#     while len(frame_data) < frame_size:
#         frame_data += client_socket.recv(frame_size - len(frame_data))

#     frame = np.frombuffer(frame_data, dtype=np.uint8)
#     frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
#     cv2.imshow('Screen', frame)
#     cv2.waitKey(1)

# try:
#     while True:
#         # Receive and display the frame
#         receive_frame()

# except KeyboardInterrupt:
#     # Clean up the connection
#     client_socket.close()
#     cv2.destroyAllWindows()
# ------------------------------------------------
# class MainWindow(QWidget):
#     def __init__(self):
#         super(MainWindow, self).__init__()

#         self.VBL = QVBoxLayout()

#         self.FeedLabel = QLabel()
#         self.VBL.addWidget(self.FeedLabel)


#         self.Worker1 = Worker1()

#         self.Worker1.start()
#         self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
#         self.setLayout(self.VBL)

#     def ImageUpdateSlot(self, Image):
#         self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

# class Worker1(QThread):
#     ImageUpdate = pyqtSignal(QImage)
#     def run(self):
#         Capture = cv2.VideoCapture(0)
#         while True:
#             ret, frame = Capture.read()
#             if ret:
#                 Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 FlippedImage = cv2.flip(Image, 1)
#                 ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
#                 Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
#                 self.ImageUpdate.emit(Pic)

# if __name__ == "__main__":
#     App = QApplication(sys.argv)
#     Root = MainWindow()
#     Root.show()
#     sys.exit(App.exec())
#---------------------------------------------------------------------------------
# from PyQt5 import QtGui
# from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
# from PyQt5.QtGui import QPixmap
# import sys
# import cv2
# from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
# import numpy as np


# class VideoThread(QThread):
#     change_pixmap_signal = pyqtSignal(np.ndarray)

#     def __init__(self):
#         super().__init__()
#         self._run_flag = True

#     def run(self):
#         # capture from web cam
#         cap = cv2.VideoCapture(0)
#         while self._run_flag:
#             ret, cv_img = cap.read()
#             if ret:
#                 self.change_pixmap_signal.emit(cv_img)
#         # shut down capture system
#         cap.release()

#     def stop(self):
#         """Sets run flag to False and waits for thread to finish"""
#         self._run_flag = False
#         self.wait()


# class App(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Qt live label demo")
#         self.disply_width = 640
#         self.display_height = 480
#         # create the label that holds the image
#         self.image_label = QLabel(self)
#         self.image_label.resize(self.disply_width, self.display_height)
#         # create a text label
#         self.textLabel = QLabel('Webcam')

#         # create a vertical box layout and add the two labels
#         vbox = QVBoxLayout()
#         vbox.addWidget(self.image_label)
#         vbox.addWidget(self.textLabel)
#         # set the vbox layout as the widgets layout
#         self.setLayout(vbox)
# #-------------------------------------------------------------------------------
#         # create the video capture thread
#         self.thread = VideoThread()
#         # connect its signal to the update_image slot
#         self.thread.change_pixmap_signal.connect(self.update_image)
#         # start the thread
#         self.thread.start()

#     def closeEvent(self, event):
#         self.thread.stop()
#         event.accept()



#     @pyqtSlot(np.ndarray)
#     def update_image(self, cv_img):
#         """Updates the image_label with a new opencv image"""
#         qt_img = self.convert_cv_qt(cv_img)
#         self.image_label.setPixmap(qt_img)
    
#     def convert_cv_qt(self, cv_img):
#         """Convert from an opencv image to QPixmap"""
#         rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
#         h, w, ch = rgb_image.shape
#         bytes_per_line = ch * w
#         convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
#         p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
#         return QPixmap.fromImage(p)
    
# if __name__=="__main__":
#     app = QApplication(sys.argv)
#     a = App()
#     a.show()
#     sys.exit(app.exec_())


#-------------------------------------------------------------------------------
# import sys
# import re

# from PyQt5.QtWidgets import (QApplication, QFormLayout, QLabel, QDialog, QLineEdit, QPushButton)

# from PyQt5 import QtCore, QtGui


# class AnimatedLabel(QLabel):
#     def __init__(self):
#         QLabel.__init__(self)

#         color1 = QtGui.QColor(255, 0, 0)
#         color2 = QtGui.QColor(255, 144, 0)
#         color3 = QtGui.QColor(255, 255, 0)
#         color4 = QtGui.QColor(224, 192, 192)

#         color5 = QtGui.QColor(192, 224, 192)
#         color6 = QtGui.QColor(192, 192, 192)
#         color7 = QtGui.QColor(212, 208, 200)

#         self.co_get = 0
#         self.co_set = 0

#         byar = QtCore.QByteArray()
#         byar.append('zcolor')
#         self.color_anim = QtCore.QPropertyAnimation(self, byar)
#         self.color_anim.setStartValue(color4)
#         self.color_anim.setKeyValueAt(0.15, color1)
#         self.color_anim.setKeyValueAt(0.3, color2)
#         self.color_anim.setKeyValueAt(0.5, color3)
#         self.color_anim.setKeyValueAt(0.75, color2)
#         self.color_anim.setEndValue(color4)
#         self.color_anim.setDuration(2000)
#         self.color_anim.setLoopCount(1)

#         self.color_anim_ok = QtCore.QPropertyAnimation(self, byar)
#         self.color_anim_ok.setStartValue(color5)
#         self.color_anim_ok.setKeyValueAt(0.5, color6)
#         self.color_anim_ok.setEndValue(color7)
#         self.color_anim_ok.setDuration(1000)
#         self.color_anim_ok.setLoopCount(-1)

#         self.custom_anim = QtCore.QPropertyAnimation(self, byar)

#     def parseStyleSheet(self):
#         ss = self.styleSheet()
#         sts = [s.strip() for s in ss.split(';') if len(s.strip())]
#         return sts

#     def getBackColor(self):
#         self.co_get += 1
#         # print(fuin(), self.co_get)
#         return self.palette().color(self.pal_ele)

#     def setBackColor(self, color):
#         self.co_set += 1
#         sss = self.parseStyleSheet()
#         bg_new = 'background-color: rgba(%d,%d,%d,%d);' % (color.red(), color.green(), color.blue(), color.alpha())

#         for k, sty in enumerate(sss):
#             if re.search('\Abackground-color:', sty):
#                 sss[k] = bg_new
#                 break
#         else:
#             sss.append(bg_new)

#         # pal = self.palette()
#         # pal.setColor(self.pal_ele, color)
#         # self.setPalette(pal)
#         self.setStyleSheet('; '.join(sss))

#     pal_ele = QtGui.QPalette.Window
#     zcolor = QtCore.pyqtProperty(QtGui.QColor, getBackColor, setBackColor)


# # this class is only for test
# class SomeDia2(QDialog):
#     def __init__(self, parent=None):
#         """Sets up labels in form"""
#         QDialog.__init__(self, parent)

#         self.co_press = 0

#         self.setModal(True)
#         self.setWindowTitle('Animation Example')

#         self.edit_pad =  QLineEdit('-1')
#         self.edit_rad =  QLineEdit('-1')
#         self._mapHeight = QLineEdit('0')

#         self.layout = QFormLayout()
#         self.lab_pad = QLabel('Padding (px):')
#         self.lab_rad = QLabel('Radius (px):' )
#         self.layout.addRow(self.lab_pad, self.edit_pad)
#         self.layout.addRow(self.lab_rad, self.edit_rad)

#         self.anila = AnimatedLabel()
#         self.anila.setText('Label for animation:')
#         # self.anila.setStyleSheet('padding: 0 4px; border-radius: 4px;')
#         self.layout.addRow(self.anila, self._mapHeight)

#         self.ok = QPushButton()
#         self.ok.setText('OK -- change animation')
#         self.ok.clicked.connect(self._okPress)

#         self.layout.addRow(self.ok)
#         self.layout.setLabelAlignment(QtCore.Qt.AlignRight)

#         self.setLayout(self.layout)
#         self.set_initial_data()

#     def set_initial_data(self):
#         pad_vali = QtGui.QIntValidator(0, 20)
#         rad_vali = QtGui.QIntValidator(0, 10)

#         self.edit_pad.setValidator(pad_vali)
#         self.edit_rad.setValidator(rad_vali)

#         pad, rad = 4, 4
#         self.edit_pad.setText(str(pad))
#         self.edit_rad.setText(str(rad))

#         self.set_ss(pad,rad)

#         # slots
#         self.edit_pad.textChanged.connect(self.change_padrad)
#         self.edit_rad.textChanged.connect(self.change_padrad)

#     def set_ss(self, pad, rad):
#         self.anila.setStyleSheet('padding: 0 %dpx; border-radius: %dpx;' % (pad, rad))
#         for lab in [self.lab_rad, self.lab_pad]:
#             lab.setStyleSheet('padding: 0 %dpx;' % pad)

#     def change_padrad(self):
#         try:
#             pad = int(self.edit_pad.text())
#             rad = int(self.edit_rad.text())
#             # print(pad, rad)
#             self.set_ss(pad, rad)
#         except Exception as ex:
#             print(type(ex).__name__)

#     def _okPress(self, flag):
#         # print('OK PRESS', flag)
#         self.co_press += 1
#         typ = self.co_press % 3
#         if 0 == typ:
#             print('Animation NO')
#             self.anila.color_anim.stop()
#             self.anila.color_anim_ok.stop()
#         elif 1 == typ:
#             print('Animation type 1')
#             self.anila.color_anim_ok.stop()
#             self.anila.color_anim.start()
#         elif 2 == typ:
#             print('Animation type 2')
#             self.anila.color_anim.stop()
#             self.anila.color_anim_ok.start()

# if __name__ == "__main__":

#     app = QApplication(sys.argv)

#     dia = SomeDia2()
#     dia.show()

#     app.exec_()