import tkinter as tk
from datetime import datetime
import csv
import time
import scanflag  # Importing scanflag module to use scanned_flag
import mylogger  # Importing logging module

class UPDATE:
    def __init__(self, filename):
        self.filename = filename
        self.rows = []
        self.updated = False
        self.length = 0  # Initialize self.length

    def readcsv(self):
        """Reads the CSV file and calculates the length of the rows."""
        try:
            with open(self.filename, mode="r") as file:
                self.rows = list(csv.reader(file))
                self.length = len(self.rows)  # Update self.length
        except FileNotFoundError:
            mylogger.logger("readcsv_From_Update_Fails")

    def validate(self, ag, colname, frame):
        """
        Validates the QR code (ag), asks for the column name, updates the specified column in the CSV,
        and displays a red, yellow, or green label based on the scanned_flag status.
        """

        for widget in frame.winfo_children():
            widget.destroy()  # Clear previous widgets in the frame

        # Display "Scanner Ready" initially
        ready_label = tk.Label(frame, text="Scanner Ready", bg="blue", fg="white", font=("Arial", 14))
        ready_label.pack(pady=10)
        self.readcsv()  # Read the CSV file and update self.length

        # Ask the user for the new column name
        new_column_name = colname

        # If header exists, ensure the column is added
        if self.rows and len(self.rows) > 0:
            if new_column_name not in self.rows[0]:
                # Add the new column to the header
                self.rows[0].append(new_column_name)
                self.rows[0].append(f"{new_column_name} Timestamp")
        else:
            mylogger.logger("Empty CSV File")
            label = tk.Label(frame, text="Invalid Range", bg="white", fg="black", font=("Arial", 14), bd=2, relief="solid", highlightbackground="blue", highlightthickness=3)
            label.pack()
            time.sleep(1)
            label.destroy()
            return

        # Process the QR code
        now = datetime.now()
        self.updated = False
        scanflag.scanned_flag = "Red"  # Default to red (not found)

        # Check for a match and update the file
        for row in self.rows[1:]:  # Skip header row
            info = "".join(row[:6])
            if ag == info:
                if len(row) >= len(self.rows[0]) and row[-2] == "OK":  # Check if already scanned
                    scanflag.scanned_flag = "Yellow"  # Set flag to Yellow if already scanned
                    mylogger.logger("QrCode Already Scanned")
                else:
                    scanflag.scanned_flag = "Green"  # Set flag to Green on first match
                    mylogger.logger("QrCode Found")
                    while len(row) < len(self.rows[0]):
                        row.append("")  # Ensure row length matches header
                    row[-2] = "OK"
                    row[-1] = f"{now.strftime('%H:%M:%S')} {now.date()}"
                    self.updated = True
                break  # Stop processing after a match is found

        if self.updated:
            self.writecsv()  # Write the updated rows back to the CSV file

        # Update the label in the Tkinter window based on the scanned_flag status
        update_scan_result(frame)

        mylogger.logger("ScanFlag-->"+str(scanflag.scanned_flag))

    def writecsv(self):
        """Writes the updated rows back to the CSV file."""
        if self.updated:
            with open(self.filename, mode='w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(self.rows)
            
            mylogger.logger("CSV File Updated "+" : "+str(self.rows)+" : "+str(file))
        else:
            mylogger.logger("No Pending Changes")


def update_scan_result(frame):
    """Updates the label in the Tkinter window based on scanflag status."""
    
    # Destroy previous labels in the frame
    for widget in frame.winfo_children():
        widget.destroy()

    if scanflag.scanned_flag == "Green":
        # Success label
        label = tk.Label(frame, text="Success: QR Code Verified", bg="green", fg="white", font=("Arial", 14))
    elif scanflag.scanned_flag == "Yellow":
        # Already scanned label
        label = tk.Label(frame, text="Warning: QR Code Already Scanned", bg="yellow", fg="black", font=("Arial", 14))
    else:
        # Error label (not found)
        label = tk.Label(frame, text="Error: QR Code Not Found", bg="red", fg="white", font=("Arial", 14))

    label.pack()  # Make sure to pack the label

    # Schedule label update to "Scanner Ready" after 1 second
    frame.after(1000, lambda: create_scanner_ready_label(frame))


def create_scanner_ready_label(frame):
    """Helper function to create 'Scanner Ready' label after a short delay, destroying existing label first."""
    
    # Destroy any existing widgets in the frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create and pack the new 'Scanner Ready' label
    label = tk.Label(frame, text="Scanner Ready", bg="white", fg="black", font=("Arial", 14), bd=2, relief="solid", highlightbackground="blue", highlightthickness=3)
    label.pack()  # Pack or grid the new label
