
import os
import sys
from pypdf import PdfReader

# Increase recursion depth for deep PDF structures
sys.setrecursionlimit(20000)

def get_input_file(folder="Full_doc"):
    """Finds the first PDF in the given folder."""
    if not os.path.exists(folder):
        return None
    for f in os.listdir(folder):
        if f.lower().endswith(".pdf"):
            return os.path.join(folder, f)
    return None

def generate_config():
    input_path = get_input_file()
    if not input_path:
        print("No PDF found in 'Full_doc' folder.")
        return

    print(f"Reading {input_path}...")
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    # Extract linear list of bookmarks
    bookmarks = []
    
    def process_outline(outline):
        for item in outline:
            if isinstance(item, list):
                process_outline(item)
            else:
                try:
                    title = item.title
                    # get_destination_page_number can raise an error if destination is invalid
                    try:
                        page = reader.get_destination_page_number(item) + 1
                        bookmarks.append((page, title))
                    except:
                        # Skip invalid destinations
                        pass
                except:
                    pass

    if reader.outline:
        process_outline(reader.outline)
    
    # Sort by page number
    bookmarks.sort(key=lambda x: x[0])
    
    # Filter out duplicates or "Page 1" if it seems like a placeholder? 
    # For now, keep everything but warn in comments if multiple items start at same page.
    
    filename = os.path.basename(input_path)
    filename_no_ext = os.path.splitext(filename)[0]
    
    config_content = [
        "import os",
        "",
        "# Input file path (Auto-detected)",
        f'INPUT_PDF = r"{input_path}"',
        "",
        "# Output directory (Subfolder within Splitted_docs)",
        f'OUTPUT_DIR = os.path.join("Splitted_docs", "{filename_no_ext}")',
        "",
        "# Split Ranges: (Start Page, End Page, Section Name)",
        "# Review and edit these ranges. Ensure they don't overlap in unwanted ways.",
        "SPLIT_RANGES = ["
    ]

    # Smart range calculation
    # If we have bookmarks at p1, p50, p100...
    # Range 1: 1 to 49
    # Range 2: 50 to 99
    # Last one: 100 to total_pages
    
    # However, because of the "Page 1" issue (Titles pointing to p1, contents at p9000), 
    # specific logic is needed:
    # If multiple bookmarks are on the same page, we might just list them.
    # The user needs to choose.
    
    # We will generate a list based on strict start-next logic, but comment out suspicious small ranges.
    
    unique_starts = []
    seen_pages = set()
    for p, t in bookmarks:
        if p not in seen_pages:
            unique_starts.append((p, t))
            seen_pages.add(p)
        else:
            # Append title to existing?
            pass

    
    output_msg = ""
    # If no bookmarks found, fall back to simple page-based splitting
    if not unique_starts:
        print(f"No bookmarks found in {filename}. Generating split based on page count (Max 800 pages/file).")
        target_pages = 800
        
        start = 1
        part_num = 1
        while start <= total_pages:
            end = min(start + target_pages - 1, total_pages)
            config_content.append(f"    ({start}, {end}, \"Part {part_num} (Pages {start}-{end})\"),")
            start = end + 1
            part_num += 1
            
    else:
        # Grouping Logic for NotebookLM (Max 50 files, Max 500k words)
        # Strategy: Group small sections until we reach ~800 pages per file.
        # This should yield ~10-15 files for a 10k page document, safe for limits.
        target_pages_per_file = 800
        
        current_group_start = -1
        current_group_end = -1
        current_group_name = ""
        current_page_count = 0
        
        first_section = True
        output_msg = ""
        
        for i in range(len(unique_starts)):
            start_page, title = unique_starts[i]
            
            if i < len(unique_starts) - 1:
                end_page = unique_starts[i+1][0] - 1
            else:
                end_page = total_pages
                
            # Basic validation
            if start_page > end_page:
                continue
                
            section_pages = end_page - start_page + 1
            
            if first_section:
                current_group_start = start_page
                current_group_end = end_page
                current_group_name = title
                current_page_count = section_pages
                first_section = False
            else:
                # Check if adding this section exceeds target
                if current_page_count + section_pages > target_pages_per_file:
                    # Close current group
                    config_content.append(f"    ({current_group_start}, {current_group_end}, \"{current_group_name} - {title.split(' ')[0]} (Part)\"),")
                    
                    # Start new group
                    current_group_start = start_page
                    current_group_end = end_page
                    current_group_name = title
                    current_page_count = section_pages
                else:
                    # Extend current group
                    current_group_end = end_page
                    current_page_count += section_pages
                    # Update name? Maybe just keep first section name or append "..."
                    # Let's keep the first section name as the main identifier, user can rename.
                    pass
                    
        # Close final group
        if current_group_start != -1:
            config_content.append(f"    ({current_group_start}, {current_group_end}, \"{current_group_name} (End)\"),")

    config_content.append("]")
    
    with open("split_config.py", "w", encoding="utf-8") as f:
        f.write("\n".join(config_content))
    
    print(output_msg)

if __name__ == "__main__":
    generate_config()
