# Django E-Commerce API

A robust, scalable RESTful API for an e-commerce platform built with Django and Django REST Framework. This project supports user authentication, product management, category organization, reviews, and profile management, with JWT-based authentication and email verification.

## Features

- **User Registration & Authentication**: Secure registration, login, logout, JWT authentication via cookies, and email verification.
- **Password Reset**: Secure password reset workflow with email notifications.
- **Profile Management**: Update and retrieve user profile details.
- **Product & Category Management**: CRUD operations for products and categories, including image uploads.
- **Product Reviews**: Nested review endpoints for products, with permissions for customers and owners.
- **Role-Based Permissions**: Admin, SuperAdmin, Customer, and Guest roles for fine-grained access control.
- **Media Handling**: Profile and product image uploads.
- **CORS Support**: Configured for frontend integration.
- **Extensible**: Easily add new features or endpoints.

## Tech Stack

- Django 5.2+
- Django REST Framework
- Simple JWT
- django-rest-passwordreset
- django-filter
- Pillow (image handling)
- SQLite (default, easily swappable)

## Getting Started

### Prerequisites

- Python 3.10+
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

### Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/yourusername/e-commerce-api.git
   cd e-commerce-api
   ```

2. **Create and activate a virtual environment**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:

   ```
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-email-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   SITE_NAME=Your Site Name
   ```

5. **Apply migrations**

   ```sh
   python manage.py migrate
   ```

6. **Create a superuser**

   ```sh
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```sh
   python manage.py runserver
   ```

## API Endpoints

| Endpoint                                 | Description                      |
| ---------------------------------------- | -------------------------------- |
| `/api/auth/register/`                    | User registration                |
| `/api/auth/verify-email/`                | Email verification               |
| `/api/auth/login/`                       | Login (JWT via cookies)          |
| `/api/auth/logout/`                      | Logout                           |
| `/api/auth/refresh/`                     | Refresh JWT token                |
| `/api/auth/profile/`                     | Get/update user profile          |
| `/api/auth/password_reset/`              | Password reset workflow          |
| `/api/products/`                         | Product CRUD, filtering, search  |
| `/api/products/categories/`              | Category CRUD, filtering, search |
| `/api/products/products/<slug>/reviews/` | Nested product reviews           |

## Project Structure

- `accounts/` – User, authentication, profile, permissions
- `products/` – Product, category, review models and endpoints
- `ecommerce/` – Project settings and URLs
- `media/` – Uploaded images
- `templates/` – Email templates

## Testing

Run unit tests with:

```sh
python manage.py test
```

## License

This project is licensed under the MIT License.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

**Contact:**  
For questions or support, please contact [binyamcheru123@gmail.com](mailto:binyamcheru123@gmail.com).
