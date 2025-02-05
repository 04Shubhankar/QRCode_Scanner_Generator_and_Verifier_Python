import cv2
import update
import time
import tkinter as tk
from PIL import Image, ImageTk
import scanflag
import mylogger

class QRSCANNER:
    def __init__(self, root, filename, column_index, colname, tk_frame=None, tk_frame_bulb=None, width=150, height=150):
        # Initialize webcam and QR code detector
        self.cap = cv2.VideoCapture(0)
        self.detector = cv2.QRCodeDetector()
        self.filename = filename
        self.column_index = column_index
        self.colname = colname
        self.tk_frame_bulb = tk_frame_bulb

        # Tkinter integration
        self.root = root
        self.tk_frame = tk_frame
        self.camera_label = None  # To store the camera preview label
        self.running = False  # Flag to control scanning

        # Configure camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def process_qr_code(self, qr_code_data):
        """Process the detected QR code and update the CSV file."""
        mylogger.logger(f"Processing QR code: {qr_code_data}")
        updater = update.UPDATE(self.filename)
        updater.validate(qr_code_data, self.colname, self.tk_frame_bulb)  # Use self.colname
        time.sleep(0.2)  # Wait for 0.2 seconds before continuing to the next QR code scan

    def start_scanning(self, window_name, tk_frame, width=150, height=150):
        """Starts the QR code scanning process."""
        self.running = True  # Set running flag to True

        # Create a Tkinter Label in the specified frame for the camera feed
        if not self.camera_label:
            self.camera_label = tk.Label(tk_frame, text="Camera Preview")
            self.camera_label.pack(side=tk.LEFT, pady=2)

        def update_frame():
            if not self.running:  # Stop updating frames if scanning is stopped
                return

            # Read a frame from the webcam
            ret, frame = self.cap.read()
            if not ret:
                mylogger.logger("Camera Failed")
                return

            # Convert the frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            # Update the Label widget with the new frame
            self.camera_label.imgtk = imgtk
            self.camera_label.config(image=imgtk)

            # Detect and decode QR codes
            data, bbox, _ = self.detector.detectAndDecode(frame)
            if data:
                mylogger.logger(f"QR Code detected: {data}")
                self.process_qr_code(data)

            # Schedule the next frame update
            tk_frame.after(10, update_frame)

        # Start updating frames
        update_frame()

    def stop_scanning(self):
        """Stops the camera scanning and releases resources."""
        self.running = False  # Stop frame update loop

        # Release camera resources
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

        # Clear Tkinter frame
        if self.camera_label:
            self.camera_label.destroy()
            self.camera_label = None

        mylogger.logger("Camera stopped and resources released.")
