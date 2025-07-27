import json
import socket
import threading
import subprocess
from queue import Queue
from datetime import datetime

NETWORK_PREFIX = "192.168.1."
START_IP = 1
END_IP = 254
THREADS = 50

results = []
queue = Queue()

def ping_and_check(ip):
    """Ping device and get hostname if available."""
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL)
        status = "Online" if result.returncode == 0 else "Offline"
    except Exception:
        status = "Offline"

    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except:
        hostname = "Unknown"

    results.append({
        "name": hostname,
        "ip": ip,
        "status": status,
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status == "Online" else None
    })

def worker():
    """Thread worker function."""
    while not queue.empty():
        ip = queue.get()
        ping_and_check(ip)
        queue.task_done()

def scan_network():
    """Scan IP range with multithreading."""
    for i in range(START_IP, END_IP + 1):
        ip = NETWORK_PREFIX + str(i)
        queue.put(ip)

    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    queue.join()
    for t in threads:
        t.join()

    return results

def save_to_json(data, filename="data/database.json"):
    """Save result to JSON file."""
    json_data = {
        "Inventory": data
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    print(f"[✔] Data saved to {filename}")

if __name__ == "__main__":
    print("[✓] Scanning network...")
    data = scan_network()
    save_to_json(data)
