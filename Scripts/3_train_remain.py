from ultralytics import YOLO

# Load the trained model
model = YOLO(r"C:\Users\Anjali\OneDrive\Desktop\DS_project\best (2).pt")

# Run inference on images
results = model(r"C:\Users\Anjali\OneDrive\Desktop\DS_project\new_invoice_images")
