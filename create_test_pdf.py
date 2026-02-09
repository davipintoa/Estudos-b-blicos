
from pypdf import PdfWriter, PageObject

def create_dummy_pdf(filename, pages):
    writer = PdfWriter()
    for _ in range(pages):
        # Create a blank letter size page (612 x 792 points)
        writer.add_page(PageObject.create_blank_page(width=612, height=792))
    
    with open(filename, "wb") as f:
        writer.write(f)
    print(f"Created dummy PDF: {filename} with {pages} blank pages.")

if __name__ == "__main__":
    create_dummy_pdf("test_document.pdf", 20)
