# QR Code Scanner, Generator, and Verifier – Python

A Python-based application for generating, scanning, and verifying QR codes. This app is designed to streamline the process of working with QR codes by allowing users to generate QR codes from CSV data, scan QR codes, and verify the data against the contents of a CSV file. The app is built using Python, OpenCV, and the `qrcode` library.

## Features

### 1. QR Code Generator
- **Create QR codes from CSV data**: Users can upload a CSV file, and the app will automatically generate QR codes for each row in the CSV. This is useful for creating QR codes in bulk for products, URLs, or other structured data.

### 2. CSV Display
- **View CSV contents**: The app allows users to display the data from any CSV file, making it easy to manage and inspect the dataset directly within the application. This is particularly helpful when working with large sets of data.

### 3. QR Code Scanner
- **Scan QR codes**: Users can scan QR codes using a webcam or by uploading an image that contains a QR code. The scanned QR code is decoded and displayed in the app for further action.

### 4. QR Code Verifier
- **Verify QR codes**: The app cross-references the data in the scanned QR code with the information in the CSV file. This ensures the validity and accuracy of the scanned data, which is ideal for applications requiring data verification.

## Tech Stack

This app uses the following technologies:

- **Python**: The core programming language used to build the application.
- **OpenCV**: A computer vision library that helps in processing images for QR code scanning.
- **qrcode Library**: A Python library used for generating QR codes.
- **Tkinter**: For creating the graphical user interface (GUI) of the app.

##Modules Used
This app makes use of the following Python modules:

- tkinter: For building the graphical user interface (GUI).
- Pillow (PIL): For handling image files, particularly in creating and displaying QR codes.
- opencv-python: For QR code scanning using a webcam.
- qrcode: For generating QR codes from input data.
- csv: For reading and writing CSV files containing the data.
- datetime: For managing time-related functionalities.
- scanflag: A custom module used for managing scanning flags during the QR code scanning process.
- mylogger: A custom logging module that tracks activities and errors in the app.
- time: For managing timing-related tasks and introducing delays where necessary.
- filedialog: A module used to open file dialogs to select files (e.g., CSV files).

## Installation

Follow the steps below to install and run the app on your local machine:

### Step 1: Clone the Repository
Clone the repository to your local machine using the following command:
```bash
git clone https://github.com/yourusername/QRCode_Scanner_Generator.git
```
## How to Use

### Step 1: Load CSV File
- Click the **"Load CSV"** button to select and load a CSV file into the app. The contents of the CSV will be displayed in the application window.

### Step 2: Generate QR Codes
- After loading the CSV file, click the **"Generate QR Codes"** button. The app will create QR codes for each row in the CSV file and display them in the window.

### Step 3: Scan QR Codes
- To scan a QR code, click the **"Scan QR Code"** button and enter name of column where results have to be stored. The app will activate the webcam, allowing you to scan a QR code. Once scanned, the app will decode and display the information from the QR code.

### Step 4: Info Verification
- When a QR code is scanned, the app will compare the scanned data with the corresponding data in the loaded CSV file. It will display whether the scanned QR code’s data matches the entry in the CSV file.



#### Feel free to fork the repository and submit pull requests if you'd like to contribute. Any improvements, bug fixes, or new features are always welcome. If you encounter any issues or have feature requests, please open an issue in the GitHub repository.

