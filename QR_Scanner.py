import cv2
import update
import time
import tkinter as tk
from PIL import Image, ImageTk
import scanflag
import mylogger

class QRSCANNER:
    def __init__(self, root, filename, column_index, colname, tk_frame=None,tk_frame_bulb=None, width=640, height=480):

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
        self.width = width
        self.height = height

        # Configure camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


    def process_qr_code(self, qr_code_data):
        """Process the detected QR code and update the CSV file."""
        mylogger.logger(f"Processing QR code: {qr_code_data}")
        updater = update.UPDATE(self.filename)
        updater.validate(qr_code_data, self.colname , self.tk_frame_bulb)  # Use self.colname
        time.sleep(0.2)  # Wait for 0.2 seconds before continuing to the next QR code scan

    def start_scanning(self, window_name, tk_frame, width=50, height=10):

        # Create a Tkinter Label in the specified frame for the camera feed
        camera_label = tk.Label(tk_frame, text="Camera Preview")
        camera_label.pack(side=tk.LEFT, pady=2)

        # Resize the camera capture
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        def update_frame():
            # Read a frame from the webcam
            ret, frame = self.cap.read()
            if not ret:
                mylogger.logger("Camara Failed")
                return

            # Convert the frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to a PhotoImage for Tkinter
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            # Update the Label widget with the new frame
            camera_label.imgtk = imgtk
            camera_label.config(image=imgtk)

            # Detect and decode QR codes
            data, bbox, _ = self.detector.detectAndDecode(frame)
            if data:
                mylogger.logger(f"QR Code detected: {data}")
                self.process_qr_code(data)

            # Schedule the next frame update
            tk_frame.after(10, update_frame)

        # Start updating frames
        update_frame()
        

