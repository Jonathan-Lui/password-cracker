from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import hashlib
import string

app = FastAPI()

# Sample wordlist (you can extend this or allow user upload)
sample_wordlist = [
    "password", "123456", "qwerty", "letmein", "welcome",
    "admin", "root", "12345", "monkey", "abc123"
]

# Define the request body model for the password input
class HashRequest(BaseModel):
    text: str

class CrackRequest(BaseModel):
    target_hash: str
    max_length: int

# Step 1: Serve the HTML page
@app.get("/", response_class=HTMLResponse)
def get_homepage():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Cracker</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f7f7f7;
                color: #333;
            }
            .container {
                max-width: 600px;
                margin: 50px auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #333;
            }
            label, button {
                font-size: 16px;
                margin-bottom: 10px;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 16px;
            }
            button {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #45a049;
            }
            .result {
                margin-top: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            .error {
                color: #ff0000;
            }
            .success {
                color: #4CAF50;
            }
            .loading {
                color: #ffa500;
            }
            .btn-container {
                display: flex;
                justify-content: space-between;
            }
            .btn-container button {
                width: 48%;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Password Cracker</h1>
            
            <label for="password">Enter Password:</label>
            <input type="text" id="password" name="password" placeholder="Enter a password to hash">

            <div class="btn-container">
                <button onclick="hashPassword()">Hash Password</button>
                <button onclick="clearResult()">Clear Results</button>
            </div>

            <h3>MD5 Hash:</h3>
            <p id="md5_hash"></p>

            <h3>Cracking Results:</h3>
            <button onclick="bruteForceCrack()">Crack with Brute Force</button>
            <button onclick="wordlistCrack()">Crack with Wordlist</button>
            <p id="crack_result" class="result"></p>
        </div>

        <script>
            function clearResult() {
                document.getElementById("password").value = '';
                document.getElementById("md5_hash").textContent = '';
                document.getElementById("crack_result").textContent = '';
            }

            function hashPassword() {
                const password = document.getElementById('password').value;
                if (password === '') {
                    alert("Please enter a password.");
                    return;
                }
                document.getElementById("crack_result").textContent = "Cracking...";
                fetch("/hash/md5", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ "text": password })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("md5_hash").textContent = data.md5_hash;
                    document.getElementById("crack_result").textContent = "";
                });
            }

            function bruteForceCrack() {
                const password = document.getElementById('password').value;
                if (password === '') {
                    alert("Please enter a password to crack.");
                    return;
                }
                const targetHash = document.getElementById("md5_hash").textContent;
                if (!targetHash) {
                    alert("Please hash a password first.");
                    return;
                }
                document.getElementById("crack_result").textContent = "Cracking with brute force... Please wait.";
                fetch("/crack/bruteforce", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ "target_hash": targetHash, "max_length": 8 })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.password) {
                        document.getElementById("crack_result").textContent = "Cracked Password: " + data.password;
                        document.getElementById("crack_result").className = "result success";
                    } else {
                        document.getElementById("crack_result").textContent = data.message;
                        document.getElementById("crack_result").className = "result error";
                    }
                });
            }

            function wordlistCrack() {
                const password = document.getElementById('password').value;
                if (password === '') {
                    alert("Please enter a password to crack.");
                    return;
                }
                const targetHash = document.getElementById("md5_hash").textContent;
                if (!targetHash) {
                    alert("Please hash a password first.");
                    return;
                }
                document.getElementById("crack_result").textContent = "Cracking with wordlist... Please wait.";
                
                // Assuming a max_length (adjust as needed)
                const maxLength = 4;

                fetch("/crack/wordlist", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ 
                        "target_hash": targetHash, 
                        "max_length": maxLength  // Added max_length here
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.password) {
                        document.getElementById("crack_result").textContent = "Cracked Password: " + data.password;
                        document.getElementById("crack_result").className = "result success";
                    } else {
                        document.getElementById("crack_result").textContent = data.message;
                        document.getElementById("crack_result").className = "result error";
                    }
                });
            }

        </script>
    </body>
    </html>
    """


# Step 2: Endpoint to hash the password
@app.post("/hash/md5")
def hash_md5(request: HashRequest):
    hashed = hashlib.md5(request.text.encode()).hexdigest()
    return {"md5_hash": hashed}

# Step 3: Brute Force Cracking (as before)
def brute_force_crack(target_hash: str, max_length: int):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

    def generate_passwords(length):
        if length == 0:
            return ['']
        else:
            smaller_passwords = generate_passwords(length - 1)
            return [char + smaller for char in characters for smaller in smaller_passwords]
    
    for length in range(1, max_length + 1):
        for password in generate_passwords(length):
            hashed = hashlib.md5(password.encode()).hexdigest()
            if hashed == target_hash:
                return password
    return None

@app.post("/crack/bruteforce")
async def crack_with_bruteforce(request: CrackRequest):
    target_hash = request.target_hash
    max_length = request.max_length  # Get max_length from the request body
    cracked_password = brute_force_crack(target_hash, max_length)  # Pass max_length to the function
    if cracked_password:
        return JSONResponse(content={"password": cracked_password})
    else:
        return JSONResponse(content={"message": "Password not found."}, status_code=400)

# Step 4: Wordlist Cracking
def wordlist_crack(target_hash: str, wordlist: list):
    for word in wordlist:
        hashed = hashlib.md5(word.encode()).hexdigest()
        if hashed == target_hash:
            return word
    return None

@app.post("/crack/wordlist")
async def crack_with_wordlist(request: CrackRequest):
    target_hash = request.target_hash
    cracked_password = wordlist_crack(target_hash, sample_wordlist)  # Pass the wordlist to the function
    if cracked_password:
        return JSONResponse(content={"password": cracked_password})
    else:
        return JSONResponse(content={"message": "Password not found."}, status_code=400)
