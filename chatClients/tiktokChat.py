import threading
import queue
from chatClients.base import ClientBase
from utils.logger import Logger
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, ConnectEvent

class TikTokChat():
    def __init__(self, username: str):
        self.username = username
        self.client = TikTokLiveClient(unique_id=username)
        self.message_queue = queue.Queue()
        self.thread = None
        self.commands = {
            "!speak": self.queueMessage("!speak"),
            "!say": self.queueMessage("!say"),
            "!talk": self.queueMessage("!talk"),
            "!dice": self.queueMessage("!dice")
        }

        @self.client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            print(f"[TikTokChat] Connected to TikTok Live chat for user: {self.username}")

        @self.client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            try:
                user = event.user.nickname
                message = event.comment
                print(f"\033[1;32m[TikTok]\033[1;37m {user}:\033[0m {message}")
            except Exception as e:
                Logger.addToLog("error",f"Error processing comment: {e}")

    def startReading(self):
        def runner():
            try:
                self.client.run()
            except Exception as e:
                Logger.addToLog("error",f"Error starting TikTok client: {e}")
        self.thread = threading.Thread(target=runner, daemon=True)
        self.thread.start()
    
    def stopReading(self):
        Logger.addToLog("info", "TikTok stop requested (manual exit required).")

    def getMessageQueue(self):
        return self.message_queue
    
    def queueMessage(self, cmd):
        return lambda u, m: self.messageQueue.put((u, m[len(cmd):].strip()))