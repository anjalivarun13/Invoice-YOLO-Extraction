
# 🧾 Automated Invoice Data Extraction and Dashboard Using YOLO, Python, and Power BI




## 📘 Project Overview
This project demonstrates a complete end-to-end pipeline for automating invoice data extraction using YOLO object detection, OCR (EasyOCR), and data visualization in Power BI.

It includes:

1.Generating synthetic invoice PDFs using Python.

2.Detecting and extracting key invoice information using YOLO and OCR

3.Storing the extracted structured data into a MySQL database

4.Connecting Power BI to MySQL for creating an interactive analytics dashboard


## 🧩 Project Workflow
## Step 1: Generate Synthetic Invoice PDFs

1.Created 2000 sample invoice PDFs programmatically using the ReportLab library.

2.Each PDF contains random invoice details such as:

image_name,invoice_id,customer_id,billing_address,shipping_address,date,due_date,product,amount,subtotal,tax_due,total

3.Libraries Used:

    import os, random
    from datetime import datetime, timedelta
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors

## Step 2: Convert PDF to Images

1.Converted all generated invoices (PDFs) into images for YOLO processing.

2.Library Used:

    from pdf2image import convert_from_path


Each page was saved as a .jpg file for annotation and model training.

## Step 3: Annotation Using Roboflow

1.Uploaded 30 sample invoice images to Roboflow.

2.Annotated key fields (like Invoice Number, Date, Total Amount, etc.).

3.Exported the dataset for YOLO training.

## Step 4: Model Training in Google Colab

Trained a YOLO model using Ultralytics in Google Colab.

Process:

1.Imported Roboflow dataset into Colab.

2.Trained model using the YOLOv8 framework (ultralytics library).

3.Adjusted epochs, batch size, and image size for best accuracy.

Libraries Used:

    !pip install roboflow ultralytics   


After training, downloaded the best.pt file for inference.

## Step 5: Object Detection on Invoice Images

Used the trained YOLO model (best.pt) to detect text regions in remaining invoice images.

## Step 6: Text Extraction Using EasyOCR

Extracted detected text from invoice images using the EasyOCR library.

Library Used:

    import easyocr


All extracted text was saved in a structured CSV file for further processing.

## Step 7: Data Cleaning Using Pandas

Cleaned and preprocessed the extracted CSV file using Pandas:

    1.Removed nulls

    2.Handled missing values

    3.Corrected column names and data types

Library Used:

    import pandas as pd

## Step 8: Store Data into MySQL Database

Connected Python with MySQL using SQLAlchemy and PyMySQL to store the cleaned invoice data.

Libraries Used:

    import pymysql
    from sqlalchemy import create_engine
    from sqlalchemy.exc import OperationalError


Stored cleaned data into a MySQL table for analytics.

## Step 9: Data Analysis in MySQL

Performed SQL queries for:

1.Aggregating invoice totals

2.Finding Top perfroming product




## Step 10: Power BI Dashboard

1.Connected Power BI directly to MySQL Database.

2.Imported the cleaned invoice dataset.

3.Created a dashboard .
## 🛠️ Technologies & Tools Used
| Category         | Tools / Libraries                |
| ---------------- | -------------------------------- |
| PDF Generation   | ReportLab                        |
| Image Conversion | pdf2image                        |
| Annotation       | Roboflow                         |
| Model Training   | Ultralytics YOLOv8, Google Colab |
| OCR              | EasyOCR                          |
| Data Cleaning    | Pandas                           |
| Database         | MySQL, SQLAlchemy, PyMySQL       |
| Visualization    | Power BI                         |

## 📊 End Output
✅ Automated extraction of invoice data

✅ Structured storage in MySQL

✅ Interactive Power BI dashboard with real-time insights


## 👩‍💻 Author
**Anjali Varun**  

🔗 [LinkedIn](https://www.linkedin.com/in/your-linkedin-username) | [GitHub](https://github.com/anjalivarun13) 