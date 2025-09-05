import cv2

def find_camera_index():
    """Cycles through camera indices and tries to open them."""
    print("Searching for available cameras...")
    for index in range(5):  # Check indices 0 through 4
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            print(f"✅ Camera found at index: {index}")
            ret, frame = cap.read()
            if ret:
                cv2.imshow(f"Camera Index {index}", frame)
                print(f"Press any key to close this window and check the next index.")
                cv2.waitKey(0)
            cap.release()
            cv2.destroyAllWindows()
        else:
            print(f"❌ No camera found at index: {index}")

if __name__ == "__main__":
    find_camera_index()