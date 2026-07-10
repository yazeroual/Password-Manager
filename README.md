# Password-Manager
A command-line password manager built with Python. Encrypts and stores passwords securely using a master password and SHA-256 hashing. Features add, view, update, delete, and list functionality with JSON storage.


#  Password Manager

A command-line password manager built with Python. Encrypts and stores passwords securely using a master password.

##  Features

-  **Master password protection** – One master password to unlock everything
-  **Encryption** – XOR encryption with base64 encoding
-  **Add entries** – Save usernames, passwords, and optional notes
-  **View entries** – Decrypt and display stored passwords
-  **Update entries** – Modify existing credentials
-  **Delete entries** – Remove stored passwords
-  **List entries** – View all saved entry names
-  **JSON storage** – Data persists in `passwords.json`

##  Technologies

- Python 3
- `hashlib` – SHA-256 hashing for master password
- `base64` – Encoding for encrypted data
- `getpass` – Secure password input (hidden text)
- `json` – File storage

## 🚀 How to Run

```bash
python password_manager.py
