import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from fpdf import FPDF


def convert_pdf_to_images(pdf_path):
    return convert_from_path(pdf_path, poppler_path=r"D:\\Applications\\poppler-23.11.0\\Library\\bin")


def extract_text_from_image(image):
    return pytesseract.image_to_string(image)


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()


def process_pdfs(input_folder, output_folder):
    for pdf_file in os.listdir(input_folder):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, pdf_file)
            images = convert_pdf_to_images(pdf_path)
            pdf = PDF()
            for i, image in enumerate(images):
                text = extract_text_from_image(image)
                # Replace non-Latin characters
                text = text.encode('latin-1', 'replace').decode('latin-1')
                pdf.add_page()
                pdf.chapter_title(f'Page {i+1}')
                pdf.chapter_body(text)
            pdf.output(os.path.join(output_folder, f'{pdf_file[:-4]}.pdf'))


# Set the directories
input_folder = './input'
output_folder = './output'

# Check if output directory exists, if not create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process the PDFs
process_pdfs(input_folder, output_folder)
