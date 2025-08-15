#  Invisible Cloak using OpenCV (Harry Potter Style) 

Bring a little magic into the real world!  
This Python project creates the illusion of invisibility using **OpenCV**, **color detection**, and some simple image processing tricks.

![Demo GIF](demo.gif)  
*(https://drive.google.com/file/d/1DCQILdlpzfXoNrhw4iZyVKYoKJp2pu1q/view?usp=drive_link)*

---

##  How It Works
1. **Background Capture** – The program first records the background without you in the frame.
2. **Color Detection** – A specific cloak color (default: RED) is detected using HSV color segmentation.
3. **Mask Cleaning** – Noise is removed, and missing cloak patches are filled using morphological operations.
4. **Background Replacement** – Detected cloak areas are replaced with the background, creating the illusion of invisibility in real-time.

---

##  Tech Stack
- **Python 3.x**
- **OpenCV** – for image processing and webcam handling
- **NumPy** – for fast array operations

---

##  Installation & Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/invisible-cloak.git
   cd invisible-cloak
