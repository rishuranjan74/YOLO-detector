import cv2

print("Attempting to open camera at index 0...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("FATAL ERROR: Cannot open camera. Exiting.")
else:
    print("Camera opened successfully. Starting video stream...")
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # If the frame was not read correctly, break the loop
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Display the resulting frame
        cv2.imshow('Minimal Camera Test - Press Q to Quit', frame)

        # Wait for the 'q' key to be pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("'q' key pressed. Closing...")
            break

# When everything is done, release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()
print("Program finished.")