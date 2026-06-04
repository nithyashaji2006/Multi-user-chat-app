import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext
import time

HOST = "127.0.0.1"
PORT = 5000

# ========================= SERVER =========================

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server started...")

    clients = {}

    def broadcast_user_list():
        users = "USERS|" + ",".join(clients.keys())

        for conn in clients.values():
            try:
                conn.send(users.encode())
            except:
                pass

    def handle_client(conn):
        try:
            username = conn.recv(1024).decode()
            clients[username] = conn

            print(username, "joined")

            broadcast_user_list()

            while True:
                message = conn.recv(1024).decode()

                if not message:
                    break

                if message.startswith("TO|"):
                    _, receiver, text, timestamp = message.split("|", 3)

                    if receiver in clients:
                        try:
                            clients[receiver].send(
                                f"{username}|{text}|{timestamp}".encode()
                            )
                        except:
                            pass

        except:
            pass

        finally:
            for user, connection in list(clients.items()):
                if connection == conn:
                    del clients[user]

            broadcast_user_list()
            conn.close()

    while True:
        conn, _ = server.accept()

        threading.Thread(
            target=handle_client,
            args=(conn,),
            daemon=True
        ).start()


# ========================= CLIENT =========================

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    root = tk.Tk()
    root.withdraw()

    username = simpledialog.askstring("Username", "Enter username:")
    chat_file = f"{username}_chat.txt"
    sock.send(username.encode())

    root.deiconify()
    root.title(f"Chat - {username}")
    root.geometry("520x650")

    # ================= CHAT AREA =================

    chat_area = scrolledtext.ScrolledText(
        root,
        width=65,
        height=20,
        wrap="word",
        font=("Segoe UI Emoji", 11)
    )

    chat_area.pack(padx=10, pady=10)
    chat_area.config(state="disabled")

    # Left side message
    chat_area.tag_configure(
        "left",
        justify="left",
        background="#f0f0f0",
        lmargin1=10,
        lmargin2=10,
        rmargin=120,
        spacing3=5
    )

    # Right side message
    chat_area.tag_configure(
        "right",
        justify="right",
        background="#cce5ff",
        lmargin1=120,
        lmargin2=120,
        rmargin=10,
        spacing3=5
    )

    # Timestamp style
    chat_area.tag_configure(
        "time",
        font=("Arial", 8),
        foreground="gray"
    )

    # ================= USER LIST =================

    tk.Label(
        root,
        text="Select Users (Ctrl+Click for multiple):"
    ).pack()

    receiver_listbox = tk.Listbox(
        root,
        selectmode="multiple",
        height=6
    )

    receiver_listbox.pack(fill="x", padx=10)

    # ================= MESSAGE ENTRY =================

    message_entry = tk.Entry(
        root,
        width=65,
        font=("Segoe UI Emoji", 11)
    )

    message_entry.pack(padx=10, pady=5)

    # ================= EMOJI PANEL =================

    emoji_list = [
        "😊","😂","🤣","❤️","🔥","👍","😍","😭",
        "😎","😢","😁","😅","🙌","🎉","💯",
        "🥲","🤔","😴","😡","🤝","💖","✨",
        "😇","🤩","🥳","😌","😜","😬","🤗"
    ]

    def add_emoji(emoji):
        message_entry.insert(tk.END, emoji)

    def open_emoji_panel():
        emoji_window = tk.Toplevel(root)
        emoji_window.title("Emoji Panel")
        emoji_window.geometry("300x220")

        row = 0
        col = 0

        for emoji in emoji_list:
            btn = tk.Button(
                emoji_window,
                text=emoji,
                font=("Segoe UI Emoji", 12),
                width=4,
                command=lambda e=emoji: add_emoji(e)
            )

            btn.grid(row=row, column=col, padx=5, pady=5)

            col += 1

            if col == 5:
                col = 0
                row += 1

    # ================= UPDATE USERS =================

    def update_users(user_list):
        receiver_listbox.delete(0, tk.END)

        for user in user_list:
            if user != username:
                receiver_listbox.insert(tk.END, user)

    # ================= INSERT MESSAGE =================

    def insert_message(text, timestamp, side):
        chat_area.config(state="normal")

        chat_area.insert(tk.END, text + "\n", side)
        chat_area.insert(tk.END, timestamp + "\n\n", ("time", side))

        with open(chat_file, "a", encoding="utf-8") as file:
            file.write(f"{text} ({timestamp})\n")

        chat_area.config(state="disabled")
        chat_area.yview(tk.END)
        try:
            with open(chat_file, "r", encoding="utf-8") as file:
                old_chats = file.readlines()

            chat_area.config(state="normal")

            for line in old_chats:
             chat_area.insert(tk.END, line)

            chat_area.config(state="disabled")

        except FileNotFoundError:
            pass

        # Auto scroll to latest message
        chat_area.yview(tk.END)

    # ================= RECEIVE MESSAGE =================

    def receive_messages():
        while True:
            try:
                message = sock.recv(1024).decode()

                if not message:
                    break

                if message.startswith("USERS|"):
                    users = message.split("|")[1].split(",")
                    update_users(users)

                else:
                    sender, text, timestamp = message.split("|", 2)

                    insert_message(
                        f"{sender}: {text}",
                        timestamp,
                        "left"
                    )

            except:
                break

    # ================= SEND MESSAGE =================

    def send_message():
        selected_indices = receiver_listbox.curselection()
        text = message_entry.get()

        if not selected_indices or text == "":
            return

        timestamp = time.strftime("%H:%M")

        for index in selected_indices:
            receiver = receiver_listbox.get(index)

            data = f"TO|{receiver}|{text}|{timestamp}"
            sock.send(data.encode())

        insert_message(text, timestamp, "right")

        message_entry.delete(0, tk.END)

    # ================= BUTTONS =================

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    emoji_button = tk.Button(
        button_frame,
        text="😀 Emoji",
        font=("Arial", 10),
        command=open_emoji_panel
    )

    emoji_button.pack(side="left", padx=10)

    send_button = tk.Button(
        button_frame,
        text="Send",
        font=("Arial", 10),
        width=10,
        command=send_message
    )

    send_button.pack(side="left", padx=10)

    # ================= THREAD =================

    threading.Thread(
        target=receive_messages,
        daemon=True
    ).start()

    root.mainloop()


# ========================= ENTRY =========================

role = input("Type 'server' or 'client': ").strip().lower()

if role == "server":
    start_server()
else:
    start_client()