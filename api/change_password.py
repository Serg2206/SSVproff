#!/usr/bin/env python3
"""
User password management script.

This script allows you to update passwords for existing users
or create new users if they don't exist.

Usage:
    python change_password.py <username> <new_password>
    
Examples:
    # Update password for existing user
    python change_password.py admin newpassword123
    
    # Create new user (if doesn't exist)
    python change_password.py john secretpassword
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


def update_or_create_user(username: str, new_password: str) -> bool:
    """
    Update password for existing user or create new user if doesn't exist.
    
    Args:
        username: Username to update or create
        new_password: New password to set
        
    Returns:
        True if operation successful, False otherwise
    """
    db = SessionLocal()
    
    try:
        # Check if user exists
        user = db.query(User).filter(User.username == username).first()
        
        if user:
            # User exists - update password
            print(f"🔄 Изменение пароля пользователя")
            print("=" * 60)
            print(f"👤 Пользователь найден: {username}")
            print("🔒 Хеширование нового пароля...")
            
            user.hashed_password = get_password_hash(new_password)
            user.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(user)
            
            print(f"✅ Успешно! Пароль для пользователя '{username}' был изменён")
            print(f"📧 Email: {user.email}")
            print(f"🔑 Роль: {'Суперпользователь' if user.is_superuser else 'Пользователь'}")
            print(f"📊 Статус: {'Активен' if user.is_active else 'Неактивен'}")
            print(f"🕐 Обновлено: {user.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f')}")
            print("=" * 60)
            print("✅ Операция завершена успешно!")
            
            return True
        else:
            # User doesn't exist - create new user
            print(f"➕ Создание нового пользователя")
            print("=" * 60)
            print(f"👤 Пользователь '{username}' не найден")
            print("📝 Создание нового пользователя...")
            print("🔒 Хеширование пароля...")
            
            new_user = User(
                email=f"{username}@example.com",
                username=username,
                hashed_password=get_password_hash(new_password),
                is_active=True,
                is_superuser=True,  # New users are created as superusers
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            print(f"✅ Успешно! Новый пользователь '{username}' создан")
            print(f"📧 Email: {new_user.email}")
            print(f"🔑 Роль: Суперпользователь")
            print(f"📊 Статус: Активен")
            print(f"🕐 Создан: {new_user.created_at.strftime('%Y-%m-%d %H:%M:%S.%f')}")
            print("=" * 60)
            print("✅ Операция завершена успешно!")
            print("\n⚠️  Рекомендации:")
            print(f"   1. Email по умолчанию: {new_user.email}")
            print(f"   2. Пользователь создан с правами суперпользователя")
            print(f"   3. Измените email при необходимости через интерфейс")
            
            return True
            
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        print("=" * 60)
        print("❌ Операция завершена с ошибкой")
        db.rollback()
        return False
        
    finally:
        db.close()


def main() -> None:
    """Main function."""
    # Check command line arguments
    if len(sys.argv) != 3:
        print("=" * 60)
        print("❌ Неверное количество аргументов")
        print("=" * 60)
        print("\n📖 Использование:")
        print(f"   python {sys.argv[0]} <username> <new_password>")
        print("\n📝 Примеры:")
        print(f"   python {sys.argv[0]} admin newpassword123")
        print(f"   python {sys.argv[0]} john secretpassword")
        print("\n💡 Скрипт выполнит:")
        print("   • Если пользователь существует → обновит пароль")
        print("   • Если пользователь не существует → создаст нового пользователя")
        print("=" * 60)
        sys.exit(1)
    
    username = sys.argv[1]
    new_password = sys.argv[2]
    
    # Validate inputs
    if not username or not username.strip():
        print("❌ Ошибка: Имя пользователя не может быть пустым")
        sys.exit(1)
    
    if not new_password or len(new_password) < 6:
        print("❌ Ошибка: Пароль должен содержать минимум 6 символов")
        sys.exit(1)
    
    # Update or create user
    success = update_or_create_user(username.strip(), new_password)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
