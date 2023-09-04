import os
import re
import requests
import fitz  # PyMuPDF

def extract_potential_dois(text):
    doi_pattern = r"10\.\d{4,9}/\S+"
    matches = re.findall(doi_pattern, text)
    return matches

def clean_doi(doi):
    return doi.rstrip('.')

def extract_doi_from_pdf_text(file_path):
    doi_pattern = r"\b(10[.][0-9]{4,}(?:[.][0-9]+)*\/(?:(?![\"&\'<>])\S)+)\b"
    doc = fitz.open(file_path)
    pdf_text = ''
    for page in doc:
        pdf_text += page.get_text("text")
        
    # Search for DOIs in the extracted text
    matches = re.findall(doi_pattern, pdf_text)
    return matches[0] if matches else None

def extract_text_from_pdf(file_object):
    doc = fitz.open(file_object)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

def extract_doi_from_pdf_using_ocr(file_object):
    # Using the same name for clarity, but we're not using OCR anymore.
    text = extract_text_from_pdf(file_object)
    potential_dois = extract_potential_dois(text)
    cleaned_dois = [clean_doi(doi) for doi in potential_dois]
    return cleaned_dois

def abstract_from_inverted_index(inverted_index):
    if not inverted_index:
        return "N/A"
    
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
    
    # Step 3: If OpenAlex returns N/A, use the OCR-based method (which is now direct text extraction)
    if paper_info[0] == "N/A":
        doi = extract_doi_from_pdf_using_ocr(file_object)
        paper_info = get_paper_info(doi)

    return [doi, *paper_info]
