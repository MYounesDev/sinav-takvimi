"""
Authentication Utilities
"""

import bcrypt
from typing import Optional, Dict
from src.database.db_manager import db_manager


class AuthService:
    """Handle user authentication"""
    
    @staticmethod
    def login(email: str, password: str) -> Optional[Dict]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email
            password: User password (plain text)
            
        Returns:
            User dict if successful, None otherwise
        """
        query = """
            SELECT u.*, d.name as department_name, d.code as department_code
            FROM users u
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.email = ?
        """
        
        results = db_manager.execute_query(query, (email,))
        
        if not results:
            return None
        
        user_row = results[0]
        stored_password = user_row['password']
        
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return {
                'id': user_row['id'],
                'name': user_row['name'],
                'email': user_row['email'],
                'role': user_row['role'],
                'department_id': user_row['department_id'],
                'department_name': user_row['department_name'],
                'department_code': user_row['department_code']
            }
        
        return None
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def create_user(name: str, email: str, password: str, role: str, department_id: int) -> int:
        """
        Create a new user
        
        Args:
            name: User name
            email: User email
            password: Plain text password
            role: User role (admin or coordinator)
            department_id: Department ID
            
        Returns:
            New user ID
        """
        hashed_password = AuthService.hash_password(password)
        
        query = """
            INSERT INTO users (name, email, password, role, department_id)
            VALUES (?, ?, ?, ?, ?)
        """
        
        return db_manager.execute_update(query, (name, email, hashed_password, role, department_id))


# Current logged-in user (global state)
current_user: Optional[Dict] = None


def set_current_user(user: Dict):
    """Set the currently logged-in user"""
    global current_user
    current_user = user


def get_current_user() -> Optional[Dict]:
    """Get the currently logged-in user"""
    return current_user


def logout():
    """Logout the current user"""
    global current_user
    current_user = None


