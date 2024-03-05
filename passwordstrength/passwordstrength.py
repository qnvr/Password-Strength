import json
import os
import math
from customtkinter import *

def load_common_passwords(file_name):
    script_dir = os.path.dirname(__file__)  
    file_path = os.path.join(script_dir, file_name)  
    with open(file_path, "r", encoding="utf-8") as f:  
        common_passwords_data = json.load(f)
        return common_passwords_data["passwords"]

def is_common_password(password, common_passwords):
    return password.lower() in common_passwords

def calculate_entropy(password):
    entropy = 0
    total_characters = len(password)
    if total_characters == 0:
        return 0
    
    
    character_counts = {}
    for char in password:
        if char in character_counts:
            character_counts[char] += 1
        else:
            character_counts[char] = 1
    
    for count in character_counts.values():
        probability = count / total_characters
        entropy -= probability * math.log2(probability)
    
    return entropy

def check_password_strength(password, common_passwords):
    if is_common_password(password, common_passwords):
        return "Weak (Common Password)"
    
    length_score = min(len(password) * 4, 100)
    
    entropy = calculate_entropy(password)
    entropy_score = min(math.ceil(entropy * 10), 100)
    
    strength_score = (length_score + entropy_score) / 2
    
    if strength_score < 40:
        return "Weak"
    elif strength_score < 70:
        return "Moderate"
    else:
        return "Strong"

def assess_password_strength():
    password = password_entry.get()
    strength = check_password_strength(password, common_passwords)
    strength_label.configure(text=f"Password strength: {strength}")


common_passwords = load_common_passwords("passwords.json")

app = CTk()
app.title("Password Strength Checker | NVR")

icon_path = os.path.join(os.path.dirname(__file__), "logoo.ico")
app.iconbitmap(icon_path)

app.geometry("400x200")

app.resizable(False, False)

strength_label = CTkLabel(app, text="")
strength_label.pack()

password_label = CTkLabel(app, text="Enter your password:")
password_label.pack()
password_entry = CTkEntry(app, show="*")
password_entry.pack()

check_button = CTkButton(app, text="Check Password Strength", command=assess_password_strength)
check_button.pack(pady=10)  

app.mainloop()
