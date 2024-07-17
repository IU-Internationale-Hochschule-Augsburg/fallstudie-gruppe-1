import cv2
import numpy as np
import requests
import json
import time
import threading

# URL and header information for the API
url = "https://api.jsonbin.io/v3/b/666b25ece41b4d34e402d580"
headers = {
    'X-Master-Key': '$2a$10$cVDLXTLgbT6IpIZ0.BIzjOEn1DB8asJ5DJPvN50x4yUaqqLVbbA9i',
    'X-Access-Key': '$2a$10$OQgJlnn2vFFKzzlf9NnylOk4lJ2/z1ElhD4c9DFWYAinDr7hszxCa',
    'Content-Type': 'application/json'
}

# Global variables to store object data
positionZumo = "[0, 0, 0, 0]"
positionObject = "[0, 0, 0, 0]"

def nothing(x):
    pass

def get_data():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("Verbindung erfolgreich!")
        record = data.get('record', {})
        while 'record' in record:
            record = record['record']
        print("Daten:", json.dumps(record, indent=4))
    else:
        print(f"Fehler bei der Verbindung: {response.status_code}")

def send_data(new_data):
    response = requests.put(url, headers=headers, json={"record": new_data})
    if response.status_code == 200:
        print("Daten erfolgreich gesendet!")
    else:
        print(f"Fehler beim Senden der Daten: {response.status_code}")

def validate_data(data):
    try:
        assert "Zumo" in data
        assert "Object" in data
        assert isinstance(data["Zumo"]["positionZumo"], str)
        assert isinstance(data["Zumo"]["facing"], list) and len(data["Zumo"]["facing"]) == 2
        assert isinstance(data["Object"]["positionObject"], str)
    except AssertionError:
        return False
    return True

class ObjectTracker:
    def __init__(self, threshold=10, buffer_size=5):  # buffer_size hinzugefügt
        self.threshold = threshold
        self.objects = {}
        self.next_id = 0
        self.buffer_size = buffer_size  # Neuer Pufferbereich
        self.position_buffers = {}  # Position-Puffer

    def update(self, contours):
        global positionZumo, positionObject
        new_objects = {}
        for contour in contours:
            if cv2.contourArea(contour) > self.threshold:
                x, y, w, h = cv2.boundingRect(contour)
                updated = False
                for obj_id, (ox, oy, ow, oh) in self.objects.items():
                    if abs(x - ox) <= self.threshold and abs(y - oy) <= self.threshold:
                        new_objects[obj_id] = (x, y, w, h)
                        updated = True
                        break
                if not updated:
                    new_objects[self.next_id] = (x, y, w, h)
                    self.next_id += 1
        self.objects = new_objects
        self.update_buffers()  # Aktualisieren der Puffer
        self.set_new_data()

    def update_buffers(self):  # Neue Methode zum Aktualisieren der Puffer
        for obj_id, (x, y, w, h) in self.objects.items():
            if obj_id not in self.position_buffers:
                self.position_buffers[obj_id] = []
            self.position_buffers[obj_id].append((x, y, w, h))
            if len(self.position_buffers[obj_id]) > self.buffer_size:
                self.position_buffers[obj_id].pop(0)

    def get_smoothed_position(self, obj_id):  # Neue Methode zur Berechnung der geglätteten Position
        buffer = self.position_buffers.get(obj_id, [])
        if not buffer:
            return 0, 0, 0, 0
        avg_x = sum(b[0] for b in buffer) // len(buffer)
        avg_y = sum(b[1] for b in buffer) // len(buffer)
        avg_w = sum(b[2] for b in buffer) // len(buffer)
        avg_h = sum(b[3] for b in buffer) // len(buffer)
        return avg_x, avg_y, avg_w, avg_h

    def draw(self, frame):
        for obj_id in self.objects.keys():
            x, y, w, h = self.get_smoothed_position(obj_id)  # Verwendung der geglätteten Position
            cx = x + w // 2
            cy = y + h // 2
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f'ID: {obj_id}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)  # Draw center point

    def set_new_data(self):
        global positionZumo, positionObject
        sorted_ids = sorted(self.objects.keys())
        if len(sorted_ids) > 0:
            lowest_id = sorted_ids[0]
            x, y, w, h = self.get_smoothed_position(lowest_id)
            cx = x + w // 2
            cy = y + h // 2
            positionZumo = f"[{cx}, {cy}, {w}, {h}]"
        if len(sorted_ids) > 1:
            second_lowest_id = sorted_ids[1]
            x, y, w, h = self.get_smoothed_position(second_lowest_id)
            cx = x + w // 2
            cy = y + h // 2
            positionObject = f"[{cx}, {cy}, {w}, {h}]"
        print(f"Updated positionZumo: {positionZumo}")
        print(f"Updated positionObject: {positionObject}")

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    cv2.namedWindow('Settings')
    cv2.createTrackbar('Blur', 'Settings', 7, 20, nothing)
    cv2.createTrackbar('Canny Min', 'Settings', 75, 200, nothing)
    cv2.createTrackbar('Canny Max', 'Settings', 150, 300, nothing)
    cv2.createTrackbar('Min Area', 'Settings', 178, 1000, nothing)

    tracker = ObjectTracker(threshold=10, buffer_size=5)  # buffer_size hinzugefügt

    while True:
        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Setze den Frame-Zähler zurück
            continue

        blur_value = cv2.getTrackbarPos('Blur', 'Settings')
        canny_min = cv2.getTrackbarPos('Canny Min', 'Settings')
        canny_max = cv2.getTrackbarPos('Canny Max', 'Settings')
        min_area = cv2.getTrackbarPos('Min Area', 'Settings')

        if blur_value % 2 == 0:
            blur_value += 1

        normalized_frame = np.zeros_like(frame)
        cv2.normalize(frame, normalized_frame, 0, 255, cv2.NORM_MINMAX)

        gray = cv2.cvtColor(normalized_frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (blur_value, blur_value), 0)

        edged = cv2.Canny(blurred, canny_min, canny_max)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        tracker.update(contours)
        tracker.draw(frame)

        cv2.imshow('Camera Feed', frame)
        cv2.imshow('Edges', edged)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Start the object tracking in a separate thread or process if needed

    tracking_thread = threading.Thread(target=main)
    tracking_thread.start()

    # Main loop for sending data
    while True:
        # Use the global variables from the object tracking
        new_data = {
            "Zumo": {
                "positionZumo": positionZumo,
                "facing": [1, 0]
            },
            "Object": {
                "positionObject": positionObject
            }
        }

        get_data()

        if validate_data(new_data):
            send_data(new_data)
            get_data()  # To verify the new data
        else:
            print("Die Datenstruktur ist ungültig.")

        time.sleep(4)
