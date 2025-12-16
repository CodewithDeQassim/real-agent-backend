# Real Agent System - Assignment 2: User Roles & Database (Back-End Design)

## 📋 Project Overview
This is the back-end implementation for the Real Agent system using **FastAPI** and **SQLAlchemy**. The system features a complete REST API for user management with four distinct user roles, CRUD operations, and authentication.

## 🛠️ Technology Stack
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM (Object-Relational Mapping)
- **SQLite** - Lightweight database
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server for running the application

## 👥 User Roles Defined
The system supports four user roles:
1. **Admin** - System administrators with full access
2. **Player** - Football players registered in the system
3. **Agent** - Player agents who manage player contracts
4. **Club Manager** - Football club managers

## 🗄️ Database Schema

### Users Table (SQLAlchemy Model)
| Field | Type | Constraints |
|-------|------|-------------|
| user_id | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| name | STRING | NOT NULL |
| email | STRING | UNIQUE, NOT NULL, INDEXED |
| role | STRING | NOT NULL, CHECK (Admin/Player/Agent/Club Manager) |
| password | STRING | NOT NULL (SHA-256 hashed) |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| last_login | DATETIME | NULLABLE |
| is_active | BOOLEAN | DEFAULT TRUE |

## 📊 Sample Data
The database includes 2 sample users for each role (8 users total):

### Admins
- John Smith (john.admin@realagent.com) - Password: admin123
- Sarah Johnson (sarah.admin@realagent.com) - Password: admin456

### Players
- Michael Torres (michael.player@realagent.com) - Password: player123
- David Martinez (david.player@realagent.com) - Password: player456

### Agents
- Robert Wilson (robert.agent@realagent.com) - Password: agent123
- Jennifer Brown (jennifer.agent@realagent.com) - Password: agent456

### Club Managers
- James Anderson (james.manager@realagent.com) - Password: manager123
- Patricia Taylor (patricia.manager@realagent.com) - Password: manager456

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/real-agent-backend.git
cd real-agent-backend
```

2. **Create a virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Initialize the database with sample data:**
```bash
python init_db.py
```

## 💻 Running the Application

### Start the FastAPI server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at: **http://localhost:8000**

### Access Interactive API Documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### General Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message and API info |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive API documentation |

### User CRUD Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |
| GET | `/users/` | Get all users (with pagination) |
| GET | `/users/{user_id}` | Get user by ID |
| GET | `/users/role/{role}` | Get users by role |
| PUT | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Delete user |

### Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | User login/authentication |

### Statistics Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stats/users` | Get user statistics |

## 🔧 API Usage Examples

### 1. Create a New User (POST)
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New User",
    "email": "newuser@realagent.com",
    "role": "Player",
    "password": "password123"
  }'
```

### 2. Get All Users (GET)
```bash
curl http://localhost:8000/users/
```

### 3. Get User by ID (GET)
```bash
curl http://localhost:8000/users/1
```

### 4. Get Users by Role (GET)
```bash
curl http://localhost:8000/users/role/Player
```

### 5. Update User (PUT)
```bash
curl -X PUT "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "email": "updated@realagent.com"
  }'
```

### 6. Delete User (DELETE)
```bash
curl -X DELETE http://localhost:8000/users/1
```

### 7. Login (POST)
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.admin@realagent.com",
    "password": "admin123"
  }'
```

### 8. Get Statistics (GET)
```bash
curl http://localhost:8000/stats/users
```

## 📁 Project Structure
```
real-agent-backend/
├── main.py                 # FastAPI application & routes
├── database.py             # Database configuration
├── models.py               # SQLAlchemy models (User table)
├── schemas.py              # Pydantic schemas (validation)
├── crud.py                 # CRUD operations
├── init_db.py              # Database initialization script
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── real_agent.db           # SQLite database (created after init)
└── screenshots/            # Database screenshots
    ├── api_docs.png
    ├── database_schema.png
    └── sample_data.png
```

## 🔐 Security Features
- **Password Hashing**: All passwords hashed using SHA-256
- **Data Validation**: Pydantic schemas validate all input data
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **Email Validation**: Pydantic EmailStr validates email format
- **Role Validation**: Database constraint ensures valid roles
- **CORS Enabled**: Allows connection with frontend

## 🎯 What is SQLAlchemy?

**SQLAlchemy** is an ORM (Object-Relational Mapping) that lets you work with databases using Python objects instead of raw SQL.

### Traditional Way (Raw SQL):
```python
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
```

### SQLAlchemy Way (Python Objects):
```python
user = User(name="John", email="john@example.com")
db.add(user)
db.commit()
```

### Benefits:
✅ Write Python code instead of SQL  
✅ Automatic table creation from models  
✅ Type safety and validation  
✅ Easy database migrations  
✅ Works with multiple databases (SQLite, PostgreSQL, MySQL)

## 🌐 Connecting to Your HTML/CSS Frontend

### Using JavaScript Fetch API:
```javascript
// Login Example
async function login(email, password) {
    const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    
    if (data.success) {
        console.log('Login successful:', data.user);
    } else {
        console.log('Login failed:', data.message);
    }
}

// Get All Users Example
async function getUsers() {
    const response = await fetch('http://localhost:8000/users/');
    const users = await response.json();
    console.log(users);
}
```

## 🧪 Testing the API

### Using the Interactive Docs (Recommended):
1. Start the server: `python main.py`
2. Open browser: http://localhost:8000/docs
3. Click on any endpoint to test it
4. Click "Try it out" and fill in the parameters
5. Click "Execute" to see the results

### Using Postman or Thunder Client:
Import the API endpoints and test each CRUD operation.

## 📸 Taking Screenshots

### For Database Schema:
1. Use **DB Browser for SQLite** (free tool)
2. Open `real_agent.db`
3. Go to "Database Structure" tab
4. Take screenshot

### For Sample Data:
1. In DB Browser, go to "Browse Data" tab
2. Select `users` table
3. Take screenshot showing all sample users

### For API Documentation:
1. Go to http://localhost:8000/docs
2. Take screenshot of the API endpoints

## 🎯 Assignment Requirements Checklist
- [x] Define user roles (Admin, Player, Agent, Club Manager)
- [x] Create database using SQLAlchemy + SQLite
- [x] Insert sample data (2 users per role = 8 total)
- [x] Backend code with full CRUD operations
- [x] User authentication functionality
- [x] RESTful API with FastAPI
- [x] Password hashing for security
- [x] Data validation with Pydantic
- [x] README with clear instructions
- [x] Professional project structure

## 🔄 Advanced Features Included
- ✨ RESTful API design
- ✨ Interactive API documentation (Swagger UI)
- ✨ Request/response validation
- ✨ Pagination support
- ✨ Statistics endpoint
- ✨ CORS enabled for frontend integration
- ✨ Proper error handling
- ✨ Type hints throughout

## 👨‍💻 Author
[Your Name]  
Student ID: [Your ID]  
Limkokwing University of Creative Technology  
Faculty of Information & Communications Technology  
September 2025

## 📝 License
This project is submitted as part of Assignment 2 for the Web Programming Technique module.

## 🙏 Acknowledgments
- Limkokwing University of Creative Technology
- Web Programming Technique Module Instructor
- FastAPI Documentation
- SQLAlchemy Documentation