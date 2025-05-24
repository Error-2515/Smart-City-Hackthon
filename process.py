import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import cv2
from ultralytics import YOLO
import pytesseract
import matplotlib.pyplot as plt

# Load models
color_model = tf.keras.models.load_model('vehicle_color_classifier.h5')
plate_model = YOLO('license_plate_detector (1).pt')
type_model = YOLO("yolov8n.pt")

# Class labels for color classification
color_labels = {
    0: 'beige', 1: 'black', 2: 'blue', 3: 'brown', 4: 'gold', 5: 'green',
    6: 'grey', 7: 'orange', 8: 'pink', 9: 'purple', 10: 'red', 11: 'silver',
    12: 'tan', 13: 'white', 14: 'yellow'
}

# Predict vehicle color
def predict_vehicle_color(image_path):
    img = load_img(image_path, target_size=(128, 128))  # Resize to model's input size
    img_array = img_to_array(img) / 255.0  # Normalize the image
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    predictions = color_model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    return color_labels[predicted_class]

# Detect number plate
def detect_number_plate(model, image):
    results = model(image)  # Run inference on the image
    boxes = results[0].boxes
    number_plate_img = None
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
        confidence = box.conf[0]  # Confidence score
        cls = box.cls[0]  # Class ID
        if confidence > 0.7 and int(cls) == 0:  # Assuming class '0' is number plate
            number_plate_img = image[y1:y2, x1:x2]
            break
    return number_plate_img

# Extract text from number plate
def extract_text_from_plate(number_plate_img):
    """
    Extract text from the number plate using OCR, ensuring it starts with a letter
    by removing leading numbers if present.
    """
    # Preprocess the image
    gray = cv2.cvtColor(number_plate_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.medianBlur(thresh, 3)
    
    # Perform OCR
    config = '--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    plate_text = pytesseract.image_to_string(denoised, config=config).strip()
    original_text = plate_text  # Save the original OCR output for fallback
    
    # Remove leading numbers until the text starts with a letter
    while plate_text and not plate_text[0].isalpha():
        plate_text = plate_text[1:]
    print(plate_text)
    # Return the processed text if it starts with a letter, else return the original text
    return plate_text if plate_text else None, original_text


    

# Predict vehicle type
def predict_vehicle_type(model, image_path):
    img = cv2.imread(image_path)
    results = model(img)
    labels = results[0].names
    boxes = results[0].boxes
    class_ids = boxes.cls
    xywh = boxes.xywh
    max_area = 0
    vehicle_type = 'vehicle not found'
    for class_id, box in zip(class_ids, xywh):
        _, _, width, height = box
        area = width * height
        if area > max_area:
            max_area = area
            vehicle_type = labels[int(class_id)]
    return vehicle_type

# Main function to process the image
def process_image(image_path):
    # Predict vehicle color
    predicted_color = predict_vehicle_color(image_path)
    
    # Detect number plate and extract text
    image = cv2.imread(image_path)
    number_plate_img = detect_number_plate(plate_model, image)
    plate_text = None
    found_text =None
    if number_plate_img is not None:
        plate_text,found_text = extract_text_from_plate(number_plate_img)
        
        if plate_text is None:
            print(f"No valid number plate detected ({found_text}).")
    
    # Predict vehicle type
    vehicle_type = predict_vehicle_type(type_model, image_path)

    return predicted_color, plate_text, vehicle_type

