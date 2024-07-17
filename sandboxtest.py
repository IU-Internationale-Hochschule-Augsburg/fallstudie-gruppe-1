import requests
import json
import time

# URL und Header-Informationen
url = "https://api.jsonbin.io/v3/b/666b25ece41b4d34e402d580"
headers = {
    'X-Master-Key': '$2a$10$cVDLXTLgbT6IpIZ0.BIzjOEn1DB8asJ5DJPvN50x4yUaqqLVbbA9i',
    'X-Access-Key': '$2a$10$OQgJlnn2vFFKzzlf9NnylOk4lJ2/z1ElhD4c9DFWYAinDr7hszxCa',
    'Content-Type': 'application/json'
}

def get_data():
    # Anforderung senden
    response = requests.get(url, headers=headers)

    # Status und Daten ausgeben
    if response.status_code == 200:
        data = response.json()
        print("Verbindung erfolgreich!")
        
        # Daten extrahieren
        record = data.get('record', {})
        while 'record' in record:
            record = record['record']
        
        print("Daten:", json.dumps(record, indent=4))
    else:
        print(f"Fehler bei der Verbindung: {response.status_code}")

def send_data(new_data):
    # Daten senden
    response = requests.put(url, headers=headers, json={"record": new_data})

    # Status prüfen
    if response.status_code == 200:
        print("Daten erfolgreich gesendet!")
    else:
        print(f"Fehler beim Senden der Daten: {response.status_code}")

def validate_data(data):
    try:
        assert "Zumo" in data
        assert "Object" in data
        assert isinstance(data["Zumo"]["positionZumo"], list) and len(data["Zumo"]["positionZumo"]) == 4
        assert isinstance(data["Zumo"]["facing"], list) and len(data["Zumo"]["facing"]) == 2
        assert isinstance(data["Object"]["positionObject"], list) and len(data["Object"]["positionObject"]) == 4
    except AssertionError:
        return False
    return True

if __name__ == "__main__":
    get_data()

    # Neue Daten definieren
    new_data = {
        "Zumo": {
            "positionZumo": [100, 150, 50, 50],
            "facing": [1, 0]
        },
        "Object": {
            "positionObject": [200, 250, 100, 100]
        }
    }

while True:
    if validate_data(new_data):
        send_data(new_data)
        get_data()  # Um die neuen Daten zu überprüfen
    else:
        print("Die Datenstruktur ist ungültig.")
    
    time.sleep(1)
