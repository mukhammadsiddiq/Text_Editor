import re
from fpdf import FPDF
import os


# saved all my functions inside of class as method
class TextEditor:
    def __init__(self):
        self.content = ""
        self.original_file_path = ""

# method for reading file
    def open_file(self, file_path):
        try:
            with open(file_path, "rb") as file:
                # Read the file as bytes and decode using utf-8, ignoring errors
                self.content = file.read().decode("utf-8", errors="ignore")
                self.original_file_path = file_path
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error opening file: {e}")

    def save_file(self, file_type):
        if not self.original_file_path:
            print("No file is open. Please open a file first.")
            return

        directory = os.path.dirname(self.original_file_path)
        file_name, file_extension = os.path.splitext(os.path.basename(self.original_file_path))
        new_file_path = os.path.join(directory, f"{file_name}_modified.{file_type}")

        with open(new_file_path, "w") as file:
            file.write(self.content)
        print(f"Changes saved to new {file_type} file: {new_file_path}")

        if file_type == "pdf":
            self.pdf_generator(new_file_path)

    def find_text(self, pattern):
        matches = re.finditer(pattern, self.content)

        for match in matches:
            start_index, end_index = match.span()
            print(f"Match found: {self.content[start_index:end_index]}")

    def insert_text(self, position, text):
        self.content = self.content[:position] + text + self.content[position:]

    def delete_text(self, start, end):
        self.content = self.content[:start] + self.content[end:]

    def display_content(self):
        print(self.content)

# method for generating pdf from new edited file
    def pdf_generator(self, file_path):
        abs_file_path = os.path.abspath(file_path)
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=12)

        # Use utf-8 encoding when writing content to the PDF
        pdf.multi_cell(0, 10, txt=self.content.encode('latin-1', 'replace').decode('latin-1'))

        pdf.output(abs_file_path)

if __name__ == "__main__":
    editor = TextEditor()

    while True:
        print("\nOptions:")
        print("1. Open file")
        print("2. Save changes to new file")
        print("3. Find text")
        print("4. Insert text")
        print("5. Delete text")
        print("6. Display content")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            file_path = input("Enter the file path to open: ")
            editor.open_file(file_path)
        elif choice == "2":
            file_type = input("Enter 'txt' to save as a text file or 'pdf' to save as a PDF file: ").lower()
            if file_type not in ["txt", "pdf"]:
                print("Invalid file type. Please enter 'txt' or 'pdf'.")
                continue
            editor.save_file(file_type)

        elif choice == "3":
            pattern = input("Enter the regex pattern to find: ")
            editor.find_text(pattern)
        elif choice == "4":
            position = int(input("Enter the position to insert text: "))
            text_to_insert = input("Enter the text to insert: ")
            editor.insert_text(position, text_to_insert)
        elif choice == "5":
            start = int(input("Enter the start position to delete text: "))
            end = int(input("Enter the end position to delete text: "))
            editor.delete_text(start, end)
        elif choice == "6":
            editor.display_content()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")
