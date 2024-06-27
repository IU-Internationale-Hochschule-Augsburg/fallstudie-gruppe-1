import cv2
import numpy as np

def nothing(x):
    pass

class ObjectTracker:
    def __init__(self, threshold=10):
        self.threshold = threshold
        self.objects = {}
        self.next_id = 0

    def update(self, contours):
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

    def draw(self, frame):
        for obj_id, (x, y, w, h) in self.objects.items():
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f'ID: {obj_id}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

def main():

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return


    # Pfad zum Video
   # video_path = 'path/to/your/video.mp4'
    # cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    cv2.namedWindow('Settings')
    cv2.createTrackbar('Blur', 'Settings', 6, 20, nothing)
    cv2.createTrackbar('Canny Min', 'Settings', 43, 200, nothing)
    cv2.createTrackbar('Canny Max', 'Settings', 99, 300, nothing)
    cv2.createTrackbar('Min Area', 'Settings', 178, 1000, nothing)

    tracker = ObjectTracker(threshold=10)

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

        # Kontrast erhöhen
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
    main()
