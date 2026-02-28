======================================================
  Little Lemon Restaurant - Back-End Capstone Project
======================================================

SETUP INSTRUCTIONS
------------------
1. Clone the repository:
   git clone <your-repo-url>
   cd littlelemon

2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate       (Mac/Linux)
   venv\Scripts\activate          (Windows)

3. Install dependencies:
   pip install -r requirements.txt

4. Create MySQL database:
   mysql -u root -p
   CREATE DATABASE littlelemon;
   EXIT;

5. Update database credentials in littlelemon/settings.py:
   'USER': 'your_mysql_username',
   'PASSWORD': 'your_mysql_password',

6. Run migrations:
   python manage.py makemigrations
   python manage.py migrate

7. Create superuser:
   python manage.py createsuperuser

8. Run server:
   python manage.py runserver

9. Run tests:
   python manage.py test restaurant


======================================================
  API PATHS TO TEST WITH INSOMNIA
======================================================

BASE URL: http://127.0.0.1:8000

--- AUTHENTICATION ---

POST /api/registration/
  Register a new user
  Body (JSON): { "username": "testuser", "password": "pass123", "email": "test@email.com" }
  Returns: token

POST /api/login/
  Login and get token
  Body (JSON): { "username": "testuser", "password": "pass123" }
  Returns: token

POST /auth/token/login/
  Djoser login (alternative)
  Body (JSON): { "username": "testuser", "password": "pass123" }

POST /auth/token/logout/
  Logout (requires: Authorization: Token <your_token>)

GET /api/me/
  Get current user info
  Requires: Authorization: Token <your_token>

--- MENU API ---

GET /api/menu/
  List all menu items
  Requires: Authorization: Token <your_token>

POST /api/menu/
  Add a new menu item
  Requires: Authorization: Token <your_token>
  Body (JSON): { "title": "Greek Salad", "price": "12.99", "inventory": 100 }

GET /api/menu/1/
  Get a single menu item (replace 1 with actual ID)
  Requires: Authorization: Token <your_token>

PUT /api/menu/1/
  Update a menu item
  Requires: Authorization: Token <your_token>
  Body (JSON): { "title": "Updated Salad", "price": "14.99", "inventory": 80 }

DELETE /api/menu/1/
  Delete a menu item
  Requires: Authorization: Token <your_token>

--- BOOKING API ---

GET /api/bookings/
  List all bookings
  Requires: Authorization: Token <your_token>

POST /api/bookings/
  Create a new booking
  Requires: Authorization: Token <your_token>
  Body (JSON): { "name": "John Doe", "no_of_guests": 4, "booking_date": "2024-06-15T19:00:00Z" }

GET /api/bookings/1/
  Get a single booking
  Requires: Authorization: Token <your_token>

PUT /api/bookings/1/
  Update a booking
  Requires: Authorization: Token <your_token>
  Body (JSON): { "name": "Jane Doe", "no_of_guests": 2, "booking_date": "2024-06-15T20:00:00Z" }

DELETE /api/bookings/1/
  Delete a booking
  Requires: Authorization: Token <your_token>

--- WEB PAGES ---

GET /           → Home page
GET /about/     → About page
GET /menu/      → Menu page (HTML)
GET /book/      → Booking form page
GET /admin/     → Django admin panel

======================================================
  HOW TO USE INSOMNIA
======================================================

1. Register a user:
   POST http://127.0.0.1:8000/api/registration/
   Body → JSON → { "username": "myuser", "password": "mypassword123" }

2. Copy the token from the response.

3. For all protected endpoints, add header:
   Authorization: Token <paste_token_here>

4. Test menu and booking endpoints as listed above.
