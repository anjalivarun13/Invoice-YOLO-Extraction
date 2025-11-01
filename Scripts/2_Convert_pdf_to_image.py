import os
from pdf2image import convert_from_path

PDF_DIR = "new_invoices"
IMG_DIR = "new_invoice_images"
os.makedirs(IMG_DIR, exist_ok=True)

def convert_pdfs_to_images():
    for pdf_file in os.listdir(PDF_DIR):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, pdf_file)
            # Convert PDF to images (1 per page, here invoices are 1 page)
            images = convert_from_path(pdf_path, dpi=300)  # high quality

            for page_num, img in enumerate(images):
                img_filename = pdf_file.replace(".pdf", f"_page{page_num+1}.png")
                img_path = os.path.join(IMG_DIR, img_filename)
                img.save(img_path, "PNG")
            print(f"Converted {pdf_file} to image(s).")

    print("✅ All PDFs converted to images in:", os.path.abspath(IMG_DIR))


if __name__ == "__main__":
    convert_pdfs_to_images()
