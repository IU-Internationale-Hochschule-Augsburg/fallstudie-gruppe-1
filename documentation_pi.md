## Raspberry Pi Documentation

### Table of Contents
1. Introduction
2. Target Audience
3. System Architecture
4. Communication
5. Technical Functionality
6. Instructions
7. Resources

### 1. Introduction
The purpose of this documentation is to provide the user with comprehensive information on the function, configuration, and use of the Raspberry Pi as one of the two essential components of the project. The role of the Raspberry Pi is to detect objects using a connected camera and transmit data on the position and size of the objects to the Zumo Robot.

### 2. Target Audience
The system is aimed at individuals who want to use and/or further develop the overall system consisting of the Raspberry Pi and Zumo Robot for the purpose of moving objects. Additionally, the Raspberry Pi's object detection and data transmission functions can also be adapted by individuals who wish to use these functions independently of the Zumo Robot for other purposes. The system is particularly suitable for computer science students who can gain experience and make learning progress through applications and extensions of the existing foundation.

### 3. System Architecture
**Hardware Level:**<br>
- **Raspberry Pi**: Performs image processing and object detection and sends the data to the Zumo Robot.<br>
- **Camera**: Captures images and sends them to the Pi for processing.<br>
- **WiFi Module**: Enables network connection for data transmission.<br>
- **Control PC**: Used to operate the Pi via SSH.<br>

**Software Level:**<br>
- **Python**: Programming language for software development.<br>
- **OpenCV**: Used to process camera images and detect objects.<br>

### 4. Communication
**Communication Protocols:**<br>
- **SSH**: Used communicate between Control PC and PI.<br>
- **HTTP**: Used to send and receive data between the Raspberry Pi and the Zumo Robot.<br>
- **JSON**: Data format for transmitting information between devices.<br>

**Network Communication:**<br>
- **WiFi**: Allows the Raspberry Pi to connect to the network to send data to the Zumo Robot.<br>

### 5. Technical Functionality
- **API Configuration**: The Pi sends data to a web server, accessed via the URL and keys in the header.<br>
- **Position Variables**: `positionZumo` and `positionObject` store the position data of the Zumo Robot and other objects.<br>
- **Functions to Retrieve (`get_data`) and Send (`send_data`) Data from/to the API**.<br>
- **Function to Validate Data (`validate_data`)**.<br>
- **ObjectTracker Class**: Manages detected objects.<br>
  - Updates detected objects (`def update`).<br>
  - Updates the data of detected objects (`def update_buffers`).<br>
  - Smooths the data of detected objects (`def get_smoothed_position`).<br>
  - Draws the boundary (rectangle) and center (dot) of detected objects.<br>
  - Updates `positionZumo` and `positionObject` (`def set_new_data()`).<br>
- **main Function**:<br>
  - Normalizes the frame.<br>
  - Creates a grayscale image.<br>
  - Smooths the grayscale image using Gaussian Blur.<br>
  - Canny algorithm: Identifies edges.<br>
  - Identifies object contours.<br>
  - Determines object sizes, identifies the largest object as the Zumo Robot.<br>

**Main Program:**<br>
- Starts the main function.<br>
- Multithreading: Image processing and API communication run in separate threads.<br>
- `new_data` contains the current values of `positionZumo` and `positionObject`.<br>
- Current data is continuously retrieved, validated, and sent to the API.<br>

### 6. Instructions
1. **Installations:**<br>
   - **Install Pip/Python**: Install Pip/Python with the following command:<br>
     ```sh
     python -m ensurepip --upgrade
     ```

   - **Install OpenCV**: Install OpenCV with the following command:<br>
     ```sh
     pip install opencv-python==4.5.3.56
     ```

2. **Clone GitHub Repository:**<br>
   - Clone the repository with the following command:<br>
     ```sh
     git clone https://github.com/IU-Internationale-Hochschule-Augsburg/fallstudie-gruppe-1.git 
     cd fallstudie-gruppe-1
     ```

3. **Check and Run:**<br>
   - **WiFi Settings**: Ensure your Raspberry Pi is correctly connected to WiFi.<br>
   - **Server Connection**: Ensure the server the Raspberry Pi is to communicate with is running and reachable.<br>
   - **Run Code**: Execute the relevant file on the Raspberry Pi.<br>

### 7. Resources:
- **OpenCV Documentation**: [OpenCV Documentation](https://docs.opencv.org/4.x/index.html)<br>
