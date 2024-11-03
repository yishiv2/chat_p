import socket
from threading import Thread

host = '127.0.0.1'
port = 8080

clients = {}
addresses = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

def handle_clients(conn, address):
    try:
        # 名前の入力を確認するループ
        while True:
            name = conn.recv(1024).decode("utf8").strip()
            if not name or any(c in name for c in "!@#$%^&*()"):
                conn.send(bytes("無効な名前です。別の名前を入力してください。", "utf8"))
            else:
                break

        # クライアントをチャットに参加させる
        welcome = "ようこそ " + name + "さん！(終了時は#quitを入力してください)"
        conn.send(bytes(welcome, "utf8"))
        msg = name + " がチャットに参加しました。"
        broadcast(bytes(msg, "utf8"))
        clients[conn] = name

        # クライアントのメッセージ受信
        while True:
            msg = conn.recv(1024)
            if msg != bytes("#quit", "utf8"):
                broadcast(msg, name + ": ")
            else:
                conn.send(bytes("#quit", "utf8"))
                conn.close()
                del clients[conn]
                broadcast(bytes(name + " が去りました。"), "")
                break

    except ConnectionResetError:
        print(f"{address} との接続が失われました")
        conn.close()
        if conn in clients:
            name = clients.pop(conn)
            broadcast(bytes(name + " が去りました。"), "")

def accept_client_connections():
    while True:
        client_conn, client_address = s.accept()
        print(client_address, "と接続")
        client_conn.send(bytes("ようこそ chatroom へ。名前を入力してください", "utf8"))
        addresses[client_conn] = client_address
        Thread(target=handle_clients, args=(client_conn, client_address)).start()

def broadcast(msg, prefix=""):
    for cli in clients:
        cli.send(bytes(prefix, "utf8") + msg)

if __name__ == "__main__":
    s.listen(5)
    print("サーバー稼働中...")
    try:
        accept_thread = Thread(target=accept_client_connections)
        accept_thread.start()
        accept_thread.join()
    except KeyboardInterrupt:
        print("サーバーを停止します...")
        s.close()
