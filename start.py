# -*- coding: utf-8 -*-s

import socket, time
import threading

host = ''
port = 9000
locaddr = (host,port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)

isOk = True


commandList = []
#commandList = ['command', 'takeoff', 'forward 90', 'ccw 180', 'forward 180', 'cw 180', 'forward 90', 'land']
#with open('example.txt') as f:
#    commandList = f.read().splitlines()

def recv():
    global isOk
    while True:
        try:
            data, server = sock.recvfrom(1518)
            mes = data.decode(encoding="utf-8")
            print(mes)
            if mes == "ok":
                isOk = True
                print(mes)
        except Exception as e:
            print (str(e), '\nExit . . .\n')
            break

recvThread = threading.Thread(target=recv)
recvThread.start()

def flying():
    global commandList
    print("Начинаю полёт, команды ")
    print(commandList)
    global isOk
    count = 0
    try:
        while True:
            if isOk == True:
                isOk = False
                sock.sendto(commandList[count].encode(encoding="utf-8"), tello_address)
                count += 1
                print("Команда " + str(count) + " из " + str(len(commandList)))
                #if count == 1 or count == 2:
                #   isOk = True
    except:
        print("stipping...")

def starting(commands):
    global commandList
    commandList = commands
    flying()


#sock.sendto("command".encode(encoding="utf-8"), tello_address)
#print("Отправил : Начало")
#time.sleep(5)
# Takeoff
#sock.sendto("takeoff".encode(encoding="utf-8"), tello_address)
#print("Отправил : Взлёт")
#sock.sendto("forward 20".encode(encoding="utf-8"), tello_address)
#print("Отправил : Вперёд 20")
# Land
#sock.sendto("land".encode(encoding="utf-8"), tello_address)
#print("Отправил : Посадка")

def loadingCommands():
    with open('example.txt') as f:
        commandList = f.read().splitlines()
    print(commandList)
#loadingCommands()
#flying()