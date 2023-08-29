import requests
from datetime import datetime, timedelta
import string
import time

def generate_date_ranges(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    while start_date <= end_date:
        yield start_date.strftime("%Y-%m-%d")
        start_date += timedelta(days=1)

def abstract_from_inverted_index(inverted_index):
    if inverted_index is None:
        return "N/A"
    word_positions = [(word, pos) for word, positions in inverted_index.items() for pos in positions]
    word_positions.sort(key=lambda x: x[1])
    abstract = ' '.join(word for word, pos in word_positions)
    return abstract

def remove_non_printable_chars(s):
    if s is None:
        return ""
    return ''.join(filter(lambda x: x in string.printable, s))

def get_total_papers_for_period(from_date, to_date, concept_id):
    search_url = f'https://api.openalex.org/works?filter=concept.id:{concept_id},from_publication_date:{from_date},to_publication_date:{to_date}'
    response = requests.get(search_url)
    response.raise_for_status()
    total_papers = response.json()["meta"]["count"]
    return total_papers

def extract_papers_from_openalex_search(search_url, limit, current_date):
    cursor = "*"
    papers = []
    papers_fetched = 0  # Initialize counter_

    while len(papers) < limit:
        url = f"{search_url}&per_page=200&cursor={cursor}"
        response = requests.get(url)
        
        # Handle rate limiting - sleep if needed
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))  # Default to 60 seconds if header is missing
            print(f"Rate limit exceeded. Sleeping for {retry_after} seconds.")
            time.sleep(retry_after)
            continue  # Re-try the request after sleeping
        
        response.raise_for_status()

        works = response.json()["results"]
        papers_fetched += len(works)
        
        for work in works:
            abstract = abstract_from_inverted_index(work['abstract_inverted_index']) if 'abstract_inverted_index' in work else "N/A"
            if abstract == "N/A":
                continue

            doi = work['doi']
            title = work['title']
            authors = ', '.join([str(authorship['author'].get('display_name', 'Unknown Author')) for authorship in work['authorships']])
            publication_date = work['publication_date']
            concepts = ', '.join([concept['display_name'] for concept in work['concepts']])
            title = remove_non_printable_chars(title)
            authors = remove_non_printable_chars(authors)
            abstract = remove_non_printable_chars(abstract)
            concepts = remove_non_printable_chars(concepts)
            papers.append([doi, title, authors, publication_date, abstract, concepts])
        
        print(f"Fetched {papers_fetched} papers for {current_date}")

        cursor = response.json()["meta"]["next_cursor"]
        if cursor is None:
            break

    return papers