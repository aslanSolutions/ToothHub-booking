# Dockerfile for booking-service
FROM python:3.8

# Set the working directory
WORKDIR /Booking/booking-service

# Copy the requirements file and install dependencies
COPY requirements.txt /Booking/booking-service/requirements.txt


RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /Booking/booking-service

# Set the entry point for the container
ENTRYPOINT ["python"]

# Default command to be executed if no command is provided when running the container
CMD ["run.py"]