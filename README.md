# Password Cracker with FastAPI

This is a FastAPI-based password hashing and cracking tool that supports:
- **MD5 hashing**
- **Brute-force password cracking**
- **Wordlist-based password cracking**
- **Real-time status updates via WebSockets(In Progress)**

## Features
- Hash a given password using MD5.
- Crack an MD5 hash using brute force (with a customizable max length).
- Crack an MD5 hash using a predefined wordlist.
- Live status updates via WebSockets during brute force attempts.
- Simple HTML interface with JavaScript to display status updates.

## Installation
### 1. Clone the repository
```bash
git clone https://github.com/Jonathan-Lui/password-cracker
cd password-cracker
```

### 2. Install dependencies
Make sure you have Python installed, then install FastAPI and Uvicorn:
```bash
pip install fastapi uvicorn
```

## Usage
### 1. Run the FastAPI server
```bash
uvicorn main:app --reload
```

### 2. Access the endpoints
- Open your browser and go to: `http://127.0.0.1:8000/` to see the basic UI.
- Use the following API endpoints:
  - `POST /hash/md5` → Hash a password.
  - `POST /crack/wordlist` → Crack a password using a wordlist.
  - `POST /crack/bruteforce` → Crack a password via brute force.
  - `WS /crack/ws` → Live password guessing updates via WebSockets.

