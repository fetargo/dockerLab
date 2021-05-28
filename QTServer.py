import socket
from sys import getsizeof
import cv2
import numpy as np
from PIL import Image
import PIL
import io
import time



def receiver():
    mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    mainSocket.bind(('', 12345))
    print('Socket bind complete')

    mainSocket.listen(1)
    print('Socket now listening')

    conn, addr = mainSocket.accept()
    print('Connection accepted')

    tcpPort = 6060
    udpPort = 5050

    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.bind(('', tcpPort))
    tcpSocket.listen(1)
    print('TCP socket ready and listening')

    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.bind(('', udpPort))
    print('UDP socket ready')
    
    while True:
        messageType = conn.recv(512)
        print("messageType recieved")
        if messageType == b'\x01':
            print("messageType = 1")
            sendReady(conn)
            messageType = conn.recv(512)
            print('Choice recieved', messageType)
            sendPort(conn, messageType, tcpPort, udpPort)
        elif messageType == b'\x02':
            print("messageType = 2")
            # check thread or create if there is not
            tcpTransfer(tcpSocket)
            tcpSocket.listen(1)
        elif messageType == b'\x03':
            print("messageType = 3")
            # check thread or create if there is not
            udpTransfer(udpSocket, conn)

def sendReady(conn):
    print("Sending ready signal")
    conn.send(b'\x00\x00')

def sendPort(conn, connType, tcpPort, udpPort):
    print('sendPort func enter')
    if connType == b'\x01':
        print('Sending TCP port', tcpPort)
        conn.send(tcpPort.to_bytes(2, "big"))
        print('TCP port sent (bytes)', tcpPort.to_bytes(2, "big"))
    elif connType == b'\x02':
        print('Sending UDP port', udpPort)
        conn.send(udpPort.to_bytes(2, "big"))
        print('UDP port sent (bytes)', udpPort.to_bytes(2, "big"))


def tcpTransfer(socket):
    print('tcpTransfer func enter')
    conn, addr = socket.accept()
    print('TCP connection accepted')
    fileName = 'ServerImage.png'
    image = Image.open(fileName,'r')
    print('Image file opened')
    imageByte = image_to_byte_array(image)
    print('Image translated to byte array')
    #size = getsizeof(imageByte)
    conn.send(imageByte)
    print('Image sent')
    conn.close()
    print('TCP connection closed')


def udpTransfer(socket, mainConn):
    conn, addr = socket.recvfrom(512)
    capture = cv2.VideoCapture("/home/fetargo/git/SocketsPy/test.mp4")
    while True:
        sentLength = 0
        err, frame = capture.read()
        for i in range(20):
        	err, frame = capture.read()
        print('Frame captured')
        image = cv2.imencode('.jpg', frame)[1].tobytes()
        print('Frame encoded to bytes')
        ##conn.sendall(image)
        mainConn.send(len(image).to_bytes(4, 'big'))
        print('Frame length sent: ', len(image))
        imgLength = len(image)
        while sentLength < imgLength:
        	imagePart = image[sentLength:sentLength+8096]
        	sentLength += 8096
        	socket.sendto(imagePart, addr)
        	print("Image part sent, length: ", sentLength)
        print('Frame sent')
        time.sleep(0.1)


def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

if __name__ == "__main__":
    receiver()
