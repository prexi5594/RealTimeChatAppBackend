Real-Time Chat Application 
Supports: 

- User signup
- User login
- Chat rooms
- Sending messages
- Fetching messages
- Polling-based real-time updates

---

# Tech Stack

- Python
- Flask
- Flask SQLAlchemy
- Flask CORS
- SQLite

---

# Project Structure

```bash
backend/
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
│
├── database/
│   └── chat.db
│
├── models/
│   ├── __init__.py
│   ├── user_model.py
│   ├── room_model.py
│   └── message_model.py
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── room_routes.py
│   └── message_routes.py
│
├── utils/
│   └── helpers.py
│
└── venv/
```

---

## Chat Rooms

Default rooms:

- General
- Sports
. Fashion
. politics

# Installation

## Clone Repository

```bash
git clone 


# Create Virtual Environment

python3 -m venv venv

Activate:
source venv/bin/activate

# Install Dependencies


pip install -r requirements.txt

 Run Backend

Start server:
python app.py


