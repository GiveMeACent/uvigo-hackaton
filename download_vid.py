import os
import cv2

def capture_and_save_video(device_name: str):

  device_folder = createFileStruct(device_name)
  video_folder = os.path.join(device_folder, "videos")
    
  # Open the camera (replace 0 with the correct camera index if needed)
  cap = cv2.VideoCapture(0)  # Assuming the camera is connected as the first device
    
  if not cap.isOpened():
        print("[ERROR] Failed to open camera.")
        return
    
    # Define the codec and create a VideoWriter object for saving the video
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    video_filename = f"{device_name}_{timestamp}.avi"
    video_path = os.path.join(video_folder, video_filename)
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Using XVID codec for AVI format
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))  # 640x480 resolution, 20 FPS
    
    print(f"[INFO] Recording video to {video_path}")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to capture frame.")
            break
        
        out.write(frame)  # Write the frame to the video file
        
        # Display the video feed (optional)
        cv2.imshow("Video Feed", frame)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    # Log the added video file
    log_video(video_filename, video_p
