import json
import subprocess
import socket

NETWORK_PREFIX = "192.168.1." 
START_IP = 1
END_IP = 10

def ping_device(ip):
    """Teste si l'appareil est en ligne"""
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False

def get_hostname(ip):
    """Récupère le nom de l'hôte si disponible"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Inconnu"

def scan_network():
    appareils = []
    for i in range(START_IP, END_IP + 1):
        ip = NETWORK_PREFIX + str(i)
        en_ligne = ping_device(ip)
        appareil = {
            "name": get_hostname(ip),
            "ip": ip,
            "status": "Online" if en_ligne else "Offline"
        }
        appareils.append(appareil)
    return appareils

def save_to_json(appareils, filename="data/database.json"):
    data = {
        "Inventory": appareils,
        "Maintenance": [],
        "Vendors": []
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[✔] Les données ont été sauvegardées dans {filename}")

if __name__ == "__main__":
    print("[✓] Analyse du réseau en cours...")
    appareils = scan_network()
    save_to_json(appareils)
