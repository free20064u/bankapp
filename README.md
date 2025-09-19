# bankapp

An app used for personal banking purposes.

## Features

- Account creation and management
- Balance inquiry
- Fund transfer between accounts
- Transaction history
- Deposit and withdrawal
- User authentication (login/register)
- Notifications for account activities

## Technology

- **Backend & Web Framework:** Django
- **Database:** SQLite (default with Django, can be changed)

## Getting Started

### Prerequisites

- Python 3.8+
- Pip

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/bankapp.git
   ```
2. Create a virtual environment:
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```
     .venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source .venv/bin/activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```
   python manage.py migrate
   ```
6. Start the development server:
   ```
   python manage.py runserver
   ```

## Project Structure

```
bankapp/
├── .venv/
├── bankapp/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── README.md
└── requirements.txt
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

MIT License