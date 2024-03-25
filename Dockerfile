# Use the official Python image as the base image
FROM python:3.9-slim AS backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY ./requirements/dev.txt .
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r dev.txt

# Copy the backend code into the container
COPY . .

# Expose port 80 for the FastAPI server
EXPOSE 8000

# Command to start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
