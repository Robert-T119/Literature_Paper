import os
import re
import requests
from pdf2image import convert_from_path
import pytesseract

def extract_potential_dois(text):
    doi_pattern = r"10\.\d{4,9}/\S+"
    matches = re.findall(doi_pattern, text)
    return matches

def clean_doi(doi):
    return doi.rstrip('.')

def extract_doi_from_pdf_text(file_path):
    # Define the DOI regex pattern
    doi_pattern = r"\b(10[.][0-9]{4,}(?:[.][0-9]+)*\/(?:(?![\"&\'<>])\S)+)\b"
    
    # Extract text from the PDF
    try:
        import PyPDF2
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            pdf_text = ''
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                pdf_text += page.extractText()
                
            # Search for DOIs in the extracted text
            matches = re.findall(doi_pattern, pdf_text)
            return matches[0] if matches else None
    except Exception as e:
        # In case of any errors (e.g., the PDF is encrypted or PyPDF2 is not installed), return None
        return None

def extract_text_from_pdf_using_ocr(file_object):
    # Convert PDF pages to images
    images = convert_from_path(file_object)

    # Extract text from each image
    extracted_texts = [pytesseract.image_to_string(img) for img in images]

    # Combine all extracted texts
    combined_text = "\n".join(extracted_texts)
    
    return combined_text

def extract_doi_from_pdf_using_ocr(file_object):
    text = extract_text_from_pdf_using_ocr(file_object)
    potential_dois = extract_potential_dois(text)
    cleaned_dois = [clean_doi(doi) for doi in potential_dois]
    
    return cleaned_dois

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

def process_uploaded_pdf(file_object):
    text = file_object.read().decode()

    # Step 1: Extract DOI using the original text-based method
    doi_pattern = r"\b(10[.][0-9]{4,}(?:[.][0-9]+)*\/(?:(?![\"&\'<>])\S)+)\b"
    matches = re.findall(doi_pattern, text)
    doi = matches[0] if matches else "N/A"
    
    # Step 2: Fetch details from OpenAlex
    paper_info = get_paper_info(doi)
    
    # Step 3: If OpenAlex returns N/A, use the OCR-based method
    if paper_info[0] == "N/A":
        doi = extract_doi_from_pdf_using_ocr(file_object)
        paper_info = get_paper_info(doi)

    return [doi, *paper_info]
