import cv2
import numpy as np
import time

def get_background(cap, num_frames=30, wait_between=0.02):
    """Capture a stable background by averaging several frames."""
    print("[INFO] Capturing background... Please step out of the frame.")
    frames = []
    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        frames.append(frame.astype(np.float32))
        time.sleep(wait_between)
    bg = np.mean(frames, axis=0).astype(np.uint8)
    print("[INFO] Background captured.")
    return bg

def create_red_mask(hsv):
    """
    Create a mask for red color in HSV.
    Looser range for better detection under varied lighting.
    """
    # Range 1 (0-10)
    lower1 = np.array([0, 100, 40])
    upper1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower1, upper1)

    # Range 2 (170-180)
    lower2 = np.array([170, 100, 40])
    upper2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower2, upper2)

    mask = mask1 | mask2
    return mask

def clean_mask(mask, k=3):
    """Remove noise and fill small holes."""
    kernel = np.ones((k, k), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)
    mask = cv2.dilate(mask, kernel, iterations=4)
    return mask

def main():
    print("[INFO] Starting camera...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not access webcam.")
        return

    time.sleep(2.0)  # warm-up

    background = get_background(cap)

    print("[INFO] Ready! Hold up your red cloak. Press 'q' to quit, 'b' to recapture background.")

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame grab failed; skipping.")
            continue

        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create & clean mask
        mask = create_red_mask(hsv)
        mask = clean_mask(mask)

        # Invert mask for non-cloak regions
        mask_inv = cv2.bitwise_not(mask)

        # Extract regions
        foreground = cv2.bitwise_and(frame, frame, mask=mask_inv)
        cloak_area = cv2.bitwise_and(background, background, mask=mask)

        # Merge without weighting (faster)
        final = cv2.add(foreground, cloak_area)

        # FPS counter
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(final, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Invisible Cloak", final)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('b'):
            background = get_background(cap)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
