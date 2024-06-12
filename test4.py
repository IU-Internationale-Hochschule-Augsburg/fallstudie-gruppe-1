import cv2

def draw_bounding_boxes(frame, contours):
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print( x + y + w + h)
def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Fehler beim Öffnen der Kamera")
        return

    while True:
        
        ret, frame = cap.read()
        
        if not ret:
            print("Fehler beim Lesen des Frames")
            break

       
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        blurred = cv2.GaussianBlur(gray, (3, 3), 1)
       
        edged = cv2.Canny(blurred, 25, 200)
        
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        
        draw_bounding_boxes(frame, contours)
        
        
        cv2.imshow("Frame", frame)
        cv2.imshow("gray",gray)
        cv2.imshow("blurred",blurred)
        cv2.imshow("edged",edged)
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()