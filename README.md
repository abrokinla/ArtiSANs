# ArtiSANs

ArtiSANs is a website that connects clients with local artisans such as carpenters, electricians, plumbers, and more. It serves as a platform for clients to find skilled artisans in their locality and request their services. The project is built with Django on the backend and Next.js on the frontend.

## Features

- User registration and authentication: Clients and artisans can create accounts and log in to the platform.
- User profiles: Users can create and manage their profiles, including adding profile pictures, contact information, and a brief bio.
- Artisan categorization: Artisans can be categorized into different skill categories, making it easier for clients to find the right professional.
- Job requests: Clients can create job requests, providing details such as title, description, and preferred artisan category.
- Artisan selection and job status: Artisans can view and accept job requests, and both clients and artisans can track the status of each job request.
- Reviews and ratings: Clients can provide reviews and ratings for artisans based on their job performance.
- Admin interface: An admin interface is available for managing user accounts, categories, job requests, and other aspects of the platform.

## Installation

To run the ArtiSANs project locally, follow these steps:

1. Clone the repository:
   
   git clone https://github.com/your-username/artisans.git

2. Set up the backend:

- Navigate to the backend directory:

    cd artisans/backend

- Create a virtual environment: 

    python -m venv venv

- Activate the virtual environment:

    source venv/bin/activate

- Install the required dependencies:

    pip install -r requirements.txt

- Apply migrations:

    python manage.py migrate

- Start the Django development server:

    python manage.py runserver

The backend server should now be running at http://localhost:8000.

# Contributing

Contributions are welcome! If you'd like to contribute to the ArtiSANs project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Submit a pull request explaining your changes.

Please ensure that your contributions adhere to the project's coding style and guidelines.

# License
The ArtiSANs project is licensed under the MIT License.

# Contact
For any inquiries or questions, feel free to reach out to the project maintainers:

Araoye Abraham - abrokinla@gmail.com

We appreciate your interest and hope you find ArtiSANs useful for connecting clients and artisans in your locality!
