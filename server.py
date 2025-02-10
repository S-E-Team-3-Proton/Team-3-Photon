import socket
import json

# Load config options from json file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

localIP = config["network_address"]
localPort = config["server_port"]
bufferSize = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print(f"UDP server up and listening on {localIP}:{localPort}")

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = f"Message from Client: {message.decode()}"
    clientIP = f"Client IP Address: {address}"

    print(clientMsg)
    print(clientIP)

    UDPServerSocket.sendto(bytesToSend, address)
