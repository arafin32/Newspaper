# Django Newspaper Application

A simple newspaper/blog application built with Django, allowing users to view articles and post comments.

## Features

-   View a list of recent articles on the homepage.
-   View individual articles with full content.
-   Authenticated users can post comments on articles.
-   User authentication (login, logout) using Django's built-in system.
-   Admin interface for managing articles and comments.

## Project Structure

-   **Newspaper/**: The main Django project directory.
    -   `settings.py`: Project settings.
    -   `urls.py`: Project-level URL routing.
-   **articles/**: A Django app for managing articles and comments.
    -   `models.py`: Defines `Article` and `Comment` database models.
    -   `views.py`: Contains view logic for displaying articles and handling comments.
    -   `urls.py`: App-specific URL routing for articles.
    -   `templates/`: HTML templates for rendering pages.
    -   `tests.py`: Unit tests for the `articles` app.
-   **manage.py**: Django's command-line utility.
-   **requirements.txt**: Python dependencies.
-   **db.sqlite3**: SQLite database file (default for development).

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for accessing the admin panel):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create a username and password.

## Running the Development Server

1.  **Start the server:**
    ```bash
    python manage.py runserver
    ```

2.  Open your web browser and navigate to `http://127.0.0.1:8000/`.
    -   The admin panel is accessible at `http://127.0.0.1:8000/admin/`.

## Running Tests

To run the automated tests for the `articles` app:

```bash
python manage.py test articles
```
