import socket
import threading
import tkinter as tk
import tkinter.simpledialog
import tkinter.messagebox

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = ""

        # GUI has been implemented below
        self.root = tk.Tk()
        self.root.title("Chat308")

        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack(pady=10)

        self.message_scroll = tk.Scrollbar(self.message_frame)
        self.message_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_list = tk.Listbox(self.message_frame, width=100, height=40, yscrollcommand=self.message_scroll.set)
        self.message_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.message_scroll.config(command=self.message_list.yview)

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=20)

        self.message_entry = tk.Entry(self.entry_frame, width=70)
        self.message_entry.pack(side=tk.LEFT)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.exit_button = tk.Button(self.entry_frame, text="Exit Chat", command=self.exit_chat)
        self.exit_button.pack(side=tk.LEFT)

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        self.nickname = self.get_nickname()
        self.client_socket.send(self.nickname.encode())

        # Start receiving messages in a separate thread
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.root.mainloop()

    def get_nickname(self):
        nickname = tk.simpledialog.askstring("Nickname", "Enter your nickname:")
        if nickname:
            return nickname
        else:
            self.root.destroy()
            return None

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client_socket.send(message.encode())
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                self.message_list.insert(tk.END, message)
                self.message_list.yview(tk.END)
            except:
                tk.messagebox.showerror("Error", "Connection closed.")
                self.client_socket.close()
                break
    
    def exit_chat(self):
        if tk.messagebox.askokcancel("Exit Chat", "Are you sure you want to exit the chat?"):
            self.client_socket.send("exit".encode())
            self.client_socket.close()
            self.root.destroy()          
    
    def close(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.client_socket.close()
            self.root.destroy()

#Run the client
client = Client('localhost', 8000)
client.connect()
