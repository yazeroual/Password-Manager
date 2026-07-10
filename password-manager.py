import base64
import getpass
import hashlib
import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(__file__), "passwords.json")


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()


def encrypt(text: str, key: bytes) -> str:
    data = text.encode("utf-8")
    encrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return base64.b64encode(encrypted).decode("utf-8")


def decrypt(token: str, key: bytes) -> str:
    encrypted = base64.b64decode(token.encode("utf-8"))
    decrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(encrypted))
    return decrypted.decode("utf-8")


def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def initialize_master(master_key):
    data = {
        "master_hash": hashlib.sha256(master_key).hexdigest(),
        "entries": {}
    }
    save_data(data)
    return data


def verify_master(data, master_key):
    return data.get("master_hash") == hashlib.sha256(master_key).hexdigest()


def add_entry(data, key):
    name = input("Entry name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    note = input("Note (optional): ").strip()
    data["entries"][name] = {
        "username": username,
        "password": encrypt(password, key),
        "note": note
    }
    save_data(data)
    print(f"Saved entry '{name}'.")


def get_entry(data, key):
    name = input("Entry name: ").strip()
    entry = data["entries"].get(name)
    if not entry:
        print("Entry not found.")
        return
    password = decrypt(entry["password"], key)
    print(f"Name: {name}")
    print(f"Username: {entry['username']}")
    print(f"Password: {password}")
    if entry.get("note"):
        print(f"Note: {entry['note']}")


def update_entry(data, key):
    name = input("Entry name: ").strip()
    entry = data["entries"].get(name)
    if not entry:
        print("Entry not found.")
        return
    username = input(f"Username [{entry['username']}]: ").strip() or entry["username"]
    password = getpass.getpass("Password (leave blank to keep current): ")
    if not password:
        password = decrypt(entry["password"], key)
    note = input(f"Note [{entry.get('note', '')}]: ").strip() or entry.get("note", "")
    data["entries"][name] = {
        "username": username,
        "password": encrypt(password, key),
        "note": note
    }
    save_data(data)
    print(f"Updated entry '{name}'.")


def delete_entry(data):
    name = input("Entry name: ").strip()
    if name in data["entries"]:
        del data["entries"][name]
        save_data(data)
        print(f"Deleted entry '{name}'.")
    else:
        print("Entry not found.")


def list_entries(data):
    entries = sorted(data["entries"].keys())
    if not entries:
        print("No entries stored.")
        return
    for name in entries:
        print(f"- {name}")


def main():
    print("Password Manager")
    data = load_data()
    master_password = getpass.getpass("Master password: ")
    master_key = derive_key(master_password)
    if data is None:
        print("No password database found. Creating new one.")
        data = initialize_master(master_key)
    else:
        if not verify_master(data, master_key):
            print("Invalid master password.")
            sys.exit(1)

    while True:
        print("\nOptions: add, get, update, delete, list, quit")
        choice = input("Choose an option: ").strip().lower()
        if choice == "add":
            add_entry(data, master_key)
        elif choice == "get":
            get_entry(data, master_key)
        elif choice == "update":
            update_entry(data, master_key)
        elif choice == "delete":
            delete_entry(data)
        elif choice == "list":
            list_entries(data)
        elif choice in {"quit", "exit"}:
            print("Goodbye.")
            break
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()

