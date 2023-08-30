import os
import re
import pandas as pd
import requests
from tabulate import tabulate
from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader

def extract_potential_dois(text):
    doi_pattern = r"10\.\d{4,9}/\S+"
    matches = re.findall(doi_pattern, text)
    return matches

def clean_doi(doi):
    return doi.rstrip('.')

def extract_text_from_pdf_using_ocr(file_path):
    images = convert_from_path(file_path, dpi=300, first_page=1, last_page=1)
    if images:
        text = pytesseract.image_to_string(images[0])
        return text
    return ""

def extract_doi_from_pdf_using_ocr(file_path):
    text = extract_text_from_pdf_using_ocr(file_path)
    dois = extract_potential_dois(text)
    return clean_doi(dois[0]) if dois else "N/A"

def abstract_from_inverted_index(inverted_index):
    word_positions = [(word, pos) for word, positions in inverted_index.items() for pos in positions]
    word_positions.sort(key=lambda x: x[1])
    abstract = ' '.join(word for word, pos in word_positions)
    return abstract

openalex_cache = {}

def get_paper_info(doi):
    if doi == "N/A":
        return ["N/A"] * 7
    
    # Check cache first
    if doi in openalex_cache:
        return openalex_cache[doi]
    
    base_url = "https://api.openalex.org/works/"
    full_doi = "https://doi.org/" + doi
    response = requests.get(base_url + full_doi)

    if response.status_code != 200:
        return ["N/A"] * 7

    data = response.json()
    authors = ', '.join([authorship['author']['display_name'] for authorship in data['authorships']]) if 'authorships' in data else "N/A"
    publication_date = data.get('publication_date', "N/A")
    title = data.get('title', "N/A")
    concepts = ', '.join([concept['display_name'] for concept in data['concepts']]) if 'concepts' in data else "N/A"
    abstract = abstract_from_inverted_index(data['abstract_inverted_index']) if 'abstract_inverted_index' in data else "N/A"
    referenced_works = ', '.join(data['referenced_works']) if 'referenced_works' in data else "N/A"
    related_works = ', '.join(data['related_works']) if 'related_works' in data else "N/A"

    # Store in cache
    openalex_cache[doi] = authors, publication_date, title, concepts, abstract, referenced_works, related_works
    
    return authors, publication_date, title, concepts, abstract, referenced_works, related_works

def hybrid_doi_extraction(file_path):
    # Extract text once
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ''.join(page.extract_text() for page in pdf_reader.pages)
    
    # Step 1: Extract DOI using the original text-based method
    doi_pattern = r"\b(10[.][0-9]{4,}(?:[.][0-9]+)*\/(?:(?![\"&\'<>])\S)+)\b"
    matches = re.findall(doi_pattern, text)
    doi = matches[0] if matches else "N/A"
    
    # Step 2: Fetch details from OpenAlex
    paper_info = get_paper_info(doi)
    
    # Step 3: If OpenAlex returns N/A, use the OCR-based method
    if paper_info[0] == "N/A":
        doi = extract_doi_from_pdf_using_ocr(file_path)
        paper_info = get_paper_info(doi)
    
    return doi, paper_info

directory = '/Users/bohui/Projects/Paper_filter/Test_paper'
pdf_files = [filename for filename in os.listdir(directory) if filename.endswith('.pdf')]
total_files = len(pdf_files)


table_data = []

for index, filename in enumerate(pdf_files, start=1):
    file_path = os.path.join(directory, filename)
    doi, paper_info = hybrid_doi_extraction(file_path)
    table_data.append([filename, doi, *paper_info])

    # Calculate and print progress percentage
    progress_percentage = (index / total_files) * 100
    print(f"Progress: {progress_percentage:.2f}% done")

table_headers = ["File Name", "DOI", "Authors", "Publication Date", "Title", "Concepts", "Abstract", "Referenced Works", "Related Works"]
table = tabulate(table_data, headers=table_headers, tablefmt="pretty")
print(table)

df = pd.DataFrame(table_data, columns=table_headers)
try:
    df.to_excel("/Users/bohui/Projects/Paper_filter/Extracted_info.xlsx", index=False)
except Exception as e:
    print(f"Exception occurred: {e}")
