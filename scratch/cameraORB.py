import cv2
import numpy as np
import random
import time

# Initialize the camera capture
cap = cv2.VideoCapture(0)

# Initialize the ORB feature detector
# orb = cv2.ORB_create(nfeatures=5000, scaleFactor=1.2, nlevels=8, edgeThreshold=31, firstLevel=0, WTA_K=2, scoreType=cv2.ORB_FAST_SCORE, patchSize=31, fastThreshold=20)
orb = cv2.ORB_create(nfeatures=10000, scaleFactor=1.1, nlevels=10, edgeThreshold=15, firstLevel=0, WTA_K=2, scoreType=cv2.ORB_FAST_SCORE, patchSize=31, fastThreshold=10)


# Initialize the brute-force matcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Initialize variables for feature tracking
prev_gray = None
prev_keypoints = None
prev_descriptors = None
feature_tracks = {}
feature_colors = {}
track_length = 10
distance_threshold = 50

# Initialize variables for FPS calculation
fps_start_time = time.time()
fps_frame_count = 0

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect keypoints and compute descriptors using ORB
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    
    if prev_gray is not None and prev_descriptors is not None:
        # Match keypoints with the previous frame using brute-force matching
        matches = bf.match(descriptors, prev_descriptors)
        
        # Filter matches based on distance threshold
        filtered_matches = []
        for match in matches:
            prev_pt = prev_keypoints[match.trainIdx].pt
            curr_pt = keypoints[match.queryIdx].pt
            distance = np.sqrt((prev_pt[0] - curr_pt[0])**2 + (prev_pt[1] - curr_pt[1])**2)
            if distance <= distance_threshold:
                filtered_matches.append(match)
        
        # Update feature tracks and colors
        current_tracks = {}
        for match in filtered_matches:
            prev_idx = match.trainIdx
            curr_idx = match.queryIdx
            
            if prev_idx in feature_tracks:
                current_tracks[curr_idx] = feature_tracks[prev_idx] + [keypoints[curr_idx].pt]
                feature_colors[curr_idx] = feature_colors[prev_idx]
            else:
                current_tracks[curr_idx] = [keypoints[curr_idx].pt]
                feature_colors[curr_idx] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        feature_tracks = current_tracks
        
        # Draw feature tracks on the current frame
        for curr_idx, track in feature_tracks.items():
            tail = track[-track_length:]
            for i in range(1, len(tail)):
                prev_pt = tuple(map(int, tail[i-1]))
                curr_pt = tuple(map(int, tail[i]))
                cv2.line(frame, prev_pt, curr_pt, feature_colors[curr_idx], 2)
            
            # Draw the current keypoint as a circle
            curr_pt = tuple(map(int, tail[-1]))
            cv2.circle(frame, curr_pt, 3, feature_colors[curr_idx], -1)
        
        # Remove old feature tracks
        feature_tracks = {k: v for k, v in feature_tracks.items() if len(v) <= track_length}
        feature_colors = {k: v for k, v in feature_colors.items() if k in feature_tracks}
    
    # Update variables for the next iteration
    prev_gray = gray
    prev_keypoints = keypoints
    prev_descriptors = descriptors
    
    # Calculate FPS
    fps_frame_count += 1
    fps_end_time = time.time()
    elapsed_time = fps_end_time - fps_start_time
    fps = fps_frame_count / elapsed_time
    
    # Display FPS on the frame
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Display the frame with feature tracks
    cv2.imshow('Frame', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()