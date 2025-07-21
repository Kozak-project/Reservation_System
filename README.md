# 🏨 Room Reservation API

This is a RESTful API for managing hotel room reservations, built with Python using Flask and SQLAlchemy. It allows basic user registration, room listing, and room booking functionality. The project is modular, testable, and ready for future extension.

---

## 🧩 Features

- ✅ User creation and retrieval
- 🏠 Room listing and management
- 📅 Room reservation creation and lookup
- 🧪 Unit testing with `pytest`
- 🔐 Environment variable support via `.env`
- 🗃️ MySQL database support using SQLAlchemy ORM

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Kozak-project/Reservation_System.git
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
FLASK_ENV=development
```

### 5. Run the application

```bash
python app.py
```

The server will start on `http://localhost:5000`.

---

## 🧪 Running Tests

```bash
pytest
```

Tests are written with `pytest` and located in the `tests/` directory.

---

## 📁 Project Structure

```
├── src/
│   ├── app.py                
│   ├── database.py           
│   ├── models.py             
│   └── routes/
│       ├── __init__.py
│       ├── users.py          
│       ├── rooms.py          
│       └── reservations.py   
│
├── tests/
│   ├── test_users.py
│   └── test_rooms.py
│
├── requirements.txt
├── .env                      
└── README.md
```

---

## 🛠 Tech Stack

- Python 3.12
- Flask 2.3
- SQLAlchemy 2.0.30
- MySQL
- Pytest for testing
- python-dotenv for config

---

## 👤 Author

Built by Kacper Kozak https://github.com/Kozak-project
Feel free to connect or share feedback!
