# Multi-User Chat Application

A real-time chat application built using Python, Socket Programming, Threading, and Tkinter. The application allows multiple users to communicate through a central server, supports emoji messaging, chat history persistence, and local network (LAN) communication.

## Features

- Real-time messaging using TCP sockets
- Multi-user communication through a central server
- Multiple recipient selection
- Emoji picker panel
- Persistent chat history
- Automatic chat history restoration on restart
- Left and right message alignment similar to modern messaging applications
- Dynamic online user list
- LAN-based communication support (same network)
- Graphical User Interface (GUI) using Tkinter
- Concurrent client handling using threading

## Architecture

Client A
↓
Server
↓
Client B

### Message Flow

Sender Client
↓
Server
↓
Selected Receiver(s)

The server acts as a mediator between clients, managing user connections, message routing, and user list updates.

## Tech Stack

| Layer       | Technology                   |
| ----------- | ---------------------------- |
| Language    | Python                       |
| Networking  | Socket Programming (TCP)     |
| GUI         | Tkinter                      |
| Concurrency | Threading                    |
| Storage     | Text File-based Chat History |

## Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd Multi-User-Chat-App
```

### 2. Run the Application

```bash
python pyt_pro.py
```

### 3. Start Server

```text
server
```

### 4. Start Client(s)

Open another terminal and run:

```bash
python pyt_pro.py
```

Then enter:

```text
client
```

Enter a username and start chatting.

## Project Structure

```text
Multi-User-Chat-App/
├── pyt_pro.py
├── README.md
```

## Future Improvements

- Message editing
- Message deletion
- File sharing
- Group chat support
- User authentication
- Internet-based communication

## Learning Outcomes

This project demonstrates:

- Client-Server Architecture
- TCP Socket Programming
- Multi-threaded Programming
- GUI Development with Tkinter
- Real-time Communication Systems
- Local Network Communication
- File Handling and Data Persistence
- Debugging and Feature Enhancement

```

```
