import cv2
import numpy as np


def detect_aruco_markers(cap=None):
    # Initialize the camera if not provided
    if cap is None:
        cap = cv2.VideoCapture(0)

    # Load the ArUco dictionary
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    # Create ArUco parameters
    aruco_params = cv2.aruco.DetectorParameters()

    # Create ArUco detector
    aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    detected_ids = []

    # Capture and process frames for a short duration
    for _ in range(10):  # Process 10 frames
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Detect ArUco markers
        corners, ids, rejected = aruco_detector.detectMarkers(frame)

        if ids is not None:
            # Draw detected markers
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Add detected IDs to the list
            detected_ids.extend(ids.flatten().tolist())

        # Display the resulting frame
        cv2.imshow('ArUco Marker Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Return the unique array of marker IDs
    return list(set(detected_ids))


# Example usage
cap = cv2.VideoCapture(0)  # Open the camera once

try:
    while True:
        ids = detect_aruco_markers(cap)
        print("Detected marker IDs:", ids)

        # Add a small delay to control the detection rate
        cv2.waitKey(100)  # Wait for 100ms

except KeyboardInterrupt:
    print("Detection stopped by user")

finally:
    # Release the capture and close windows when done
    cap.release()
    cv2.destroyAllWindows()