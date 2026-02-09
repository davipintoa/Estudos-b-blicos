# PDF Splitter for NotebookLM

A local Python tool designed to split large PDF documents (10,000+ pages) into smaller chunks that fit within Google NotebookLM's source limits (500,000 words per source, 50 sources).

## Features
- **Smart Grouping**: Automatically groups bookmarked sections to maximize size while staying under limits.
- **Fallback Mode**: Splits by page count (e.g., 800 pages/file) if no Table of Contents is found.
- **Ordered Output**: Generates numbered files (e.g., `01. Part 1.pdf`) to maintain reading order.
- **Recursion Handling**: Capable of processing PDFs with extremely deep bookmark structures.

## Installation

1. Install [Python](https://www.python.org/downloads/).
2. Install the required library:
   ```bash
   pip install pypdf
   ```

## Usage

1. **Place your PDF** in the `Full_doc/` folder.
2. **Run the tool**:
   ```bash
   python main.py
   ```
3. **Follow the menu**:
   - **Option 1**: Generate the split configuration.
   - **Option 2**: Execute the split.
   - **Option 3**: Check word count estimates.

Output files are saved in `Splitted_docs/<Your_Filename>/`.

## Project Structure
- `main.py`: Entry point.
- `src/`: contains `pdf_splitter.py`, `generate_split_config.py`, and `check_limits.py`.
- `Full_doc/`: Input folder (ignored by git).
- `Splitted_docs/`: Output folder (ignored by git).
