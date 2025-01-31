import qrcode
from PIL import Image, ImageDraw
import csv
import tkinter as tk
from tkinter import filedialog
import mylogger

def file_selector():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV Files", "*.csv")])
    while file_path == "":
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV Files", "*.csv")])
    mylogger.logger("Selected File in QRCodeGenrator.py is -->"+ file_path)
    return file_path

def directory_selector():
    folder_path = filedialog.askdirectory(title="Select Folder to Save QR Codes")
    while folder_path == "":
        folder_path = filedialog.askdirectory(title="Select Folder to Save QR Codes")
    mylogger.logger("Selected Folder in QRCodeGenrator.py is to save QR-->" + folder_path)
    return folder_path

def genqr(data, text, folder_path):
    # Data to be encoded
    # Encoding data using make() function
    img = qrcode.make(data)

    # Adding text below the QR Code
    # Create a new image with space for text below the QR Code
    new_width = img.size[0]
    new_height = img.size[1] + 15  # Add space for the text
    new_img = Image.new("RGB", (new_width, new_height), "white")

    # Paste the QR Code onto the new image
    new_img.paste(img, (0, 0))

    # Add the text
    draw = ImageDraw.Draw(new_img)
    text_x = (new_width - len(text) * 6) // 2  # Approximate text width for centering
    text_y = img.size[1] + 5  # Position the text just below the QR Code
    draw.text((text_x, text_y), text, fill="black")

    # Saving the final image
    sanitized_filename = ''.join(c for c in text if c.isalnum() or c in (' ', '_')).strip()
    file_path = f"{folder_path}/{sanitized_filename}.png"
    new_img.save(file_path)
    mylogger.logger(f"QR Code saved at: {file_path}")

def main(startjoin,endjoin,file):
    folder_path = directory_selector()

    with open(file) as csv_file:
        rows = list(csv.reader(csv_file))
        mylogger.logger("Length Or Rows -->"+str(len(rows)))
        max_row=len(rows[0])
        for row in rows:
            info = "".join(row[:max_row])
            genqr(info, "".join(row[startjoin:endjoin]), folder_path)
            mylogger.logger("row[0]-->"+str(row[0]))
        return True

