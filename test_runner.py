
from pdf_splitter import split_pdf
import os

def run_test():
    input_pdf = "test_document.pdf"
    if not os.path.exists(input_pdf):
        print(f"Error: {input_pdf} not found. Run create_test_pdf.py first.")
        return

    # Define test ranges (1-based)
    ranges = [
        (1, 5, "Test Section 1"),
        (6, 10, "Test Section 2"),
        (11, 20, "Test Section 3 - Large Chunk")
    ]

    print("Running split_pdf validation...")
    split_pdf(input_pdf, ranges)
    
    # Verification
    expected_files = ["TestSection1.pdf", "TestSection2.pdf", "TestSection3-LargeChunk.pdf"]
    for f in expected_files:
        if os.path.exists(f):
            print(f"SUCCESS: {f} created.")
        else:
             print(f"FAILURE: {f} NOT created.")

if __name__ == "__main__":
    run_test()
