import cv2
import pytesseract
import re
import os
import pyperclip

def detect_timestamp(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Define the region of interest (ROI) for the left timestamp
    height, width, _ = image.shape
    roi = image[0:height, 0:int(width)]  # Adjust to focus on the left side of the image

    # Convert the ROI to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to enhance text
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Run OCR on the processed ROI
    custom_config = r'--oem 3 --psm 6'  # Using Tesseract OCR configurations
    detected_text = pytesseract.image_to_string(thresh, config=custom_config)

    # Use regular expressions to extract the timestamp in mm:ss format
    timestamp_pattern = r'\b\d{1,2}:\d{2}\b'
    matches = re.findall(timestamp_pattern, detected_text)

    new_time = matches[0].replace(":", "_")

    new_image_path = "/Users/xiaotingzhou/Desktop/QuickTime_Screenshot_" + f"{new_time}.png"
    # Rename the file
    # os.rename(image_path, new_image_path)

    pyperclip.copy(matches[0])  # Copies text to clipboard

    if matches:
        return matches[0]  # Return the first detected timestamp
    else:
        return None  # Return None if no timestamp is found


# Example usage:
image_path = "/Users/xiaotingzhou/Desktop/QuickTime_Screenshot.png"  # Update with the correct image path
timestamp = detect_timestamp(image_path)
if timestamp:
    print("Detected timestamp:", timestamp)
else:
    print("No timestamp found.")