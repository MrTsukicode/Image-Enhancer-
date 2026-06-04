import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

# Define folders
image_folder = "images"
output_file = "extracted_text.txt"

print("Looking for files inside the images folder...")

# Make sure the file always gets created so Git never crashes
with open(output_file, "w", encoding="utf-8") as f:
    f.write("=== OCR Processing Log ===\n")

if not os.path.exists(image_folder) or not os.listdir(image_folder):
    print(f"Error: The '{image_folder}' folder is empty!")
    with open(output_file, "a", encoding="utf-8") as f:
        f.write("Error: No files found to process inside the images folder.\n")
else:
    for file_name in os.listdir(image_folder):
        file_path = os.path.join(image_folder, file_name)
        
        # Lowercase check to bypass Windows vs Linux naming quirks
        if file_name.lower().endswith('.pdf'):
            print(f"Found PDF: {file_name}. Converting to images...")
            try:
                # convert_from_path with explicit fallback configurations
                pages = convert_from_path(file_path)
                
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"\n=== Text from PDF: {file_name} ===\n")
                    
                    for i, page in enumerate(pages):
                        print(f"Processing Page {i+1}...")
                        text = pytesseract.image_to_string(page)
                        f.write(f"--- Page {i+1} ---\n")
                        f.write(text)
                        f.write("\n")
                print(f"Successfully processed PDF: {file_name}")
            except Exception as e:
                print(f"Error processing PDF {file_name}: {e}")
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"Error processing {file_name}: {str(e)}\n")

        elif file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Found Image: {file_name}. Processing...")
            try:
                text = pytesseract.image_to_string(Image.open(file_path))
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"\n=== Text from Image: {file_name} ===\n")
                    f.write(text)
                    f.write("\n")
                print(f"Successfully processed image: {file_name}")
            except Exception as e:
                print(f"Error processing image {file_name}: {e}")

print("All processing done!")
