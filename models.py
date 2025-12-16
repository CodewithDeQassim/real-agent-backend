"""
SQLAlchemy Models - Define database tables as Python classes
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint
from sqlalchemy.sql import func
from database import Base
import hashlib

class User(Base):
    """
    User model representing the users table in the database
    """
    __tablename__ = "users"
    
    # Columns
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Add constraint to ensure role is valid
    __table_args__ = (
        CheckConstraint(
            role.in_(['Admin', 'Player', 'Agent', 'Club Manager']),
            name='valid_role_check'
        ),
    )
    
    def __repr__(self):
        return f"<User(id={self.user_id}, name='{self.name}', role='{self.role}')>"
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return self.password == self.hash_password(password)