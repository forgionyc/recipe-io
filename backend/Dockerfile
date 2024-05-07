# Use the official Python image as a base
FROM python:3.10.12

# Install system dependencies
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /code
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code

# Upgrade pip and install project dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r reqs.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]