FROM python:3.12-alpine

# Set the working directory
WORKDIR /build

# Install dependencies
COPY requirements.txt /build/
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /build/