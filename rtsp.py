import cv2
import subprocess
import sys

# Define your video file path and RTSP stream URL (correctly formatted)
video_path = "classroom.mp4"  
rtsp_url = "rtsp://192.168.1.100:554/live"  # Replace with your drone's RTSP stream address

# Open the video file using OpenCV
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video file.")
    sys.exit()

fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set up FFmpeg process for RTSP streaming
ffmpeg_command = [
    'ffmpeg',
    '-y',  # Overwrite output files without asking
    '-f', 'rawvideo',  # Raw video format
    '-vcodec', 'rawvideo',  # Specify raw video codec
    '-pix_fmt', 'bgr24',  # Pixel format (BGR)
    '-s', f'{frame_width}x{frame_height}',  # Set resolution
    '-r', str(fps),  # Frame rate
    '-i', '-',  # Input from stdin (raw frames)
    '-vcodec', 'libx264',  # Video codec (H.264)
    '-f', 'rtsp',  # Output format: RTSP
    '-rtsp_transport', 'tcp',  # Use TCP for RTSP transport
    rtsp_url  # RTSP URL to stream to
]

# Start FFmpeg process
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

# Loop to read frames from the video and feed them to FFmpeg for RTSP streaming
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("End of video stream.")
        break
    
    # Write the frame to FFmpeg's stdin (raw frame in BGR24 format)
    ffmpeg_process.stdin.write(frame.tobytes())
    
    # Optionally display the frame
    cv2.imshow("Video Stream", frame)
    
    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up after the loop
cap.release()
cv2.destroyAllWindows()
ffmpeg_process.stdin.close()
ffmpeg_process.wait()
