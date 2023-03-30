# Base image
FROM python:3

# Set working directory
WORKDIR /app

# Copy script to container
COPY src/crawl.py .

# Install psycopg2 and lxml
RUN pip install psycopg2 lxml scrapy

# Run script
CMD ["python", "crawl.py"]
