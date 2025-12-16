"""
FastAPI Main Application
Real Agent System - Backend API
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import models
import schemas
import crud
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Real Agent API",
    description="Backend API for Real Agent System - User Management",
    version="1.0.0"
)

# Mount frontend files (if needed)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Configure CORS (for connecting with HTML/CSS frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint - serve frontend
@app.get("/")
def read_root():
    """Serve the main frontend page"""
    return FileResponse("frontend/index.html")

# API info endpoint
@app.get("/api")
def api_info():
    """API information endpoint"""
    return {
        "message": "Welcome to Real Agent API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "users": "/users",
            "login": "/auth/login"
        }
    }

# Health check
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Real Agent API"}

# Frontend routes
@app.get("/about")
def about_page():
    """Serve the about page"""
    return FileResponse("frontend/about.html")

@app.get("/contact")
def contact_page():
    """Serve the contact page"""
    return FileResponse("frontend/contact.html")

# ============ USER CRUD ENDPOINTS ============

# CREATE - Register new user
@app.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    # Check if email already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return crud.create_user(db=db, user=user)

# READ - Get all users
@app.get("/users/", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all users with pagination
    """
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users

# READ - Get user by ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

# READ - Get users by role
@app.get("/users/role/{role}", response_model=List[schemas.UserResponse])
def read_users_by_role(role: str, db: Session = Depends(get_db)):
    """
    Get all users with a specific role
    """
    valid_roles = ['Admin', 'Player', 'Agent', 'Club Manager']
    if role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}"
        )
    
    users = crud.get_users_by_role(db, role=role)
    return users

# UPDATE - Update user
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Update user information
    """
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

# DELETE - Delete user
@app.delete("/users/{user_id}", response_model=schemas.MessageResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user
    """
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return schemas.MessageResponse(message="User deleted successfully")

# ============ AUTHENTICATION ENDPOINTS ============

@app.post("/auth/login", response_model=schemas.LoginResponse)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and login
    """
    user = crud.authenticate_user(db, email=credentials.email, password=credentials.password)
    
    if not user:
        return schemas.LoginResponse(
            success=False,
            message="Invalid email or password",
            user=None
        )
    
    return schemas.LoginResponse(
        success=True,
        message="Login successful",
        user=schemas.UserResponse.model_validate(user)
    )

# ============ STATISTICS ENDPOINTS ============

@app.get("/stats/users")
def get_user_statistics(db: Session = Depends(get_db)):
    """
    Get user statistics
    """
    total_users = crud.get_user_count(db)
    role_counts = crud.get_all_roles_count(db)
    active_users = len(crud.get_active_users(db))
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "by_role": role_counts
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 