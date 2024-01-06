# Dockerfile for wishList-service
FROM python:3.8

# Set the working directory
WORKDIR /booking-service/wishlist-service

# Copy the requirements file and install dependencies
COPY requirements.txt /booking-service/wishlist-service/requirements.txt

RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /booking-service/wishlist-service

# Set the entry point for the container
ENTRYPOINT ["python"]

# Default command to be executed if no command is provided when running the container
CMD ["run.py"]
