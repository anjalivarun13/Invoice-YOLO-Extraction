# import os, random
# from datetime import datetime, timedelta
# from faker import Faker
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import mm
# from reportlab.lib import colors

# fake = Faker()
# OUTPUT_DIR = "invoices"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # --- Company static details ---
# COMPANY_NAME = "ABC Solutions Pvt. Ltd."
# COMPANY_ADDRESS = "123, Business Street, Mumbai, MH 400001"
# COMPANY_PHONE = "022-1234567890"
# COMPANY_WEBSITE = "www.abcsolutions.com"

# def create_invoice_pdf(i):
#     width, height = A4
#     c = canvas.Canvas(os.path.join(OUTPUT_DIR, f"invoice_{i:04d}.pdf"), pagesize=A4)

#     # --- HEADER ---
#     c.setFillColorRGB(0.2, 0.4, 0.7)
#     c.rect(0, height-40*mm, width, 40*mm, fill=1, stroke=0)
#     c.setFillColor(colors.white)
#     c.setFont("Helvetica-Bold", 18)
#     c.drawString(20*mm, height-25*mm, COMPANY_NAME)
#     c.setFont("Helvetica", 9)
#     c.drawString(20*mm, height-32*mm, COMPANY_ADDRESS)
#     c.drawString(20*mm, height-37*mm, f"Phone: {COMPANY_PHONE} | Website: {COMPANY_WEBSITE}")
    
#     # Invoice title
#     c.setFont("Helvetica-Bold", 20)
#     c.drawRightString(width-20*mm, height-25*mm, "INVOICE")

#     # --- Invoice details ---
#     invoice_no = f"{1000+i}"
#     cust_id = f"CUST-{random.randint(100,999)}"
    
#     # Generate a unique realistic date within last 6 months
#     start_date = datetime.now() - timedelta(days=180)
#     date = start_date + timedelta(days=random.randint(0, 180))
#     date = date.date()
#     due_date = date + timedelta(days=30)

#     x_right = width-70*mm
#     y_top = height-50*mm
#     c.setFillColor(colors.black)
#     c.setFont("Helvetica", 9)
#     c.drawString(x_right, y_top, f"DATE: {date.isoformat()}")
#     c.drawString(x_right, y_top-6*mm, f"INVOICE #: {invoice_no}")
#     c.drawString(x_right, y_top-12*mm, f"CUSTOMER ID: {cust_id}")
#     c.drawString(x_right, y_top-18*mm, f"DUE DATE: {due_date.isoformat()}")

#     # --- BILL TO ---
#     bill_y = height-65*mm
#     c.setFillColorRGB(0.2, 0.4, 0.7)
#     c.rect(20*mm, bill_y, 60*mm, 8*mm, fill=1, stroke=0)
#     c.setFillColor(colors.white)
#     c.setFont("Helvetica-Bold", 9)
#     c.drawString(22*mm, bill_y+2*mm, "BILL TO")
    
#     c.setFillColor(colors.black)
#     c.setFont("Helvetica", 9)
#     c.drawString(20*mm, bill_y-6*mm, fake.name())
#     c.drawString(20*mm, bill_y-12*mm, fake.company())
#     c.drawString(20*mm, bill_y-18*mm, fake.street_address())
#     c.drawString(20*mm, bill_y-24*mm, f"{fake.city()}, {fake.state_abbr()} {fake.postcode()}")
#     c.drawString(20*mm, bill_y-30*mm, fake.phone_number())

#     # --- SHIP TO ---
#     ship_y = bill_y-35*mm
#     c.setFillColorRGB(0.2, 0.4, 0.7)
#     c.rect(20*mm, ship_y, 60*mm, 8*mm, fill=1, stroke=0)
#     c.setFillColor(colors.white)
#     c.setFont("Helvetica-Bold", 9)
#     c.drawString(22*mm, ship_y+2*mm, "SHIP TO")

#     c.setFillColor(colors.black)
#     c.setFont("Helvetica", 9)
#     c.drawString(20*mm, ship_y-6*mm, fake.name())
#     c.drawString(20*mm, ship_y-12*mm, fake.company())
#     c.drawString(20*mm, ship_y-18*mm, fake.street_address())
#     c.drawString(20*mm, ship_y-24*mm, f"{fake.city()}, {fake.state_abbr()} {fake.postcode()}")
#     c.drawString(20*mm, ship_y-30*mm, fake.phone_number())

#     # --- TABLE HEADER ---
#     table_y = ship_y-40*mm
#     c.setFillColorRGB(0.2, 0.4, 0.7)
#     c.rect(20*mm, table_y, width-40*mm, 8*mm, fill=1, stroke=0)
#     c.setFillColor(colors.white)
#     c.setFont("Helvetica-Bold", 9)
#     c.drawString(22*mm, table_y+2*mm, "DESCRIPTION")
#     c.drawString(122*mm, table_y+2*mm, "TAXED")
#     c.drawString(152*mm, table_y+2*mm, "AMOUNT")

#     # --- LINE ITEMS ---
#     c.setFillColor(colors.black)
#     c.setFont("Helvetica", 9)
#     col_x = [20*mm, 120*mm, 150*mm, 190*mm]
#     y = table_y - 10*mm
#     row_height = 10*mm

#     subtotal, taxable = 0, 0
#     num_items = random.randint(3, 6)
#     for _ in range(num_items):
#         desc = fake.bs().capitalize()
#         amount = round(random.uniform(50, 500), 2)
#         taxed = random.choice([True, False])
        
#         # Grid
#         c.line(col_x[0], y+row_height/2, col_x[-1], y+row_height/2)
#         c.line(col_x[0], y-row_height/2, col_x[-1], y-row_height/2)
#         for cx in col_x:
#             c.line(cx, y-row_height/2, cx, y+row_height/2)

#         # Text
#         c.drawString(col_x[0]+2*mm, y, desc[:40])
#         if taxed:
#             c.drawCentredString((col_x[1]+col_x[2])//2, y, "X")
#             taxable += amount
#         c.drawRightString(col_x[-1]-2*mm, y, f"{amount:.2f}")
#         subtotal += amount
#         y -= row_height

#     # Bottom line
#     c.line(col_x[0], y-row_height/2, col_x[-1], y-row_height/2)

#     # --- TOTALS ---
#     tax_rate = 0.0625
#     tax_due = round(taxable*tax_rate, 2)
#     total = subtotal + tax_due
#     totals_y = 70*mm
#     c.setFont("Helvetica", 9)
#     c.drawRightString(190*mm, totals_y, f"Subtotal: {subtotal:.2f}")
#     c.drawRightString(190*mm, totals_y-6*mm, f"Taxable: {taxable:.2f}")
#     c.drawRightString(190*mm, totals_y-12*mm, f"Tax rate: {tax_rate*100:.2f}%")
#     c.drawRightString(190*mm, totals_y-18*mm, f"Tax due: {tax_due:.2f}")
#     c.setFont("Helvetica-Bold", 11)
#     c.drawRightString(190*mm, totals_y-30*mm, f"TOTAL: ${total:.2f}")

#     # --- COMMENTS ---
#     c.setFillColorRGB(0.2,0.4,0.7)
#     c.rect(20*mm, 55*mm, 80*mm, 8*mm, fill=1, stroke=0)
#     c.setFillColor(colors.white)
#     c.setFont("Helvetica-Bold", 9)
#     c.drawString(22*mm, 57*mm, "OTHER COMMENTS")
#     c.setFillColor(colors.black)
#     c.setFont("Helvetica", 8)
#     c.drawString(22*mm, 50*mm, "1. Total payment due in 30 days")
#     c.drawString(22*mm, 44*mm, "2. Please include the invoice number on your check")

#     # --- FOOTER ---
#     c.setFont("Helvetica-Oblique", 8)
#     c.drawString(20*mm, 30*mm, "If you have any questions about this invoice, please contact")
#     c.drawString(20*mm, 25*mm, "Thank You For Your Business!")

#     c.showPage()
#     c.save()


# def main(n=2000):
#     for i in range(1, n+1):
#         create_invoice_pdf(i)
#         if i % 100 == 0:
#             print(f"Generated {i} invoices...")
#     print("✅ Done. All invoices saved in:", os.path.abspath(OUTPUT_DIR))


# if __name__ == "__main__":
#     main(2000)


PRODUCTS = [
    {"description": "Web Hosting (1 Year)", "price": 120.00, "taxed": True},
    {"description": "Domain Registration", "price": 15.99, "taxed": True},
    {"description": "SEO Optimization", "price": 299.00, "taxed": False},
    {"description": "Email Marketing Package", "price": 199.99, "taxed": False},
    {"description": "E-commerce Website Setup", "price": 999.00, "taxed": True},
    {"description": "Cloud Storage 100GB", "price": 49.00, "taxed": True},
    {"description": "SSL Certificate (1 Year)", "price": 59.99, "taxed": True},
    {"description": "WordPress Installation", "price": 79.00, "taxed": True},
    {"description": "Mobile App Development", "price": 1500.00, "taxed": True},
    {"description": "Software Maintenance Plan", "price": 399.00, "taxed": True},
    {"description": "Custom Logo Design", "price": 89.00, "taxed": False},
    {"description": "IT Support (per hour)", "price": 60.00, "taxed": True},
    {"description": "Firewall Setup", "price": 250.00, "taxed": True},
    {"description": "Network Audit", "price": 180.00, "taxed": True},
    {"description": "Digital Marketing Plan", "price": 350.00, "taxed": False},
    {"description": "Remote Desktop Setup", "price": 120.00, "taxed": True},
    {"description": "Antivirus Installation", "price": 35.00, "taxed": True},
    {"description": "Data Recovery Service", "price": 220.00, "taxed": True},
    {"description": "Database Optimization", "price": 300.00, "taxed": True},
    {"description": "Server Backup Configuration", "price": 275.00, "taxed": True},
    {"description": "Cloud Migration Service", "price": 1200.00, "taxed": True},
    {"description": "Website Audit", "price": 95.00, "taxed": False},
    {"description": "Analytics Setup", "price": 135.00, "taxed": False},
    {"description": "API Integration", "price": 450.00, "taxed": True},
    {"description": "Payment Gateway Setup", "price": 225.00, "taxed": True},
    {"description": "On-site Technician Visit", "price": 90.00, "taxed": True},
    {"description": "Router Configuration", "price": 45.00, "taxed": True},
    {"description": "IT Infrastructure Assessment", "price": 600.00, "taxed": True},
    {"description": "CRM Customization", "price": 550.00, "taxed": True},
    {"description": "UX/UI Consulting", "price": 320.00, "taxed": False},
    {"description": "Project Management", "price": 700.00, "taxed": False},
    {"description": "VPN Setup", "price": 85.00, "taxed": True},
    {"description": "Office 365 Setup", "price": 180.00, "taxed": True},
    {"description": "Cloud Email Configuration", "price": 110.00, "taxed": True},
    {"description": "Laptop Repair Service", "price": 150.00, "taxed": True},
    {"description": "Printer Setup", "price": 40.00, "taxed": True},
    {"description": "Wireless Network Installation", "price": 350.00, "taxed": True},
    {"description": "Data Encryption Service", "price": 290.00, "taxed": True},
    {"description": "Website Redesign", "price": 750.00, "taxed": False},
    {"description": "Online Security Assessment", "price": 400.00, "taxed": True},
    {"description": "Chatbot Integration", "price": 550.00, "taxed": True},
    {"description": "Inventory Management System", "price": 1250.00, "taxed": True},
    {"description": "Cloud Resource Optimization", "price": 880.00, "taxed": True},
    {"description": "Monthly Website Maintenance", "price": 90.00, "taxed": True},
    {"description": "Client Portal Setup", "price": 480.00, "taxed": True},
    {"description": "Mobile Responsiveness Fix", "price": 240.00, "taxed": True},
    {"description": "Load Balancer Configuration", "price": 390.00, "taxed": True},
    {"description": "Network Cable Installation", "price": 180.00, "taxed": True},
    {"description": "Content Management Training", "price": 200.00, "taxed": False},
    {"description": "Backup Monitoring Service", "price": 130.00, "taxed": True},
]


CUSTOMERS = [
    {"name": "John Doe", "company": "Doe Enterprises", "address": "101 First Street", "city": "New York", "state": "NY", "zip": "10001", "phone": "212-555-1234"},
    {"name": "Jane Smith", "company": "Smith Consulting", "address": "202 Market Ave", "city": "San Francisco", "state": "CA", "zip": "94105", "phone": "415-555-9876"},
    {"name": "Emily Johnson", "company": "Johnson Tech", "address": "303 Innovation Blvd", "city": "Austin", "state": "TX", "zip": "73301", "phone": "512-555-6543"},
    {"name": "Michael Brown", "company": "Brown Solutions", "address": "404 Commerce Rd", "city": "Chicago", "state": "IL", "zip": "60616", "phone": "312-555-4321"},
    {"name": "Lisa White", "company": "White & Co.", "address": "505 Central Plaza", "city": "Seattle", "state": "WA", "zip": "98101", "phone": "206-555-7654"},
    {"name": "David Green", "company": "Green Innovations", "address": "606 Sunset Blvd", "city": "Los Angeles", "state": "CA", "zip": "90028", "phone": "310-555-8899"},
    {"name": "Olivia Harris", "company": "Harris Group", "address": "707 Tech Park", "city": "Denver", "state": "CO", "zip": "80202", "phone": "303-555-9087"},
    {"name": "Ethan Moore", "company": "Moore Ventures", "address": "808 North Loop", "city": "Houston", "state": "TX", "zip": "77002", "phone": "713-555-2301"},
    {"name": "Sophia Clark", "company": "Clark Design Studio", "address": "909 Art District", "city": "Portland", "state": "OR", "zip": "97209", "phone": "503-555-5566"},
    {"name": "Daniel Lewis", "company": "Lewis Logistics", "address": "1010 Freight Way", "city": "Atlanta", "state": "GA", "zip": "30303", "phone": "404-555-2121"},
    {"name": "Ava Walker", "company": "Walker Strategies", "address": "1111 Union Square", "city": "Boston", "state": "MA", "zip": "02108", "phone": "617-555-7890"},
    {"name": "James Hall", "company": "Hall & Associates", "address": "1212 Broadway", "city": "Nashville", "state": "TN", "zip": "37203", "phone": "615-555-6789"},
    {"name": "Mia Young", "company": "Young Tech Services", "address": "1313 Main Street", "city": "Phoenix", "state": "AZ", "zip": "85001", "phone": "602-555-4521"},
    {"name": "Benjamin Allen", "company": "Allen Media", "address": "1414 Film Row", "city": "Los Angeles", "state": "CA", "zip": "90014", "phone": "310-555-7788"},
    {"name": "Charlotte Scott", "company": "Scott Interiors", "address": "1515 Home Blvd", "city": "Miami", "state": "FL", "zip": "33101", "phone": "305-555-3344"},
    {"name": "Logan Adams", "company": "Adams Real Estate", "address": "1616 Skyline Ave", "city": "Dallas", "state": "TX", "zip": "75201", "phone": "214-555-6677"},
    {"name": "Grace Nelson", "company": "Nelson Solutions", "address": "1717 Startup Ln", "city": "Raleigh", "state": "NC", "zip": "27601", "phone": "919-555-1133"},
    {"name": "William Baker", "company": "Baker Finance Group", "address": "1818 Wealth Blvd", "city": "Charlotte", "state": "NC", "zip": "28202", "phone": "704-555-9911"},
    {"name": "Isabella Rivera", "company": "Rivera Communications", "address": "1919 Comms Dr", "city": "Orlando", "state": "FL", "zip": "32801", "phone": "407-555-4466"},
    {"name": "Lucas Carter", "company": "Carter AI Labs", "address": "2020 AI Plaza", "city": "San Jose", "state": "CA", "zip": "95110", "phone": "408-555-2211"}
]

import os, random
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

OUTPUT_DIR = "new_invoices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Company static details ---
COMPANY_NAME = "ABC Solutions Pvt. Ltd."
COMPANY_ADDRESS = "123, Business Street, Mumbai, MH 400001"
COMPANY_PHONE = "022-1234567890"
COMPANY_WEBSITE = "www.abcsolutions.com"

def create_invoice_pdf(i):
    width, height = A4
    c = canvas.Canvas(os.path.join(OUTPUT_DIR, f"invoice_{i:04d}.pdf"), pagesize=A4)

    # --- HEADER ---
    c.setFillColorRGB(0.2, 0.4, 0.7)
    c.rect(0, height-40*mm, width, 40*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(20*mm, height-25*mm, COMPANY_NAME)
    c.setFont("Helvetica", 9)
    c.drawString(20*mm, height-32*mm, COMPANY_ADDRESS)
    c.drawString(20*mm, height-37*mm, f"Phone: {COMPANY_PHONE} | Website: {COMPANY_WEBSITE}")
    
    # Invoice title
    c.setFont("Helvetica-Bold", 20)
    c.drawRightString(width-20*mm, height-25*mm, "INVOICE")

    # --- Invoice details ---
    invoice_no = f"{1000+i}"
    cust_id = f"CUST-{random.randint(100,999)}"
    
    # Generate a unique realistic date within last 6 months
    start_date = datetime.now() - timedelta(days=180)
    date = start_date + timedelta(days=random.randint(0, 180))
    date = date.date()
    due_date = date + timedelta(days=30)

    x_right = width-70*mm
    y_top = height-50*mm
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawString(x_right, y_top, f"DATE: {date.isoformat()}")
    c.drawString(x_right, y_top-6*mm, f"INVOICE #: {invoice_no}")
    c.drawString(x_right, y_top-12*mm, f"CUSTOMER ID: {cust_id}")
    c.drawString(x_right, y_top-18*mm, f"DUE DATE: {due_date.isoformat()}")

        # Pick a random customer
    customer = random.choice(CUSTOMERS)

    # --- BILL TO ---
    bill_y = height-65*mm
    c.setFillColorRGB(0.2, 0.4, 0.7)
    c.rect(20*mm, bill_y, 60*mm, 8*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(22*mm, bill_y+2*mm, "BILL TO")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawString(20*mm, bill_y-6*mm, customer["name"])
    c.drawString(20*mm, bill_y-12*mm, customer["company"])
    c.drawString(20*mm, bill_y-18*mm, customer["address"])
    c.drawString(20*mm, bill_y-24*mm, f"{customer['city']}, {customer['state']} {customer['zip']}")
    c.drawString(20*mm, bill_y-30*mm, customer["phone"])

    # --- SHIP TO (Same as BILL TO) ---
    ship_y = bill_y-35*mm
    c.setFillColorRGB(0.2, 0.4, 0.7)
    c.rect(20*mm, ship_y, 60*mm, 8*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(22*mm, ship_y+2*mm, "SHIP TO")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawString(20*mm, ship_y-6*mm, customer["name"])
    c.drawString(20*mm, ship_y-12*mm, customer["company"])
    c.drawString(20*mm, ship_y-18*mm, customer["address"])
    c.drawString(20*mm, ship_y-24*mm, f"{customer['city']}, {customer['state']} {customer['zip']}")
    c.drawString(20*mm, ship_y-30*mm, customer["phone"])

    # --- TABLE HEADER ---
    table_y = ship_y-40*mm
    c.setFillColorRGB(0.2, 0.4, 0.7)
    c.rect(20*mm, table_y, width-40*mm, 8*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(22*mm, table_y+2*mm, "DESCRIPTION")
    c.drawString(122*mm, table_y+2*mm, "TAXED")
    c.drawString(152*mm, table_y+2*mm, "AMOUNT")

    # --- LINE ITEMS ---
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    col_x = [20*mm, 120*mm, 150*mm, 190*mm]
    y = table_y - 10*mm
    row_height = 10*mm

    subtotal, taxable = 0, 0
    items = random.sample(PRODUCTS, k=random.randint(3, min(6, len(PRODUCTS))))
    for item in items:
        desc = item["description"]
        amount = item["price"]
        taxed = item["taxed"]
        
        # Grid
        c.line(col_x[0], y+row_height/2, col_x[-1], y+row_height/2)
        c.line(col_x[0], y-row_height/2, col_x[-1], y-row_height/2)
        for cx in col_x:
            c.line(cx, y-row_height/2, cx, y+row_height/2)

        # Text
        c.drawString(col_x[0]+2*mm, y, desc[:40])
        if taxed:
            c.drawCentredString((col_x[1]+col_x[2])//2, y, "X")
            taxable += amount
        c.drawRightString(col_x[-1]-2*mm, y, f"{amount:.2f}")
        subtotal += amount
        y -= row_height

    # Bottom line
    c.line(col_x[0], y-row_height/2, col_x[-1], y-row_height/2)

    # --- TOTALS ---
    tax_rate = 0.0625
    tax_due = round(taxable*tax_rate, 2)
    total = subtotal + tax_due
    totals_y = 70*mm
    c.setFont("Helvetica", 9)
    c.drawRightString(190*mm, totals_y, f"Subtotal: {subtotal:.2f}")
    c.drawRightString(190*mm, totals_y-6*mm, f"Taxable: {taxable:.2f}")
    c.drawRightString(190*mm, totals_y-12*mm, f"Tax rate: {tax_rate*100:.2f}%")
    c.drawRightString(190*mm, totals_y-18*mm, f"Tax due: {tax_due:.2f}")
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(190*mm, totals_y-30*mm, f"TOTAL: ${total:.2f}")

    # --- COMMENTS ---
    c.setFillColorRGB(0.2,0.4,0.7)
    c.rect(20*mm, 55*mm, 80*mm, 8*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(22*mm, 57*mm, "OTHER COMMENTS")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8)
    c.drawString(22*mm, 50*mm, "1. Total payment due in 30 days")
    c.drawString(22*mm, 44*mm, "2. Please include the invoice number on your check")

    # --- FOOTER ---
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(20*mm, 30*mm, "If you have any questions about this invoice, please contact")
    c.drawString(20*mm, 25*mm, "Thank You For Your Business!")

    c.showPage()
    c.save()


def main(n=2000):
    for i in range(1, n+1):
        create_invoice_pdf(i)
        if i % 100 == 0:
            print(f"Generated {i} invoices...")
    print("✅ Done. All invoices saved in:", os.path.abspath(OUTPUT_DIR))


if __name__ == "__main__":
    main(2000)