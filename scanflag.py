# scanflag.py

scanned_flag = "Red"  # Default state for scanned_flag

# Any other function or logic where you need to modify the scanned_flag
def set_scanned_flag(status):
    global scanned_flag
    scanned_flag = status
    print(f"scanned_flag is now: {scanned_flag}")
