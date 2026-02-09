
import os
import sys
from pypdf import PdfReader

# Increase recursion depth for deep PDF structures
sys.setrecursionlimit(20000)

def estimate_word_counts(directory):
    if not os.path.exists(directory):
         print(f"Directory not found: {directory}")
         return

    print(f"Analyzing PDF files in {directory} (and subfolders)...")
    
    pdf_files = []
    # Walk to find all PDFs
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, f))
    
    if not pdf_files:
        print(f"No PDF files found in {directory} (or subfolders).")
        return

    total_words = 0
    file_stats = []

    for path in pdf_files:
        try:
            reader = PdfReader(path)
            words = 0
            # Simple heuristic: extract text
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    words += len(text.split())
            
            # storing name relative to input directory for readability
            rel_name = os.path.relpath(path, directory)
            file_stats.append((rel_name, words))
            total_words += words
        except Exception as e:
            print(f"Error reading {path}: {e}")

    # Sort by word count descending
    file_stats.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nTotal Files: {len(pdf_files)}")
    print(f"Total Words (Estimated): {total_words}")
    print(f"Average Words per File: {total_words / len(pdf_files) if pdf_files else 0:.0f}")
    
    print("\nTop 10 Largest Files:")
    for f, w in file_stats[:10]:
        print(f"{f}: {w} words")

    print("\nTop 10 Smallest Files:")
    for f, w in file_stats[-10:]:
        print(f"{f}: {w} words")
        
    return file_stats


def get_latest_subfolder(parent_dir):
    """Returns the path to the most recently created subdirectory."""
    if not os.path.exists(parent_dir):
        return None
        
    subdirs = [os.path.join(parent_dir, d) for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]
    
    if not subdirs:
        return None
        
    # Sort by modification time (most recent first)
    latest_subdir = max(subdirs, key=os.path.getmtime)
    return latest_subdir

if __name__ == "__main__":
    # Default locations to check for Splitted_docs
    possible_roots = [
        "Splitted_docs",
        os.path.join("..", "Splitted_docs"),
        os.path.join(os.path.dirname(__file__), "..", "Splitted_docs")
    ]
    
    target_root = None
    for root in possible_roots:
        if os.path.exists(root):
            target_root = root
            break
            
    if not target_root:
        print("Error: Could not find 'Splitted_docs' folder.")
        sys.exit(1)

    # Check if we should find the latest subfolder
    latest_folder = get_latest_subfolder(target_root)
    
    if latest_folder:
        print(f"Latest split output found: {latest_folder}")
        estimate_word_counts(latest_folder)
    else:
        print(f"No subfolders found in {target_root}. Checking root...")
        estimate_word_counts(target_root)
