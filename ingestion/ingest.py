import pdfplumber
import re

def extraction():
    with pdfplumber.open(r"C:\Users\shett\Downloads\resume.pdf") as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text(x_tolerance = 1.5)
        text = text.replace("(cid:136)","-")
        text = re.sub(r"(\w)-\n(\w)", r"\1\2",text)
        print(text)
        return text