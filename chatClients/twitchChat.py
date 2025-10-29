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

    def __init__(self, server: str, port: int, nickname: str, token: str, channel: str, sourceRoom: str):
        self.server = server
        self.port = port
        self.nickname = nickname
        self.token = token
        self.channel = channel if channel.startswith("#") else f"#{channel}"
        self.sourceRoom = sourceRoom
        self.sock = socket.socket()
        self.messageQueue = queue.Queue()
        self.stopEvent = threading.Event()
        self.commands ={
            "!speak": self.queueMessage("!speak"),
            "!say": self.queueMessage("!say"),
            "!talk": self.queueMessage("!talk"),
            "!dice": self.queueMessage("!dice"),
            "!id": self.sendNickname(),
            "!nick": self.sendNickname(),
            "!username": self.sendNickname(),
        }
    
    def connect(self):
        self.sock.connect((self.server, self.port))
        self.sock.send(f"PASS {self.token}\r\n".encode('utf-8'))
        self.sock.send(f"NICK {self.nickname}\r\n".encode('utf-8'))
        self.sock.send(f"JOIN {self.channel}\r\n".encode('utf-8'))
        self.sock.send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8"))

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
                        if not self.verifySourceRoom(line):
                            continue
                        try:
                            if line.startswith("@"):
                                line = line.split(" ", 1)[1]
                            prefix, rest = line.split(" PRIVMSG ", 1)
                            user = prefix.split('!', 1)[0][1:]
                            message = rest.split(':', 1)[1].strip()
                            print(f"\033[1;35m[Twitch]\033[1;37m {user}:\033[0m {message}")
                            for cmd, action in self.commands.items():
                                if message.startswith(cmd):
                                    action(user, message)
                                    break
                        except Exception as e:
                            Logger.addToLog("error", f"Error parsing message: {line} - {e}")
                    else:
                        print(f"{line.strip()}")
            except Exception as e:
                Logger.addToLog("error", f"Error in readMessages: {e}")
    
    def sendMessage(self, message: str):
        self.sock.send(f"PRIVMSG {self.channel} :{message}\r\n".encode('utf-8'))

    def verifySourceRoom(self, line: str,) -> bool:
        if not line.startswith("@"):
            return False
        tags = line.split(" ", 1)[0][1:].split(";")
        for tag in tags:
            k,_,v = tag.partition("=")
            if k == "source-room-id":
                return v == self.sourceRoom
        return True
    
    def queueMessage(self, cmd):
        return lambda u, m: self.messageQueue.put((u, m[len(cmd):].strip()))
    
    def sendNickname(self, cmd=None):
        return lambda u, m: self.sendMessage(f"@{u}, Fortnite ID: Ammi_Wang - Roblox ID: awa457456")