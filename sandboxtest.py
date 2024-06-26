import requests

# URL und Header-Informationen
url = "https://api.jsonbin.io/v3/b/666b25ece41b4d34e402d580"
headers = {
    'X-Master-Key': '$2a$10$cVDLXTLgbT6IpIZ0.BIzjOEn1DB8asJ5DJPvN50x4yUaqqLVbbA9i',
    'X-Access-Key': '$2a$10$OQgJlnn2vFFKzzlf9NnylOk4lJ2/z1ElhD4c9DFWYAinDr7hszxCa'
}

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
    
    print("Daten:", record)
else:
    print(f"Fehler bei der Verbindung: {response.status_code}")

if __name__ == "__main__":
    # Sicherstellen, dass der Code nur ausgeführt wird, wenn das Skript direkt aufgerufen wird
    pass
