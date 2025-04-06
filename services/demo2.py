import cv2
import pytesseract
from PIL import Image

# Point to tesseract.exe if not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Step 1: Read the image using OpenCV
img = cv2.imread(r'C:/Users/MEVIN/Downloads/ut.jpg')

# Step 2: Convert to grayscale (simplifies the image)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Step 3: Apply adaptive thresholding (better for uneven lighting/handwritten notes)
thresh = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)

# Optional Step 4: Denoise (reduces unwanted noise)
denoised = cv2.fastNlMeansDenoising(thresh, h=30)

# Optional Step 5: Save the processed image to check it manually
cv2.imwrite('processed_image.jpg', denoised)

# Step 6: Extract text using pytesseract with better configuration
custom_config = r'--oem 3 --psm 6'  # Try other PSMs if needed
text = pytesseract.image_to_string(denoised, config=custom_config)

# Step 7: Print the result
print("Extracted Text:\n")
print(text)
