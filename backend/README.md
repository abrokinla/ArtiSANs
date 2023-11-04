# ArtiSans Backend

ArtiSANs of a comprehensive platform designed to connect clients with skilled artisans in various fields. The backend is responsible for managing data, user authentication, and API endpoints for creating, listing, and assigning job requests to artisans. It is built using Django and the Django REST framework, providing a robust and secure foundation for the ArtiSans platform.

## Key Features:

- User management for both clients and artisans.
- Creation and management of job requests by clients.
- Assignment of job requests to artisans.
- Artisan profile management.
- API endpoints for seamless interaction with the frontend.

## Getting Started

To run the ArtiSans Django project locally, follow these steps:

1. Clone the repository: `$ git clone https://github.com/abrokinla/artisans.git`
2. Navigate to the backend directory: `$ cd /backend`
3. Create a virtual environment: `$ python3 -m venv env`
4. Activate the virtual environment:
   - On macOS and Linux: `$ source env/bin/activate`
   - On Windows: `$ .\env\Scripts\activate`
5. Install the project dependencies: `$ pip install -r requirements.txt`
6. Run database migrations: `$ python manage.py migrate`
7. Start the development server: `$ python manage.py runserver`
8. Access the API at `http://localhost:8000/`

## Endpoints

Below are the available API endpoints for the EduSchola Django project:

### POST /artisans/create/

- **General*:
  - Creates a new artisan object.
  - Requires a JSON object in the request body with the artisan user details.
  - Returns details of artisan.

- **Sample Request:*
```shell
 $ curl http://127.0.0.1:8000/api/artisans/create -X POST -H "Content-Type:application/json" -d "{
    "user": {
        "username": "artisan1",
        "email": "artisan@example.com",
        "password": "password123"
    },
    "categories": [1],
    "bio": "This is a test artisan bio.",
    "experience": "This is a test artisan experience.",
    "location": "This is a test artisan location.",
    "whatsapp": "+15555555555",
    "tel": "+15555555555"
}
"
```
- **Sample Response:*
```json
{
    "success": true,
    "data": {
        "user": {
            "username": "artisan1",
            "role": "client",
            "first_name": "",
            "last_name": ""
        },
        "categories": [
            1
        ],
        "bio": "This is a test artisan bio.",
        "experience": "This is a test artisan experience.",
        "location": "This is a test artisan location.",
        "whatsapp": "+15555555555",
        "tel": "+15555555555"
    }
}
```
