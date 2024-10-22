import cv2
import numpy as np
import math

display = True


def detect_aruco_markers(frame):
    """
    Detect ArUco markers in the given frame and return a list of marker objects.
    Each marker object contains the marker ID and the coordinates of its 4 corners.
    """
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, dsize=(640, 360))
    if display:
        cv2.imshow('grayscale', gray)

    # Load the ArUco dictionary
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

    # Create ArUco parameters
    aruco_params = cv2.aruco.DetectorParameters()

    # Create ArUco detector
    aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    # Detect the markers
    corners, ids, rejected = aruco_detector.detectMarkers(gray)

    markers = []
    if ids is not None:
        for i, marker_id in enumerate(ids):
            marker_corners = corners[i][0]
            markers.append({
                'id': marker_id[0],
                'corners': marker_corners,
                'distance': get_marker_distance(marker_corners)
            })

    return markers

def line_length(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def x_midpoint(a, b):
    return (a[1] + b[1]) / 2


def get_marker_distance(points):
    side = line_length(points[0], points[1])

    distance = 1 / side
    return distance * 1500 / 2.54  # conversion factor to inches


# Example usage:
if __name__ == "__main__":
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        markers = detect_aruco_markers(frame)

        if display:
            for marker in markers:
                # Draw the marker outline
                cv2.polylines(frame, [np.int32(marker['corners']) * 3], True, (255, 160, 60), 5)

                # Estimate and display the distance
                distance = marker['distance']

                # Get the top-left corner of the marker for text placement
                text_position = tuple(marker['corners'][0].astype(int) * 3)

                cv2.putText(frame, f"ID: {marker['id']}, Dist: {distance:.2f}in",
                            text_position,
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

            cv2.imshow('ArUco Marker Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print(markers)

    cap.release()
    cv2.destroyAllWindows()
