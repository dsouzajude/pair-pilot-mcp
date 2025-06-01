# Use an official Python runtime as a parent image
FROM python:3.13.3-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /server

# Copy the requirements file into the container at /server
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (the 'src' directory) into the container at /server/src
COPY ./src /server/src

# Make port 8100 available to the world outside this container
EXPOSE 8100

# Define the command to run your application
CMD ["python", "src/main.py"]
