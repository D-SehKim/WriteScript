import cv2 
import pytesseract

def get_text(screenshot_path):
    screenshot_path = screenshot_path

    img = cv2.imread(screenshot_path)
    (h, w) = img.shape[:2]
    img = cv2.resize(img, (w*3, h*3))

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    binary_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))

    # Detect horizontal lines in the binary image
    detected_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    # Subtract the detected lines from the binary image
    binary_image_no_lines = cv2.bitwise_and(binary_image, cv2.bitwise_not(detected_lines))

    text = pytesseract.image_to_string(binary_image_no_lines, config='--psm 6 --oem 3 -c tessedit_char_blacklist=|')