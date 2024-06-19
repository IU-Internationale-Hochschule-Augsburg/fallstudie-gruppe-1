import cv2

def nothing(x):
    pass

def main():
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    cv2.namedWindow('Settings')
    cv2.createTrackbar('Blur', 'Settings', 6, 20, nothing)   
    cv2.createTrackbar('Canny Min', 'Settings', 43, 200, nothing)  
    cv2.createTrackbar('Canny Max', 'Settings', 99, 300, nothing) 
    cv2.createTrackbar('Min Area', 'Settings', 178, 1000, nothing) 

    while True:
       
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        blur_value = cv2.getTrackbarPos('Blur', 'Settings')
        canny_min = cv2.getTrackbarPos('Canny Min', 'Settings')
        canny_max = cv2.getTrackbarPos('Canny Max', 'Settings')
        min_area = cv2.getTrackbarPos('Min Area', 'Settings')

        if blur_value % 2 == 0:
            blur_value += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (blur_value, blur_value), 0)
        edged = cv2.Canny(blurred, canny_min, canny_max)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > min_area: 
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Camera Feed', frame)
        cv2.imshow('Edges', edged)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
