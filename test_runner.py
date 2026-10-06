
import os
from src.pdf_splitter import split_pdf
from create_test_pdf import create_dummy_pdf

def run_test():
    input_pdf = "test_document.pdf"
    if not os.path.exists(input_pdf):
        print(f"{input_pdf} not found. Creating dummy test PDF...")
        create_dummy_pdf(input_pdf, 20)

    # Define test ranges (1-based)
    ranges = [
        (1, 5, "Test Section 1"),
        (6, 10, "Test Section 2"),
        (11, 20, "Test Section 3 - Large Chunk")
    ]

    print("Running split_pdf validation...")
    split_pdf(input_pdf, ranges)
    
    # Verification
    expected_files = [
        "01. Test Section 1.pdf",
        "02. Test Section 2.pdf",
        "03. Test Section 3 - Large Chunk.pdf"
    ]
    all_success = True
    for f in expected_files:
        if os.path.exists(f):
            print(f"SUCCESS: {f} created.")
        else:
            print(f"FAILURE: {f} NOT created.")
            all_success = False

    if all_success:
        print("\nAll tests passed successfully!")

if __name__ == "__main__":
    run_test()
