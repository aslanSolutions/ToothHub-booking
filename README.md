# Project Name

    1. Appointment Service
    The Appointment Service is a Python-based service designed to manage appointments for healthcare professionals, dentists, or any service providers that require scheduling. This service provides functionality to create, retrieve, update, and delete appointments. It includes features to check for appointment availability, get details of a specific appointment, and retrieve a list of appointments based on various criteria such as date or healthcare professional.

    2. Wishlist Service
    The Wishlist Service is a Python service that enables users to create and manage wishlists. Users can add items they wish to acquire, mark items as purchased, and remove them from the wishlist. The service allows users to share their wishlists with others, making it a versatile tool for tracking desired items and facilitating gift-giving. Python is used to implement the wishlist service, offering a user-friendly and efficient experience for wishlist management.

    3. Booking Service
    The Booking Service is a Python-based service tailored for managing bookings and reservations. Whether it's for hotel rooms, event spaces, or other resources, this service facilitates the booking process. Users can create new bookings, update existing ones, and cancel reservations. The service employs Python to provide a robust and scalable solution for handling booking-related operations. It includes features like checking availability, getting booking details, and listing all bookings.

These services are designed to be modular, scalable, and easily integrable into a broader system. Python's versatility and readability make it an excellent choice for developing such services, providing a balance between simplicity and functionality. Each service is implemented as a microservice, allowing for independent deployment, scaling, and maintenance. The services communicate through APIs, ensuring seamless integration into diverse applications and systems.

## Prerequisites

- [Python](https://www.python.org/) (version 3.7 < ..)
- [Virtualenv](https://pypi.org/project/virtualenv/) (optional but recommended)

## Setup

1. Clone the repository:

    ```bash
    git clone https://git.chalmers.se/courses/dit355/2023/student-teams/dit356-2023-07/Booking.git
    ```

2. Navigate to the project directory:

    ```bash
    cd / "Each of the services"
    ```

3. Copy .env.example & paste in new file as .env

    ```bash
    cp .env.example .env
    ```

4. (Optional) Create and activate a virtual environment:

    ```bash
    virtualenv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

    This step is recommended to isolate your project dependencies.

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```


## Usage

Run Project


```bash
    python3/python run.py
```