# set python as base image
FROM python:3.12-slim

# install dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy requirements, install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy whole app into the container
COPY . /app
WORKDIR /app

# dummy data
COPY seed.py .
RUN python seed.py

EXPOSE 8000

# run app (FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
