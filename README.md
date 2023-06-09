# PyQt5-GUI-based-threaded-mutli-client-server-with-video-

This project allows you to connect via TCP client-server socket connection while having all the information displayed on a PyQt5 GUI window including chat and webcam video.

## Setup
Make sure your python VERSION is above 3.8 as I ran into problem with versions lower than 3.8 while testing. To test your python VERSION:
```bash
python --version
```
Use the python file named "setup.py" while in the project directory to automatically download all the modules used in this project.

```cmd
cd [PATH]
python setup.py
```
PATH - whare you essentially downloaded the project.

## Utilization

To start the simply navigate to your folder where you saved the project. Example of my destination of the PATH.

```cmd
cd C:\Prog\python\test
```
Then you can choose to either run the server
```cmd
python server.py
```
 or the client.
```cmd
python client.py
```
If you run a LAN client-server system only the server will capture the computer's webcam image while leaving the client with a cv2-warning (It does not terminate your code). 

## Thing to know 
The project should be saved in a folder, the name and location doesn't matter.  

Only 1 server and a maximum of 4 (this number is changeable) clients can run at a time. If either the server or the client aren't receiving webcam image, make sure if both your client and server aren't using the same webcam. 

It is NOT recommended to download any images, files, etc. to the folder "IconsAndImaged" reason being it will mess up the logic in the client code and the visual aspect of the GUI window.
Also try not to touch the "bans.txt" file because it COULD mess up server logic.

This version of the project also exists with an AUDIO part but it doesn't work simultaneously with the video part. The audio code for the project sits in the "audio.txt" file, to use you simply defy a threaded object and start the thread (the output class also receives a 'conn' variable like so "conn,addr = TCPServer.accept()".

```bash
            self.OutPut = OutPut(conn)        #OutPut handler
            self.OutPut.start()               #<==============

            self.InPut = InPut()              #InPut handler
            self.InPut.start()                #<==============
```
Feel free to experiment with it and let me know if you'd accomplished any result.

## Contributing

Pull requests are welcome. let me know what I did wrong or something that could be done better in the project.

Ministeru
