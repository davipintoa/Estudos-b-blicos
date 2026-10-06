
import os
import sys
from typing import List, Tuple
from pypdf import PdfReader, PdfWriter

# Increase recursion depth for deep PDF structures
sys.setrecursionlimit(20000)

def split_pdf(input_path: str, ranges: List[Tuple[int, int, str]], output_dir: str = "."):
    """
    Splits a PDF file into multiple shorter PDF files based on the provided page ranges.

    Args:
        input_path (str): The path to the source PDF file.
        ranges (List[Tuple[int, int, str]]): A list of tuples, where each tuple contains:
            - start_page (int): The starting page number (1-based index).
            - end_page (int): The ending page number (1-based index, inclusive).
            - section_name (str): The name for the output section (used in filename).
        output_dir (str): Directory to save the output files. w
    """
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    try:
        # Open the PDF file in binary mode
        # PdfReader creates an object that represents the PDF file.
        # It reads the file structure but does not load all pages into memory.
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        print(f"Opened '{input_path}' with {total_pages} pages.")

        for i, (start_page, end_page, section_name) in enumerate(ranges, start=1):
            # Validate ranges
            if start_page < 1 or end_page > total_pages or start_page > end_page:
                print(f"Error: Invalid range specified for '{section_name}': {start_page}-{end_page}. Skipping.")
                continue

            # distinct, safe filename
            safe_name = "".join([c for c in section_name if c.isalpha() or c.isdigit() or c in (' ', '-', '_', '.')]).strip()
            # If section_name already ends in .pdf, don't add it again
            if safe_name.lower().endswith(".pdf"):
                safe_name = safe_name[:-4]
            
            # Add numeric prefix (e.g., "01. Section Name.pdf")
            final_filename = f"{i:02d}. {safe_name}.pdf"
                
            output_filename = os.path.join(output_dir, final_filename)
            
            print(f"Processing section: {section_name} (Pages {start_page}-{end_page})...")
            
            writer = PdfWriter()

            # pypdf uses 0-based indexing for pages
            # Convert 1-based [start, end] to 0-based [start-1, end)
            # However, range in python is exclusive at the end, so we want range(start-1, end)
            # because end-1 is the index of the last page we want.
            
            # Example: Pages 1 to 3. 
            # 1-based: 1, 2, 3
            # 0-based indices: 0, 1, 2
            # range(0, 3) -> 0, 1, 2. Correct.
            
            for page_idx in range(start_page - 1, end_page):
                writer.add_page(reader.pages[page_idx])

            with open(output_filename, "wb") as output_file:
                writer.write(output_file)
            
            print(f"  -> Created: {output_filename}")

        print("\nSplitting process completed.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Check for external configuration file
    config_path = "split_config.py"
    if os.path.exists(config_path):
        print(f"Loading configuration from {config_path}...")
        try:
             # Add current directory to sys.path to ensure import works
             sys.path.append(os.getcwd())
             import split_config
             INPUT_PDF = split_config.INPUT_PDF
             # Check if OUTPUT_DIR is defined in config
             if hasattr(split_config, 'OUTPUT_DIR'):
                 output_dir = split_config.OUTPUT_DIR
                 if not os.path.exists(output_dir):
                     os.makedirs(output_dir)
                 # We need to pass output_dir to split_pdf or handle it.
                 # Let's modify split_pdf to accept an output_dir or handle it in the loop.
                 # For now, let's just change the working directory or prefix filenames?
                 # Prefixing filenames is safer.
                 pass
             else:
                 output_dir = "."
                 
             SPLIT_RANGES = split_config.SPLIT_RANGES
             
             # Adjust split_pdf call to use output_dir
             # We need to refactor split_pdf slightly or just pass absolute paths for filenames? 
             # Let's pass output_dir to split_pdf.
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)
    else:
        # Default / Fallback
        INPUT_PDF = "large_document.pdf"
        output_dir = "."
        SPLIT_RANGES = []

    # Simple command line argument check for overrides
    if len(sys.argv) > 1:
        INPUT_PDF = sys.argv[1]
    
    if not os.path.exists(INPUT_PDF):
        if INPUT_PDF == "large_document.pdf":
             print("Please configure 'split_config.py' or provide a file path.")
        else:
             print(f"File not found: {INPUT_PDF}")
    elif not SPLIT_RANGES:
        print("No split ranges defined. Please check 'split_config.py'.")
    else:
        # We need to update split_pdf signature to support output_dir
        # But wait, I can't easily change the signature in this replace block without changing the definition too.
        # I'll just change the loop in split_pdf in a separate call or do a robust rewrite.
        # Actually, let's just change CWD to output_dir?
        # No, INPUT_PDF might be relative.
        
        # Better: pass output_dir to split_pdf as a new argument.
        split_pdf(INPUT_PDF, SPLIT_RANGES, output_dir=output_dir)

