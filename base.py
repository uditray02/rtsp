import cv2
import subprocess
import sys

# Define your video file path and RTSP stream URL (correctly formatted)
video_path = "video.mp4"  

# Open the video file using OpenCV
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video file.")
    sys.exit()

fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# Loop to read frames from the video and feed them to FFmpeg for RTSP streaming
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("End of video stream.")
        break
    
    
    # Optionally display the frame
    cv2.imshow("Video Stream", frame)
    
    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up after the loop
cap.release()
cv2.destroyAllWindows()
