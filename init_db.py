"""
Initialize database with sample data
Run this script once to populate the database with sample users
"""
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, User
import models

def init_database():
    """
    Create tables and insert sample data
    """
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully\n")
    
    # Create database session
    db = SessionLocal()
    
    # Sample users data (2 per role = 8 users)
    sample_users = [
        # Admins
        {
            "name": "John Smith",
            "email": "john.admin@realagent.com",
            "role": "Admin",
            "password": User.hash_password("admin123")
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.admin@realagent.com",
            "role": "Admin",
            "password": User.hash_password("admin456")
        },
        
        # Players
        {
            "name": "Michael Torres",
            "email": "michael.player@realagent.com",
            "role": "Player",
            "password": User.hash_password("player123")
        },
        {
            "name": "David Martinez",
            "email": "david.player@realagent.com",
            "role": "Player",
            "password": User.hash_password("player456")
        },
        
        # Agents
        {
            "name": "Robert Wilson",
            "email": "robert.agent@realagent.com",
            "role": "Agent",
            "password": User.hash_password("agent123")
        },
        {
            "name": "Jennifer Brown",
            "email": "jennifer.agent@realagent.com",
            "role": "Agent",
            "password": User.hash_password("agent456")
        },
        
        # Club Managers
        {
            "name": "James Anderson",
            "email": "james.manager@realagent.com",
            "role": "Club Manager",
            "password": User.hash_password("manager123")
        },
        {
            "name": "Patricia Taylor",
            "email": "patricia.manager@realagent.com",
            "role": "Club Manager",
            "password": User.hash_password("manager456")
        }
    ]
    
    print("Inserting sample users...")
    print("-" * 80)
    
    for user_data in sample_users:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        
        if existing_user:
            print(f"⊘ User {user_data['email']} already exists, skipping...")
        else:
            user = User(**user_data)
            db.add(user)
            print(f"✓ Inserted: {user_data['name']} - {user_data['role']}")
    
    db.commit()
    print("-" * 80)
    print("✓ Sample data inserted successfully\n")
    
    # Display all users
    print("Current users in database:")
    print("=" * 80)
    
    users = db.query(User).all()
    
    for user in users:
        print(f"[{user.user_id}] {user.name:<25} {user.email:<35} {user.role:<15}")
    
    print("=" * 80)
    print(f"Total users: {len(users)}\n")
    
    # Display statistics by role
    print("Users by role:")
    print("-" * 80)
    roles = ['Admin', 'Player', 'Agent', 'Club Manager']
    
    for role in roles:
        count = db.query(User).filter(User.role == role).count()
        print(f"{role:<15}: {count} users")
    
    print("-" * 80)
    
    db.close()
    print("\n✓ Database initialization complete!")

def reset_database():
    """
    Drop all tables and recreate them (use with caution!)
    """
    print("⚠️  WARNING: This will delete all data!")
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() == 'yes':
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✓ All tables dropped")
        
        print("Recreating tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Tables recreated\n")
        
        print("Database has been reset. Run init_database() to add sample data.")
    else:
        print("Reset cancelled.")

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("REAL AGENT DATABASE INITIALIZATION")
    print("=" * 80 + "\n")
    
    init_database()