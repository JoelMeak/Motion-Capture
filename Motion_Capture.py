import cv2
import numpy as np 

# Load the video
src = ""
cap = cv2.VideoCapture(src)

# fps
fps = cap.get(cv2.CAP_PROP_FPS)

# Total Frames
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Background subtraction
fgbg = cv2.createBackgroundSubtractorMOG2()

# Variable to keep track of motion
motion_detected = False
mads = []
threshold_factor = 0.2
current_frame = -1
prev_frame = 1
seconds = []

interval = 1

for i in range(round(total_frames / interval)):
    current_frame += 1
    if current_frame == i:
        ret, frame = cap.read()
        if not ret:
            break
        if prev_frame is not None:
            diff = cv2.absdiff(frame, prev_frame)
            mad = np.mean(np.abs(diff))
            avg = np.mean(frame)
            norm_mad = round(mad / avg, 3)
            mads.append(float(norm_mad))
            if norm_mad > 0.01:
                with open("Motion_Detection", "a+") as file:
                    file.seek(0)
                    second = str(round(current_frame / fps))
                    if second not in seconds:
                        seconds.append(second)
                    for s in seconds:
                      file.write("True --- " + str(s) + "   (" + str(norm_mad) + ")\n")

        prev_frame = frame




with open(str(src) + "   MAD_SCORE", "w+") as file:
    for i in mads:
        file.write(str(i) + " --- ")
print(f"fps: {fps}")
print(f"total frames: {total_frames}")
print(f"frames checked: {len(mads)}")
cap.release()
cv2.destroyAllWindows()