FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN python -m spacy download ja_core_news_sm

COPY . .

CMD ["python3", "./main.py"]