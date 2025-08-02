import cv2

def process_8k_frame(frame):
    frame = cv2.resize(frame, (7680, 4320))
    return frame
