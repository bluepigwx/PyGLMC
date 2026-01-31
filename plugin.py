import socket
import logging
import threading
import json
from collections  import deque

logger = logging.getLogger(__name__)


_host = "localhost"
_port = 9987

class Plugin:
    def __init__(self):
        self.socket = None
        self.commands = deque()
        
        self._cmd_lokcer = threading.Lock()
        
    
    def init(self):
        """
        Docstring for init
        外部init接口
        :param self: Description
        """
        if self.socket != None:
            logger.warning(f"socket not none")
            self.socket.close()
        
        try:
            logger.info(f"try to connect {_host}:{_port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((_host, _port))
        except Exception as e:
            logger.error(f"failed to connect to {_host}:{_port} {e}")
            self.socket = None
            raise Exception(e)
        
        logger.info(f"connect to {_host}:{_port} success")
        
        #开启收包线程
        try:
            self.recv_thread = threading.Thread(target=self._receiv)
            self.recv_thread.daemon = True
            self.recv_thread.start()
        except Exception as e:
            logger.error(f"create thread failed {e}")
            self.socket.close()
            raise Exception(e)
            
        logger.info(f"create receiv threading success")
        
        
    def _push_cmd(self, command):
        with self._cmd_lokcer:
            self.commands.append(command)
            
        
    def _receiv(self):
        self.socket.settimeout(None)
        
        buffer = b''
        
        try:
            while True:
                data = self.socket.recv(8192)
                buffer += data
                
                try:
                    command = json.loads(buffer.decode("utf-8"))
                    self._push_cmd(command)
                    buffer = b''
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    pass
                
        except Exception as e:
            pass
        
        
    def finit(self):
        self.disconnect()
        
    
    def disconnect(self):
        if self.socket != None:
            try:
                self.socket.close()
            except Exception as e:
                logger.error(f"failed to disconnect {e}")
            finally:
                self.socket = None
                
    
    def update(self):
        """
        从commands队列中取出操作在主线程中执行
        """
        cnt = 0
        with self._cmd_lokcer:
            while self.commands:
                cmd = self.commands.popleft()
                
                logger.info(f"process cmd {cmd}")
                self.process_cmd(cmd)
                cnt += 1
                
    
    def _handle_hello(self, params):
        logger.info(f"handle hello message {params}")
    
    
    def process_cmd(self, command):
        hadlers = {
            "hello" :self._handle_hello,
        }
        
        cmd_type = command.get("type")
        cmd_params = command.get("paramas", {})
        
        handler = hadlers.get(cmd_type)
        if handler:
            try:
                handler(cmd_params)
            except Exception as e:
                pass
        else:
            logger.error(f"unkonw command {cmd_type}")
            
    
    