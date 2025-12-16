"""
CRUD operations for User model
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import User
from schemas import UserCreate, UserUpdate
from typing import List, Optional
from datetime import datetime

# CREATE
def create_user(db: Session, user: UserCreate) -> User:
    
   # Create a new user in the database
    
    hashed_password = User.hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        role=user.role,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# READ
def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Get a user by ID
    """
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email
    """
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Get all users with pagination
    """
    return db.query(User).offset(skip).limit(limit).all()

def get_users_by_role(db: Session, role: str) -> List[User]:
    """
    Get all users with a specific role
    """
    return db.query(User).filter(User.role == role).all()

def get_active_users(db: Session) -> List[User]:
    """
    Get all active users
    """
    return db.query(User).filter(User.is_active == True).all()

# UPDATE
def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """
    Update user information
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    # Update only provided fields
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Hash password if it's being updated
    if 'password' in update_data:
        update_data['password'] = User.hash_password(update_data['password'])
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# DELETE
def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user from the database
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

# AUTHENTICATION
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not user.is_active:
        return None
    if not user.verify_password(password):
        return None
    
    # Update last login time
    user.last_login = datetime.now()
    db.commit()
    
    return user

# STATISTICS
def get_user_count(db: Session) -> int:
    """
    Get total number of users
    """
    return db.query(User).count()

def get_user_count_by_role(db: Session, role: str) -> int:
    """
    Get count of users by role
    """
    return db.query(User).filter(User.role == role).count()

def get_all_roles_count(db: Session) -> dict:
    """
    Get count of users for each role
    """
    return {
        'Admin': get_user_count_by_role(db, 'Admin'),
        'Player': get_user_count_by_role(db, 'Player'),
        'Agent': get_user_count_by_role(db, 'Agent'),
        'Club Manager': get_user_count_by_role(db, 'Club Manager')
    }