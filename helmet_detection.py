import cv2
import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
import io

# Function to load the YOLOv8 model
def load_yolov8_model():
    # Load a pre-trained YOLOv8 model (adjust based on your version)
    model = YOLO('yolov8n.pt')  # YOLOv8 Nano for lightweight model, change if necessary
    return model

# Function to detect yellow color in the image
def detect_yellow(image):
    # Convert the image to HSV (Hue, Saturation, Value) color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper bounds for the yellow color in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])

    # Create a mask for yellow color
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    
    # If any yellow color is detected, it will be white in the mask
    yellow_detected = np.any(yellow_mask)
    return yellow_detected, yellow_mask

# Function to run inference on uploaded image, focusing on detecting the helmet
def detect_helmet_on_uploaded_image(model, uploaded_image):
    # Read the uploaded image into a PIL object
    pil_image = Image.open(io.BytesIO(uploaded_image.read()))
    
    # Convert the PIL image to RGB and then to numpy array
    image = np.array(pil_image.convert("RGB"))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Detect yellow color in the image
    yellow_detected, yellow_mask = detect_yellow(image)

    # Perform inference on the image, using model.predict() for specific detection
    results = model(image, classes=[0])  # Only look for the 'helmet' class (adjust the class ID if needed)

    # Results rendering
    annotated_image = results[0].plot()  # Use the first result to get the image with annotations

    # If yellow is detected, highlight the yellow regions
    if yellow_detected:
        # Highlight yellow regions in the original image
        image_with_highlight = cv2.bitwise_and(image, image, mask=yellow_mask)
        # Overlay the highlighted yellow region on the annotated image
        image_with_highlight = cv2.addWeighted(annotated_image, 1, image_with_highlight, 0.5, 0)
    else:
        image_with_highlight = annotated_image

    # Display the annotated image in the Streamlit app
    st.image(image_with_highlight, channels='BGR', use_container_width=True)

    # Check for 'helmet' or 'no_helmet' class in the results
    detected_classes = results[0].names  # Get class names of detected objects
    helmet_detected = False
    no_helmet_detected = False

    # Loop through the detections and focus only on the "helmet" class
    for class_id, confidence in zip(results[0].boxes.cls, results[0].boxes.conf):
        if detected_classes[int(class_id)] == "helmet" and confidence > 0.5:
            helmet_detected = True
        elif detected_classes[int(class_id)] == "no_helmet" and confidence > 0.5:
            no_helmet_detected = True

    # Display pop-up style messages based on the detections
    if helmet_detected or yellow_detected:
        st.success('Helmet is present. No issues detected.')
    else:
        st.error('No helmet, ask to wear helmet.', icon="⚠️")

# Main Streamlit Interface
def main():
    st.title('Helmet Detection on Construction Sites')

    # Load YOLOv8 model
    model = load_yolov8_model()
    st.success('YOLOv8 Model Loaded.')

    # Upload Image Section
    uploaded_image = st.file_uploader("Upload an image of the worker", type=["jpg", "png", "jpeg"])
    
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        # Detect helmet on uploaded image
        detect_helmet_on_uploaded_image(model, uploaded_image)
    
if __name__ == "__main__":
    main()
