import socket
import random
import time

bufferSize  = 1024
serverAddressPort   = ("127.0.0.1", 7500)
clientAddressPort   = ("127.0.0.1", 7501)

print('This program will generate some test traffic for 2 players on the red')
print('team as well as 2 players on the green team')
print('')

red1 = input('Enter equipment id of red player 1 ==> ')
red2 = input('Enter equipment id of red player 2 ==> ')
green1 = input('Enter equipment id of green player 1 ==> ')
green2 = input('Enter equipment id of green player 2 ==> ')

# Create datagram sockets
UDPServerSocketReceive = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocketTransmit = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# bind server socket
UDPServerSocketReceive.bind(serverAddressPort)

# wait for start from game software
print("\nWaiting for start from game_software...")

received_data = ' '
while received_data != '202':
    received_data, address = UDPServerSocketReceive.recvfrom(bufferSize)
    received_data = received_data.decode('utf-8')
    print("Received from game software: " + received_data)
print('')

# create events, random player and order
counter = 0

while True:
    if counter == 5:
        message = f"{red1}:{red2}"  # friendly fire red
    elif counter == 15:
        message = f"{green2}:{green1}"  # friendly fire green
    elif counter == 10:
        message = f"{red1}:43"  # base hit
    elif counter == 20:
        message = f"{green2}:53"  # base hit
    else:
        redplayer = red1 if random.randint(1, 2) == 1 else red2
        greenplayer = green1 if random.randint(1, 2) == 1 else green2
        if random.randint(1, 2) == 1:
            message = f"{redplayer}:{greenplayer}"
        else:
            message = f"{greenplayer}:{redplayer}"

    print("Transmitting to game: " + message)
    UDPClientSocketTransmit.sendto(message.encode(), clientAddressPort)

    received_data, address = UDPServerSocketReceive.recvfrom(bufferSize)
    received_data = received_data.decode('utf-8')
    print("Received from game software: " + received_data + "\n")

    counter += 1
    if received_data == '221':
        break
    time.sleep(random.randint(1, 3))

print("Program complete.")
