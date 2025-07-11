# Mental Health Counselor AI

A Django-based mental health counseling chatbot powered by Groq's LLM API.

## Features

- Real-time chat interface with AI counselor
- Multiple LLM model support (Llama 3.1, Llama 3.3)
- Custom prompt engineering capabilities
- Resource management system
- User preferences and settings
- Dynamic site customization
- Secure authentication system

## Setup

1. Clone the repository
```bash
git clone https://github.com/imahmoud79/myproject-final.git
cd myproject-final
```

2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with:
```
DJANGO_SECRET_KEY=your-secret-key
GROQ_API_KEY=your_groq_api_key_here
```

4. Run migrations
```bash
python manage.py migrate
```

5. Run the development server
```bash
python manage.py runserver
```

## Environment Variables

The following environment variables are required:

- `DJANGO_SECRET_KEY`: Your Django secret key
- `GROQ_API_KEY`: Your Groq API key for LLM access

## Project Structure

- `myproject/`: Main Django project directory
  - `chat/`: Chat application with AI counselor functionality
  - `users/`: User authentication and management
  - `templates/`: HTML templates
  - `static/`: Static files (CSS, JavaScript)
  - `media/`: User uploaded files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# ChatCare
