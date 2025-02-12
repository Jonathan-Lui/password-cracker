import hashlib
import itertools
from hashlib import md5


# Function to hash a password using MD5
def md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

# Brute-force attack with lowercase letters
def brute_force(target_hash, charset="abcdefghijklmnopqrstuvwxyz", max_length=6):
    for length in range(1, max_length + 1):
        for attempt in itertools.product(charset, repeat=length):
            attempt = ''.join(attempt)
            if md5_hash(attempt) == target_hash:
                return attempt  # Password found!
    return None  # No match found

# Target hash
target_hash = "5f4dcc3b5aa765d61d8327deb882cf99"

# Run brute-force attack
password = brute_force(target_hash)
print(f"Cracked Password: {password}" if password else "Password not found.")