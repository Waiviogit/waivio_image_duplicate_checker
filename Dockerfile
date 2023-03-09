# Base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY app.py .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE ${PORT}


CMD ["python", "app.py"]