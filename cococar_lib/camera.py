from .utils import get_marker_distance
import cv2


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        # Load the ArUco dictionary
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        # Create ArUco parameters
        aruco_params = cv2.aruco.DetectorParameters()
        # Create ArUco detector
        self.aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    def detect_aruco_markers(self):
        """
        Detect ArUco markers in the given frame and return a list of marker objects.
        Each marker object contains the marker ID and the coordinates of its 4 corners.
        """
        # take a picture
        ret, frame = self.cap.read()
        if not ret:
            self.destroy()
            raise Exception('Failed to get camera frame.')

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.resize(gray, dsize=(640, 360))

        # Detect the markers
        corners, ids, rejected = self.aruco_detector.detectMarkers(gray)

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

    def destroy(self):
        self.cap.release()
