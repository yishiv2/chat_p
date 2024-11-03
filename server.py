import socket
from threading import Thread

class ChatServer:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.clients = {}
        self.addresses = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

    def start(self):
        self.server_socket.listen(5)
        print("サーバー稼働中...")
        try:
            accept_thread = Thread(target=self.accept_client_connections)
            accept_thread.start()
            accept_thread.join()
        except KeyboardInterrupt:
            print("サーバーを停止します...")
            self.server_socket.close()

    def accept_client_connections(self):
        while True:
            client_conn, client_address = self.server_socket.accept()
            print(f"{client_address} と接続")
            client_conn.send(bytes("ようこそ chatroom へ。名前を入力してください", "utf8"))
            self.addresses[client_conn] = client_address
            Thread(target=self.handle_client, args=(client_conn,)).start()

    def handle_client(self, conn):
        name = self.receive_name(conn)
        if name:
            welcome_message = f"ようこそ {name}さん！(終了時は#quitを入力してください)"
            conn.send(bytes(welcome_message, "utf8"))
            self.broadcast(f"{name} がチャットに参加しました。")
            self.clients[conn] = name

            while True:
                msg = conn.recv(1024)
                if msg == bytes("#quit", "utf8"):
                    conn.send(bytes("#quit", "utf8"))
                    conn.close()
                    del self.clients[conn]
                    self.broadcast(f"{name} が去りました。")
                    break
                else:
                    self.broadcast(msg, f"{name}: ")

    def receive_name(self, conn):
        while True:
            name = conn.recv(1024).decode("utf8").strip()
            if not name or any(c in name for c in "!@#$%^&*()"):
                conn.send(bytes("無効な名前です。別の名前を入力してください。", "utf8"))
            else:
                return name

    def broadcast(self, msg, prefix=""):
        for client in self.clients:
            client.send(bytes(prefix, "utf8") + msg if isinstance(msg, bytes) else bytes(prefix + msg, "utf8"))

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()
