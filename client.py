import socket
import threading
import tkinter
from tkinter import simpledialog, filedialog, messagebox
import emoji
import os

HOST = 'localhost'
PORT = 5555

class Client:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Application")
        self.socket = None  

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to server: {e}")
            self.master.destroy()
            return

        self.username_prompt()
        self.gui_setup()

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def username_prompt(self):
        self.username = simpledialog.askstring("Username", "Please choose a username", parent=self.master)
        if self.username:
            try:
                self.socket.send(self.username.encode('utf-8'))
            except Exception as e:
                messagebox.showerror("Send Error", f"Failed to send username: {e}")
                self.master.destroy()

    def gui_setup(self):
        self.text_area = tkinter.Text(self.master, wrap='word', font=('Arial', 12))
        self.text_area.pack(padx=20, pady=5)

        self.input_frame = tkinter.Frame(self.master)
        self.input_frame.pack(padx=20, pady=5)

        self.input_area = tkinter.Entry(self.input_frame, width=50, font=('Arial', 12))
        self.input_area.grid(row=0, column=0, padx=5, pady=5)
        self.input_area.bind("<Return>", self.write)

        self.send_button = tkinter.Button(self.input_frame, text="Send", command=self.write_button, font=('Arial', 12))
        self.send_button.grid(row=0, column=1, padx=5, pady=5)

        self.emoji_button = tkinter.Button(self.input_frame, text="😀", command=self.send_emoji, font=('Arial', 12))
        self.emoji_button.grid(row=0, column=2, padx=5, pady=5)

        self.attach_button = tkinter.Button(self.input_frame, text="Attach", command=self.attach_file, font=('Arial', 12))
        self.attach_button.grid(row=0, column=3, padx=5, pady=5)

    def send_emoji(self):
        emoji_window = tkinter.Toplevel(self.master)
        emoji_window.title("Select Emoji")

        emojis = ["😀", "😂", "😍", "😭", "😠", "😎", "👍", "🙏"]

        for em in emojis:
            button = tkinter.Button(emoji_window, text=em, command=lambda em=em: self.add_emoji(em, emoji_window), font=('Arial', 12))
            button.pack(side=tkinter.LEFT, padx=5, pady=5)

    def add_emoji(self, em, emoji_window):
        self.input_area.insert(tkinter.END, em)
        emoji_window.destroy()

    def write(self, event=None):
        self.send_message()

    def write_button(self):
        self.send_message()

    def send_message(self):
        message = self.input_area.get()
        if message.strip():  
            try:
                if self.socket:
                    self.socket.send(message.encode('utf-8'))
                else:
                    messagebox.showerror("Send Error", "Socket is not connected.")
            except socket.error as e:
                messagebox.showerror("Send Error", f"Failed to send message: {e}")
                return

            self.input_area.delete(0, tkinter.END)

    def receive(self):
        while True:
            try:
                if self.socket:
                    message = self.socket.recv(1024).decode('utf-8')
                    if not message:
                        break  
                    self.text_area.insert(tkinter.END, message + "\n")
            except socket.error as e:
                messagebox.showerror("Receive Error", f"Error receiving message: {e}")
                break

        if self.socket:
            self.socket.close()

    def attach_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                filename = os.path.basename(file_path)
                with open(file_path, 'rb') as file:
                    file_data = file.read()

                if self.socket:
                    self.socket.send(f"{self.username}: [File: {filename}]".encode('utf-8'))
                    self.socket.send(file_data)
                else:
                    messagebox.showerror("Error", "Socket is not connected.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to attach file: {e}")

root = tkinter.Tk()
client = Client(root)
root.mainloop()
