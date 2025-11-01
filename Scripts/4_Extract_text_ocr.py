import os
import cv2
import easyocr
from ultralytics import YOLO
import pandas as pd
import mysql.connector

# -------------------------------
# 1️⃣ Load YOLO model
# -------------------------------
model = YOLO(r'C:\Users\Anjali\OneDrive\Desktop\DS_project\best (2).pt')

# -------------------------------
# 2️⃣ Define image folder
# -------------------------------
image_dir = r'C:\Users\Anjali\OneDrive\Desktop\DS_project\new_invoice_images'
image_paths = [os.path.join(image_dir, img)
               for img in os.listdir(image_dir)
               if img.lower().endswith(('.jpg', '.png', '.jpeg'))]

# -------------------------------
# 3️⃣ Initialize OCR reader
# -------------------------------
reader = easyocr.Reader(['en'])

# -------------------------------
# 4️⃣ Setup CSV for Progress Tracking
# -------------------------------
progress_csv = r'C:\Users\Anjali\OneDrive\Desktop\DS_project\invoice_progress1.csv'

if os.path.exists(progress_csv):
    df_existing = pd.read_csv(progress_csv)
    processed_files = set(df_existing['image_name'].tolist())
else:
    df_existing = pd.DataFrame(columns=[
        'image_name', 'invoice_id', 'customer_id', 'billing_address', 'shipping_address',
        'date', 'due_date', 'product', 'amount', 'subtotal', 'tax_due', 'total'
    ])
    processed_files = set()

# -------------------------------
# 5️⃣ Process images with auto-save
# -------------------------------
for img_path in image_paths:
    image_name = os.path.basename(img_path)
    if image_name in processed_files:
        print(f"Skipping already processed: {image_name} ✅")
        continue

    print(f"\nProcessing: {image_name}")
    try:
        image = cv2.imread(img_path)
        result = model(img_path)[0]

        invoice_data = {
            "image_name": image_name,
            "invoice_id": "", "customer_id": "",
            "billing_address": "", "shipping_address": "",
            "date": "", "due_date": "",
            "subtotal": "", "tax_due": "", "total": "",
            "products": []
        }

        # Collect detections
        detections = []
        for box, c in zip(result.boxes.xyxy, result.boxes.cls):
            label = model.names[int(c.item())]
            x_min, y_min, x_max, y_max = [int(v) for v in box]
            cropped = image[y_min:y_max, x_min:x_max]
            ocr_results = reader.readtext(cropped)
            extracted_text = " ".join([text for (_, text, _) in ocr_results]).strip()
            if extracted_text:
                detections.append({
                    "label": label,
                    "text": extracted_text,
                    "y": y_min,
                    "x": x_min
                })

        # Product–Amount pairing
        products = [d for d in detections if d["label"] == "product"]
        amounts = [d for d in detections if d["label"] == "amount"]
        products.sort(key=lambda x: x["y"])
        amounts.sort(key=lambda x: x["y"])

        for p in products:
            closest_amount = None
            min_diff = float('inf')
            for a in amounts:
                diff = abs(p["y"] - a["y"])
                if diff < min_diff:
                    min_diff = diff
                    closest_amount = a["text"]
            invoice_data["products"].append({
                "product": p["text"],
                "amount": closest_amount if closest_amount else ""
            })

        # Other fields
        for d in detections:
            if d["label"] in invoice_data and d["label"] != "products":
                invoice_data[d["label"]] = d["text"]

        # Build rows for this image
        rows = []
        for prod_pair in invoice_data["products"]:
            row = {
                "image_name": invoice_data["image_name"],
                "invoice_id": invoice_data["invoice_id"],
                "customer_id": invoice_data["customer_id"],
                "billing_address": invoice_data["billing_address"],
                "shipping_address": invoice_data["shipping_address"],
                "date": invoice_data["date"],
                "due_date": invoice_data["due_date"],
                "product": prod_pair["product"],
                "amount": prod_pair["amount"],
                "subtotal": invoice_data["subtotal"],
                "tax_due": invoice_data["tax_due"],
                "total": invoice_data["total"]
            }
            rows.append(row)

        # Save this image’s results immediately
        df_temp = pd.DataFrame(rows)
        df_temp.to_csv(progress_csv, mode='a',
                       header=not os.path.exists(progress_csv), index=False)

        print(f"✅ Saved progress for: {image_name}")

    except Exception as e:
        print(f"❌ Error in {image_name}: {e}")
        continue

print("\n✅ All images processed or saved in progress CSV.")

# -------------------------------
# 6️⃣ Load CSV and clean types
# -------------------------------
df = pd.read_csv(progress_csv)
numeric_cols = ['amount', 'subtotal', 'tax_due', 'total']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
df['due_date'] = pd.to_datetime(df['due_date'], errors='coerce').dt.date

# -------------------------------
# 7️⃣ Insert into MySQL (fixed version)
# -------------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin@123",
        database="invoice_db"
    )
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INT AUTO_INCREMENT PRIMARY KEY,
        image_name VARCHAR(255),
        invoice_id VARCHAR(100),
        customer_id VARCHAR(100),
        billing_address TEXT,
        shipping_address TEXT,
        date DATE,
        due_date DATE,
        product VARCHAR(255),
        amount DECIMAL(10,2),
        subtotal DECIMAL(10,2),
        tax_due DECIMAL(10,2),
        total DECIMAL(10,2)
    )
    """)

    # ✅ Replace NaN or NaT with None (SQL NULL)
    df = df.where(pd.notnull(df), None)

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO invoices (
                image_name, invoice_id, customer_id, billing_address, shipping_address,
                date, due_date, product, amount, subtotal, tax_due, total
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row['image_name'],
            row['invoice_id'],
            row['customer_id'],
            row['billing_address'],
            row['shipping_address'],
            row['date'],
            row['due_date'],
            row['product'],
            float(row['amount']) if row['amount'] is not None else 0.0,
            float(row['subtotal']) if row['subtotal'] is not None else 0.0,
            float(row['tax_due']) if row['tax_due'] is not None else 0.0,
            float(row['total']) if row['total'] is not None else 0.0
        ))

    conn.commit()
    print("✅ All data inserted into MySQL successfully!")

except Exception as e:
    print(f"❌ MySQL Error: {e}")

finally:
    if conn.is_connected():
        conn.close()


