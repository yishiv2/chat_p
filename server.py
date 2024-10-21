import socket


host = 'localhost'
port = 8080


#AF_INETはIPv4,SOCK_STREAMはTCP接続,(UDP接続をしたい場合はSOCK_DGRAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#サーバーのホストとポート番号にソケットをバインド
s.bind((host, port))

#ソケットをクライアントのリクエストを待つ状態にする
s.listen(1)
print("サーバー起動中...")
#サーバーがクライアントのリクエストを受け入れ、接続を確立したときに処理
conn, addr = s.accept()

#サーバーがクライアントに送信するメッセージを設定
message = "Hey, やあ."
conn.send(message.encode())
conn.close()
