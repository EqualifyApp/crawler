# Use an official Python runtime as a parent image
FROM python:3.9.10

# Set the working directory to /app/src
WORKDIR /app/src

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8084 available to the world outside this container
EXPOSE 8084

# Run main.py when the container launches
CMD ["python", "main.py"]
