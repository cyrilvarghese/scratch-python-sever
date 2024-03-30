import os
import PyPDF2
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)


def crop_pages_in_range(pdf_file, from_page, to_page):
    cropped_pages = []
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(from_page - 1, to_page):
            page = pdf_reader.getPage(page_num)
            cropped_pages.append(page)

    return cropped_pages

def save_cropped_pdf(pdf_file, from_page, to_page, save_path=parent_dir,delete_original=True):
    # Get the base name of the PDF file
    file_name, file_ext = os.path.splitext(pdf_file)
    # Generate the name for the cropped PDF file
    cropped_file_name = f"{file_name}_cropped.pdf"

    # Create a new PDF file writer
    pdf_writer = PyPDF2.PdfWriter()

    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        
        # Add cropped pages to the PDF writer
        for page_num in range(from_page - 1, min(to_page, pdf_reader.numPages)):
            page = pdf_reader.getPage(page_num)
            pdf_writer.addPage(page)

        # Determine the save path
        if save_path:
            cropped_file_path = os.path.join(save_path, cropped_file_name)
        else:
            cropped_file_path = cropped_file_name

        # Write the cropped pages to a new PDF file
        with open(cropped_file_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

         # Delete the original file if specified
        if delete_original:
            os.remove(pdf_file)
    
    print("------saved cropped File : ",cropped_file_name)
    return cropped_file_path

def main():
    pdf_file = input("Enter the path to the PDF file: ")
    from_page = int(input("Enter the starting page number: "))
    to_page = int(input("Enter the ending page number: "))
    
    cropped_file_name = save_cropped_pdf(pdf_file, from_page, to_page)

    print(f"Cropped pages saved to '{cropped_file_name}'.")

if __name__ == "__main__":
    main()
