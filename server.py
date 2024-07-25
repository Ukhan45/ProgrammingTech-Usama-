import socket
import threading
import sqlite3
import os

# Ensure the data directory exists
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
os.makedirs(data_dir, exist_ok=True)

# Construct the absolute path for the database file
db_path = os.path.join(data_dir, 'chat_logs.db')

# Debugging: Print the database path to verify it
print(f"Database path: {db_path}")

# Database setup
try:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, username TEXT, message TEXT)''')
    conn.commit()
    print("Database connected and table created successfully.")
except sqlite3.Error as e:
    print(f"Database error: {e}")
    conn = None

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen()

clients = []
usernames = []

def broadcast(message, client):
    for cl in clients:
        if cl != client:
            try:
                cl.send(message)
            except socket.error as e:
                print(f"Error sending message to {cl}: {e}")
                clients.remove(cl)
                cl.close()

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
            
            # Save message to database
            try:
                username, msg = message.decode().split(": ", 1)
                if conn:
                    c.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, msg))
                    conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except ValueError:
                print("Message format error")
        except socket.error as e:
            print(f"Socket error: {e}")
            break

    remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        username = usernames[index]
        clients.remove(client)
        usernames.remove(username)
        broadcast(f'{username} left the chat!'.encode('utf-8'), client)
        client.close()
        print(f"{username} has been removed and socket closed.")

def receive():
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            client.send('USERNAME'.encode('utf-8'))
            username = client.recv(1024).decode('utf-8')
            usernames.append(username)
            clients.append(client)

            print(f"Username of the client is {username}")
            broadcast(f"{username} joined the chat!".encode('utf-8'), client)
            client.send("Connected to the server!".encode('utf-8'))

            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        except socket.error as e:
            print(f"Socket error during accept: {e}")

print("Server is listening...")
receive()
