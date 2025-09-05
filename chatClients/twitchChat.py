import threading
import queue
import socket
from chatClients.base import ClientBase
from utils.logger import Logger

class TwitchChat(ClientBase):
    server: str
    port: int
    nickname: str
    token: str
    channel: str
    sock: socket.socket
    messageQueue: queue.Queue
    readingThread: threading.Thread
    stopEvent: threading.Event

    def __init__(self, server: str, port: int, nickname: str, token: str, channel: str):
        self.server = server
        self.port = port
        self.nickname = nickname
        self.token = token
        self.channel = channel if channel.startswith("#") else f"#{channel}"
        self.sock = socket.socket()
        self.messageQueue = queue.Queue()
        self.stopEvent = threading.Event()
    
    def connect(self):
        self.sock.connect((self.server, self.port))
        self.sock.send(f"PASS {self.token}\r\n".encode('utf-8'))
        self.sock.send(f"NICK {self.nickname}\r\n".encode('utf-8'))
        self.sock.send(f"JOIN {self.channel}\r\n".encode('utf-8'))

    def startReading(self):
        self.readingThread = threading.Thread(target=self.readMessages)
        self.readingThread.start()
    
    def stopReading(self):
        self.stopEvent.set()
        if self.readingThread.is_alive():
            self.readingThread.join()
        self.sock.close()

    def readMessages(self):
        buffer = ""
        while True:
            try:
                buffer += self.sock.recv(2048).decode('utf-8')
                lines = buffer.split('\r\n')
                buffer = lines.pop()
                for line in lines:
                    if line.startswith("PING"):
                        self.sock.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
                        print("[TwitchChat] PING recibido, PONG enviado")
                    elif "PRIVMSG" in line:
                        try:
                            user = line.split('!', 1)[0][1:]
                            message = line.split('PRIVMSG', 1)[1].split(':', 1)[1]
                            if message.startswith("!speak"):
                                self.messageQueue.put((user, message.replace("!speak", "", 1)))
                        except Exception as e:
                            print(f"[TwitchChat] Error al parsear mensaje: {line}\n{e}")
                            Logger.addToLog("error", f"Error parsing message: {line} - {e}")
                    else:
                        print(f"[TwitchChat] {line.strip()}")
            except Exception as e:
                print(f"[TwitchChat - Error] {e}")
                Logger.addToLog("error", f"Error in readMessages: {e}")
    
    def sendMessage(self, message: str):
        self.sock.send(f"PRIVMSG {self.channel} :{message}\r\n".encode('utf-8'))