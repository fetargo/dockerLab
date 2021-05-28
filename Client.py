import socket
import cv2
import numpy as np
from PIL import Image

port = 0
initSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.140.128"

def connect():
    try:
        initSocket.connect((host, 12345))
    except:
        return 1
    return 0
    #close_program

def sendChoice(choice):
    answer = None
    messageType = b'\x01'
    try:
        initSocket.send(bytes(messageType))
        print("Connection message sent ", bytes(messageType))
        answer = initSocket.recv(512)
        print("Connection message recieved")
    except:
        initSocket.close()
        return 1
    if not answer:
        return 1
    initSocket.send(choice.to_bytes(1, "big"))
    print("Choice sent", choice)
    port = int.from_bytes(initSocket.recv(512), "big")
    print("Port recieved", port)
    if not port:
        return 1
    return 0, port
#send 

def useTCP(port):
    print("useTCP function enter. Port = ", port)
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    answer = None
    messageType = b'\x02'
    try:
        initSocket.send(bytes(messageType))
        tcpSocket.connect((host, port))
    except:
        initSocket.close()
        return 1

    fileName = 'Image.png'
    image = open(fileName,'wb')
    while True:
        dataPart = tcpSocket.recv(1024)
        if not dataPart:
            break
        image.write(dataPart)
    
    print("Image received successfully")
    image.close()

    ##try:
    ##    image = Image.open(fileName)
    ##    print("Image converting success")
    ##except:
    ##    print("Image converting failure")
    ##    tcpSocket.close()
    ##    return 1

    tcpSocket.close()
    ##return image
    return fileName

def connectUDP(port):
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("UDP socket created")
    addr = (host, port)
    messageType = b'\x03'
    try:
        initSocket.send(bytes(messageType))
        ##answer = int(initSocket.recv(512))
        ##if answer == 1:
        ##    UDPSocket = udpSocket
    except:
        initSocket.close()
        return 1
    udpSocket.sendto(b'\x01', addr)
    return 0, udpSocket


def useUDP(UDPSocket):
    print("useUDP func enter")
    if UDPSocket == None:
        return 1
    print("Receiving image len")
    data = initSocket.recv(512)

    img_len = int.from_bytes(data, 'big') # lenght of image
    print("Image lenght = ", img_len)
    e=0
    data = b''
    while e < img_len:
        d,addr = UDPSocket.recvfrom(8096)
        e += len(d)
        data += d
        print(e)
    print("Raw data recieved, length: ", e)
    nparr = np.fromstring(data, np.uint8)
    print("NumPy array converted from string")
    frame = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    return frame

if __name__ == "__main__":
    initSocket.send(bytes('hello, motherfucker!', encoding = 'UTF-8'))

    print("Enter file name of the image with extentsion (example: filename.jpg,filename.png or if a video file then filename.mpg etc) - ")
    fileName = 'Image.png'
    image = open(fileName,'w')
    while True:
        dataPart = initSocket.recv(512)
        if not dataPart:
            break
        image.write(dataPart)
    image.close()
    print("Image received successfully")


    #photo = PhotoImage(file="Image.png")
