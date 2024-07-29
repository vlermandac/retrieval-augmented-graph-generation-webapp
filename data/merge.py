import fitz  # PyMuPDF
import os


def create_notice_page(doc_name):
    """
    Create a new PDF page with the text '### DOC doc_name ###' centered on the page.
    """
    # Create a new document
    notice_doc = fitz.open()
    # Add a blank page
    page = notice_doc.new_page()
    # Define the text to be added
    text = f"### DOC {doc_name} ###"
    # Define the position and font size
    position = (22, 22)  # Top-left corner (1 inch margin)
    font_size = 4
    # Add the text to the page
    page.insert_text(position, text, fontsize=font_size)
    return notice_doc


def merge_pdfs_with_notices(pdf_files, output_file):
    """
    Merge multiple PDF files into one, inserting a notice page between each document.
    """
    # Create a new PDF document
    merged_pdf = fitz.open()

    for pdf_file in pdf_files:
        # Open the current PDF file
        current_pdf = fitz.open(pdf_file)
        # Create a notice page for the current document
        notice_page = create_notice_page(os.path.basename(pdf_file))
        # Insert the notice page
        merged_pdf.insert_pdf(notice_page)
        # Insert the current PDF file
        merged_pdf.insert_pdf(current_pdf)

    # Save the merged PDF to the output file
    merged_pdf.save(output_file)


if __name__ == "__main__":
    # List of PDF files to be merged, all the pdf files in the current directory
    pdf_files = [file for file in os.listdir() if file.endswith(".pdf")]

    # Output file name
    output_file = "documentos-varios.pdf"

    # Merge the PDFs with notices
    merge_pdfs_with_notices(pdf_files, output_file)

    # Move the output file to an output directory. If the directory does not exist, create it
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    os.replace(output_file, os.path.join(output_dir, output_file))

    print(f"Merged PDF saved to: {os.path.join(output_dir, output_file)}")
