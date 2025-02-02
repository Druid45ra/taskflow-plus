# Taskflow Plus

Taskflow Plus is a task management application built with FastAPI, SQLAlchemy, and WebSockets. It allows users to create, update, and manage tasks, and provides real-time notifications via email and WebSockets.

## Features

- User registration and authentication
- Task creation, update, and deletion
- Real-time task notifications via WebSockets
- Email notifications for task updates
- Role-based access control

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/taskflow-plus.git
    cd taskflow-plus
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    python scripts/init_db.py
    ```

5. Generate mock data (optional):
    ```sh
    python scripts/generate_mock.py
    ```

6. Run the application:
    ```sh
    uvicorn app.main:app --reload
    ```

## Usage

- Access the API documentation at `http://localhost:8000/docs`
- Register a new user via the `/users/register` endpoint
- Log in to obtain an access token via the `/users/login` endpoint
- Use the access token to authenticate requests to the `/tasks` endpoints

## Running Tests

1. Install test dependencies:
    ```sh
    pip install -r requirements-test.txt
    ```

2. Run the tests:
    ```sh
    pytest
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
