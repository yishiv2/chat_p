import tkinter
import socket
from tkinter import *
from threading import Thread

class ChatClient:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        # GUIの初期化
        self.window = Tk()
        self.window.title("Chat Room Application")
        self.my_msg = StringVar()
        self.my_msg.set("")
        self.create_gui()
        
        # ユーザー名の取得
        self.ask_username()

        # 受信スレッドの開始
        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def create_gui(self):
        message_frame = Frame(self.window, bg="red")
        message_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        scrollbar = Scrollbar(message_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.msg_list = Listbox(message_frame, height=15, width=100, bg="blue", yscrollcommand=scrollbar.set)
        self.msg_list.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.msg_list.yview)

        entry_field = Entry(self.window, textvariable=self.my_msg, fg='red')
        entry_field.grid(row=1, column=0, sticky="ew")
        send_button = Button(self.window, text="Send", font="Arial", fg="black", command=self.send)
        send_button.grid(row=1, column=1)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

    def ask_username(self):
        username_window = Toplevel(self.window)
        username_window.title("ユーザー名の入力")
        username_label = Label(username_window, text="ユーザー名を入力してください:")
        username_label.pack()
        username_entry = Entry(username_window)
        username_entry.pack()

        def submit_username():
            username = username_entry.get()
            self.client_socket.send(bytes(username, "utf8"))
            username_window.destroy()

        submit_button = Button(username_window, text="送信", command=submit_username)
        submit_button.pack()

        self.window.wait_window(username_window)  # ウィンドウが閉じるまで待機

    def receive(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode("utf8")
                self.msg_list.insert(tkinter.END, msg)
            except Exception as e:
                print("受信エラー:", e)
                break

    def send(self):
        msg = self.my_msg.get()
        self.my_msg.set("")
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "#quit":
            self.client_socket.close()
            self.window.destroy()

    def on_closing(self):
        self.my_msg.set("#quit")
        self.send()

if __name__ == "__main__":
    chat_client = ChatClient()
