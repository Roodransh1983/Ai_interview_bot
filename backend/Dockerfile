FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet'); nltk.download('omw-1.4'); nltk.download('maxent_ne_chunker'); nltk.download('words')"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
