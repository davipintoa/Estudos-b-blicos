
import sys
from pypdf import PdfReader

def extract_toc(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        print(f"Processing: {pdf_path}")
        print(f"Total Pages: {len(reader.pages)}")
        
        print("\n--- Table of Contents ---")
        # pypdf's outline implementation returns a nested list of Destination objects and lists.
        # We need to recursively traverse it.
        
        def recurse_outline(outline, level=0):
            for item in outline:
                if isinstance(item, list):
                    recurse_outline(item, level + 1)
                else:
                    try:
                        title = item.title
                        # page_number from get_destination_page_number is 0-based
                        page_num = reader.get_destination_page_number(item) + 1 
                        indent = "  " * level
                        print(f"{indent}- Page {page_num}: {title}")
                    except Exception as e:
                        # Some outline items might be broken or point to external links
                        continue

        if reader.outline:
            recurse_outline(reader.outline)
        else:
            print("No outline found in this PDF.")

    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_toc(sys.argv[1])
    else:
        # Default for the user's current context
        extract_toc("Full_doc/Complete-Babylonian-Talmud-English.pdf")
