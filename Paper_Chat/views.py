from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
import openai
import os
from PyPDF2 import PdfReader
import json
import shutil

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MAX_TOKENS = 4000  # Max token count for a single API call_

def homepage(request):
    return render(request, 'dashboard.html')

def index(request):
    context = {}
    if 'pdf_url' in request.session:
        context['file_url'] = request.session['pdf_url']
        del request.session['pdf_url']
    return render(request, 'Paper_Chat/index.html', context)

def clean_temp_directory():
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def upload_pdf(request):
    if request.method == "POST":
        clean_temp_directory()
        pdf_file = request.FILES['pdf_file']
        temp_directory = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_directory, exist_ok=True)
        file_path = os.path.join(temp_directory, pdf_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)
        pdf_content = extract_text_from_pdf(file_path)
        request.session['pdf_content'] = pdf_content
        relative_url = os.path.join('media', 'temp', pdf_file.name)
        request.session['pdf_url'] = relative_url
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'upload_pdf.html')

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def process_text_chunkwise(text, query):
    chunk_size = MAX_TOKENS - 50  # Reserve some tokens for the query and other text
    start = 0
    end = chunk_size
    while start < len(text):
        chunk = text[start:end]
        prompt = f"Document says: {chunk}. User asks: {query}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        answer = response.choices[0].text.strip()
        if len(answer) > 10:
            return answer
        start += chunk_size // 2
        end = start + chunk_size
    return "I couldn't find a detailed answer based on the provided document."

@csrf_exempt
def process_text(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST method is allowed.")
    
    try:
        data = json.loads(request.body)
        text = data.get('text')
        action = data.get('action')
        pdf_content = data.get('pdf_content', "")

        if not text or not action:
            return HttpResponseBadRequest("Invalid data format.")

        # When the question comes from the chatbox
        if pdf_content:
            result = process_text_chunkwise(pdf_content, text)
        # When using summarize/explain buttons
        else:
            if action == 'summarize':
                result = your_summarize_function(text)
            elif action == 'explain':
                result = your_explain_function(text)
            else:
                return HttpResponseBadRequest("Invalid action.")

        return JsonResponse({'result': result})

    except ValidationError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def your_summarize_function(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following text: {text}",
            max_tokens=4000
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

def your_explain_function(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Explain the following text in a systematic way: {text}",
            max_tokens=4000
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)
