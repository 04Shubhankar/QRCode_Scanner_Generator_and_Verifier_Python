import csv
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import QR_Scanner
import QRCodeGenrator 
from PIL import Image, ImageTk
import time
import cv2
import scanflag
import mylogger

mylogger.logger("App.py_Started")
# Global variables
selected_file_path = ""  # Stores the selected file path
file_label = None  # Label to display the selected file path
spinbox = False  # Track whether spinboxes are created
qrscanner = None  # Variable to store the QRSCANNER object for stopping it later
colname_frame = None  # Initialize the colname_frame here


def file_selector():
    """Opens a file dialog to select a CSV file."""
    global selected_file_path, file_label
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV Files", "*.csv")])
    
    while file_path == "":
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV Files", "*.csv")])
    
    if file_path:  # If a file is selected
        selected_file_path = file_path
        if file_label:  # If the label already exists, update its text
            file_label.config(text=file_path)
        else:  # Create the label if it doesn't exist
            global csv_frame
            file_label = tk.Label(csv_frame, text=file_path)
            file_label.pack()
        mylogger.logger("FileSelection_Button_Pressed,Select_Path-->"+file_path)
        display_csv(file_path)

def display_csv(file_path):
    """Displays the content of a CSV file in the Treeview."""
    mylogger.logger("Displayed File,Select_Path-->"+file_path)
    # Clear any existing data in the Treeview
    for row in tree.get_children():
        tree.delete(row)
    
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        
        # Get the column headers
        headers = next(csv_reader)
        tree["columns"] = headers
        
        # Set the column headers
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, anchor="center")
        
        # Insert the data rows
        for row in csv_reader:
            tree.insert("", tk.END, values=row)


def genrate_qr():
    """Handles QR code generation logic."""
    global selected_file_path, spinbox, spinboxa, spinboxb

    if not selected_file_path:  # Prompt the user to select a file if none is selected
        file_selector()
    
    if selected_file_path:
        display_csv(selected_file_path)
        mylogger.logger("genrate_qr_Button_Pressed,Select_Path-->"+selected_file_path)

        if not spinbox:  # Create spinboxes and start button if not already created
            label = tk.Label(spinbox_frame, text="Set Starting and Ending \nColumns for QR File Naming:")
            label.pack(side=tk.LEFT, pady=5)

            spinboxa = tk.Spinbox(spinbox_frame, from_=0, to=100, width=10)
            spinboxa.pack(side=tk.LEFT, pady=10)

            spinboxb = tk.Spinbox(spinbox_frame, from_=0, to=100, width=10)
            spinboxb.pack(side=tk.LEFT, pady=10)

            progress = ttk.Progressbar(spinbox_frame, orient="horizontal", length=200, mode="determinate")
            progress.pack(side=tk.LEFT, pady=10)

            def start_progress(max_value):
                progress["maximum"] = max_value
                for i in range(max_value + 1):
                    progress["value"] = i
                    root.update_idletasks()
                    time.sleep(0.05)

            def start_generation():
                start_col = int(spinboxa.get())
                end_col = int(spinboxb.get())
                
                if start_col != end_col:
                    status = False
                    while not status:
                        status = QRCodeGenrator.main(start_col, end_col, selected_file_path)
                        start_progress(5)
                else:
                    mylogger.logger("Invalid Range Entered")
                    label = tk.Label(root, text="Invalid Range", bg="white", fg="black", font=("Arial", 14), bd=2, relief="solid", highlightbackground="blue", highlightthickness=3)
                    label.pack()
                    time.sleep(1)
                    label.destroy()
                

            start_button = tk.Button(spinbox_frame, text="Start", command=start_generation)
            start_button.pack(side=tk.LEFT, pady=10)

            spinbox = True

def scan_qr():
    """Prompts the user to select a file and provides an input box for column name."""
    global selected_file_path, colname_frame

    # Destroy previous frame if it exists to avoid duplicates
    if colname_frame and colname_frame.winfo_exists():
        colname_frame.destroy()

    # Force file selection every time scan_qr is called
    file_selector()

    if selected_file_path:
        mylogger.logger("scan_qr_Button_Pressed,Select_Path-->"+selected_file_path)
        
        # Create a new frame for colname input and button
        colname_frame = tk.Frame(root)
        colname_frame.pack(pady=10)

        # Label for the input box
        colname_label = tk.Label(colname_frame, text="Enter Column Name:")
        colname_label.pack(side=tk.LEFT, padx=5)

        # Input box for colname
        colname_entry = tk.Entry(colname_frame, width=20)
        colname_entry.pack(side=tk.LEFT, padx=5)

        def stop_qr_scanning():
            """Stops the camera and releases resources."""
            global qrscanner
            if qrscanner:  # Check if the scanner exists
                qrscanner.stop_scanning()  # Call the stop_scanning method of the QRSCANNER class
            cv2.destroyAllWindows()  # Ensure all OpenCV windows are destroyed
            if cam_frame.winfo_exists():  # Only destroy cam_frame if it exists
                cam_frame.destroy()
            mylogger.logger("Camera stopped and resources released.")
            #stop_button.config(state="disabled")  # Disable the stop button after stopping the scan
            #submit_button.config(state="disabled")

        def start_qr_scanning():
            colname = colname_entry.get()
            if not colname:
                label = tk.Label(csv_frame, text="Please Enter a Valid Name", bg="white", fg="Red", font=("Arial", 14), bd=2, relief="solid", highlightbackground="blue", highlightthickness=3)
                label.pack()
                time.sleep(1)
                label.destroy()
                return
            mylogger.logger("Submit_Pressed_To_Start_Scanning")

            mylogger.logger(f"Starting QR scan with column name: {colname}")
            label = tk.Label(bulb_frame, text="Scanner Ready", bg="white", fg="black", font=("Arial", 14), bd=2, relief="solid", highlightbackground="blue", highlightthickness=3)
            label.pack(side=tk.LEFT, padx=5)
            global qrscanner  # Make qrscanner global so it can be accessed in stop_qr_scanning
            qrscanner = QR_Scanner.QRSCANNER("T.E.C MBS2025", selected_file_path, 1, colname, cam_frame, bulb_frame)  # Pass colname
            qrscanner.start_scanning("T.E.C MBS2025", cam_frame)

            stop_button.config(state="normal")  # Enable the stop button after starting the scan
            #submit_button.config(state="disabled")


        # Button to submit colname and start scanning
        global submit_button
        submit_button = tk.Button(
            colname_frame,
            text="Start Scanning",
            command=start_qr_scanning,
            bg="white",
            font=("Helvetica", 10, "bold"),
        )
        submit_button.pack(side=tk.LEFT, padx=5)

        global stop_button
        stop_button = tk.Button(
            colname_frame,
            text="Stop Scanning",
            command=stop_qr_scanning,
            bg="white",
            font=("Helvetica", 10, "bold"),
            state="disabled"  # Initially disable the stop button
        )
        stop_button.pack(side=tk.LEFT, padx=5)


# Initialize the main Tkinter window
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.title("QR Scanner & Generator")
root.configure(bg="white")

# Create the label with white background
label = tk.Label(root, text="QR Scanner & Generator", font=("Arial", 60, "bold"), bg="white")
label.pack(pady=20)

# Frames
button_frame = tk.Frame(root, bg="white")
button_frame.pack()

csv_frame = tk.Frame(root)
csv_frame.pack()

spinbox_frame = tk.Frame(csv_frame)
spinbox_frame.pack()

cam_frame = tk.Frame(root)
cam_frame.pack()

bulb_frame = tk.Frame(cam_frame)
bulb_frame.pack(side="right")

# Buttons
select_file_button= tk.Button(button_frame,
                   text="Select File",
                   command=file_selector,
                   activebackground="lightyellow",  # Background color when pressed
                   activeforeground="black",  # Text color when pressed
                   bd=2,  # Border width
                   bg="white",  # Background color
                   cursor="hand1",  # Mouse cursor style
                   fg="black",  # Text color
                   font=("Helvetica", 12, "bold"),  # Font style, size, and weight
                   height=1,  # Height in lines
                   highlightbackground="lightyellow",  # Background color when focused
                   highlightcolor="blue",  # Border color when focused
                   image=None,  # Replace with an image path if needed
                   justify="center",  # Text alignment
                   padx=10,  # Horizontal padding
                   pady=10,  # Vertical padding
                   relief="raised",  # Border style
                   state="normal",  # Button state
                   takefocus=True,  # Whether it can receive keyboard focus
                   underline=0,  # Index of underlined character
                   width=10,  # Width in characters
                   wraplength=100,  # Maximum text width before wrapping
                   bitmap=None,  # Replace with a bitmap path if needed
                   compound="left",  # Combine text and image
                   overrelief="sunken")  # Relief style when the mouse hovers
select_file_button.pack(side=LEFT, padx=10)

genrate_qr_button = tk.Button(
    button_frame,
    text="Genrate QR Codes",
    command=genrate_qr,
    activebackground="lightyellow",  # Background color when pressed
    activeforeground="black",  # Text color when pressed
    bd=2,  # Border width
    bg="white",  # Background color
    cursor="hand1",  # Mouse cursor style
    fg="black",  # Text color
    font=("Helvetica", 12, "bold"),  # Font style, size, and weight
    height=1,  # Height in lines
    highlightbackground="lightyellow",  # Background color when focused
    highlightcolor="blue",  # Border color when focused
    image=None,  # Replace with an image path if needed
    justify="center",  # Text alignment
    padx=10,  # Horizontal padding
    pady=10,  # Vertical padding
    relief="raised",  # Border style
    state="normal",  # Button state
    takefocus=True,  # Whether it can receive keyboard focus
    underline=0,  # Index of underlined character
    width=10,  # Width in characters
    wraplength=100,  # Maximum text width before wrapping
    bitmap=None,  # Replace with a bitmap path if needed
    compound="left",  # Combine text and image
    overrelief="sunken"
)
genrate_qr_button.pack(side=LEFT, padx=10)

scan_qr_button = tk.Button(
    button_frame,
    text="Scan QR Codes",
    command=scan_qr,
    activebackground="lightyellow",  # Background color when pressed
    activeforeground="black",  # Text color when pressed
    bd=2,  # Border width
    bg="white",  # Background color
    cursor="hand1",  # Mouse cursor style
    fg="black",  # Text color
    font=("Helvetica", 12, "bold"),  # Font style, size, and weight
    height=1,  # Height in lines
    highlightbackground="lightyellow",  # Background color when focused
    highlightcolor="blue",  # Border color when focused
    image=None,  # Replace with an image path if needed
    justify="center",  # Text alignment
    padx=10,  # Horizontal padding
    pady=10,  # Vertical padding
    relief="raised",  # Border style
    state="normal",  # Button state
    takefocus=True,  # Whether it can receive keyboard focus
    underline=0,  # Index of underlined character
    width=10,  # Width in characters
    wraplength=100,  # Maximum text width before wrapping
    bitmap=None,  # Replace with a bitmap path if needed
    compound="left",  # Combine text and image
    overrelief="sunken"
)
scan_qr_button.pack(side=LEFT, padx=10)

# Treeview for CSV display
tree = ttk.Treeview(csv_frame, height=5)

# Scrollbars
v_scrollbar = ttk.Scrollbar(csv_frame, orient=tk.VERTICAL, command=tree.yview)
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

h_scrollbar = ttk.Scrollbar(csv_frame, orient=tk.HORIZONTAL, command=tree.xview)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
tree.pack(fill=tk.BOTH, expand=True)
# Run the application
root.mainloop()
