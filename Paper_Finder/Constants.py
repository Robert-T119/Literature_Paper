stop_words = set([
    'ourselves', 'hers', 'between', 'yourself', 'but', 
    'again', 'there', 'about', 'once', 'during', 'out', 
    'very', 'having', 'with', 'they', 'own', 'an', 'be', 
    'some', 'for', 'do', 'its', 'yours', 'such', 'into', 
    'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 
    'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 
    'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 
    'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 
    'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 
    'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 
    'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 
    'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 
    'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 
    'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 
    'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 
    'against', 'a', 'by', 'doing', 'it', 'how', 'further', 
    'was', 'here', 'than'
      ])

concept_list = [
    ('Materials Science', 'https://openalex.org/c192562407'),
    ('Engineering', 'https://openalex.org/c127413603'),
    ('Chemistry', 'https://openalex.org/c185592680'),
    ('Physics', 'https://openalex.org/c121332964'),
    ('Environmental Science', 'https://openalex.org/c39432304'),
    ('Geology', 'https://openalex.org/c127313418'),
    ('Mathematics', 'https://openalex.org/c33923547'),
    ('Medicine', 'https://openalex.org/c71924100'),
]

must_satisfy_keywords = ['solid oxide fuel cells', 'sofc', 'sofcs', 'solid-oxide fuel cells', 'solid oxide fuel cell', 'solid-oxide fuel cell', 'soec', 'soecs', 'solid oxide electrolyzer']
stop_sequence = "\n"