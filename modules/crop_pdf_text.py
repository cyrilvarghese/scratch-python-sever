import os
import PyPDF2
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
print(parent_dir)

def crop_pages_in_range(pdf_file, from_page, to_page):
    cropped_pages = []
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(from_page - 1, to_page):
            page = pdf_reader.getPage(page_num)
            cropped_pages.append(page.extractText())

    return cropped_pages

def save_cropped_text(pdf_file, from_page, to_page, save_path=parent_dir,delete_original=True):
    # Get the base name of the PDF file
    file_name, file_ext = os.path.splitext(pdf_file)
    # Generate the name for the cropped text file
    cropped_file_name = f"{file_name}_cropped({from_page}_{to_page}).txt"

    cropped_pages = crop_pages_in_range(pdf_file, from_page, to_page)

    # Convert cropped pages to plain text
    text_content = ''
    for index, page_content in enumerate(cropped_pages, start=from_page):
        text_content += f'---Page {index}:\n\n{page_content}\n\n'

    # Determine the save path
    if save_path:
        cropped_file_path = os.path.join(save_path, cropped_file_name)
    else:
        cropped_file_path = cropped_file_name

    # Write text content to a file
    with open(cropped_file_path, 'w') as file:
        file.write(text_content)
    
    # Delete the original file if specified
    if delete_original:
        os.remove(pdf_file)
    
    print("------saved cropped File : ",cropped_file_name)
    return cropped_file_path

def main():
    pdf_file = input("Enter the path to the PDF file: ")
    from_page = int(input("Enter the starting page number: "))
    to_page = int(input("Enter the ending page number: "))

    cropped_file_name = save_cropped_text(pdf_file, from_page, to_page)

    print(f"Cropped pages saved to '{cropped_file_name}'.")

if __name__ == "__main__":
    main()
