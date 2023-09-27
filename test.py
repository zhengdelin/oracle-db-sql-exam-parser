import aspose.ocr as ocr

# Initialize an object of AsposeOcr class
api = ocr.AsposeOcr()

# Load the scanned PDF file
input = ocr.OcrInput(ocr.InputType.PDF)
input.add("outputs/parse-image-output.pdf")

# Recognize text with OCR
result = api.recognize(input)

# Print the output text to the console
print(result[0].recognition_text)
