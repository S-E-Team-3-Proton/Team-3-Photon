import socket
import json

# Load configu from json file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

serverAddress = config["network_address"]
serverPort = config["client_port"]
bufferSize = 1024

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, (serverAddress, serverPort))

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = f"Message from Server: {msgFromServer[0].decode()}"

print(msg)