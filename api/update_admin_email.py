#!/usr/bin/env python3
"""
Update SSV admin user email script.

This script updates the email address for the SSV user and ensures
they have superuser privileges.

Usage:
    python update_admin_email.py
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


def update_admin_email() -> bool:
    """
    Update email for SSV user and ensure superuser privileges.
    
    Returns:
        True if operation successful, False otherwise
    """
    db = SessionLocal()
    
    try:
        username = "SSV"
        new_email = "ssvnauka@gmail.com"
        
        # Check if user exists
        user = db.query(User).filter(User.username == username).first()
        
        if user:
            # User exists - update email and ensure superuser
            print(f"🔄 Обновление информации пользователя")
            print("=" * 60)
            print(f"👤 Пользователь найден: {username}")
            print(f"📧 Текущий email: {user.email}")
            print(f"📧 Новый email: {new_email}")
            print("🔄 Обновление...")
            
            # Update email
            user.email = new_email
            
            # Ensure user is superuser
            if not user.is_superuser:
                print("🔑 Установка прав суперпользователя...")
                user.is_superuser = True
            
            # Ensure user is active
            if not user.is_active:
                print("📊 Активация пользователя...")
                user.is_active = True
            
            user.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(user)
            
            print()
            print("=" * 60)
            print("✅ Успешно! Информация пользователя обновлена")
            print("=" * 60)
            print()
            print("📋 Информация о пользователе:")
            print(f"   👤 Имя пользователя: {user.username}")
            print(f"   🆔 USER ID: {user.id}")
            print(f"   📧 EMAIL: {user.email}")
            print(f"   🔑 Роль: {'✓ Суперпользователь' if user.is_superuser else 'Пользователь'}")
            print(f"   📊 Статус: {'✓ Активен' if user.is_active else '✗ Неактивен'}")
            print(f"   📅 Создан: {user.created_at.strftime('%d.%m.%Y %H:%M:%S')}")
            print(f"   🕐 Обновлено: {user.updated_at.strftime('%d.%m.%Y %H:%M:%S')}")
            print()
            print("=" * 60)
            print("✅ Операция завершена успешно!")
            print("=" * 60)
            
            return True
        else:
            # User doesn't exist - create new user
            print(f"➕ Создание нового пользователя SSV")
            print("=" * 60)
            print(f"👤 Пользователь '{username}' не найден в базе данных")
            print("📝 Создание нового пользователя...")
            print(f"📧 Email: {new_email}")
            print("🔒 Генерация временного пароля...")
            
            # Create user with default password that must be changed
            default_password = "SSV1963ssv"
            
            new_user = User(
                email=new_email,
                username=username,
                hashed_password=get_password_hash(default_password),
                is_active=True,
                is_superuser=True,
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            print()
            print("=" * 60)
            print("✅ Успешно! Новый пользователь создан")
            print("=" * 60)
            print()
            print("📋 Информация о пользователе:")
            print(f"   👤 Имя пользователя: {new_user.username}")
            print(f"   🆔 USER ID: {new_user.id}")
            print(f"   📧 EMAIL: {new_user.email}")
            print(f"   🔑 Роль: ✓ Суперпользователь")
            print(f"   📊 Статус: ✓ Активен")
            print(f"   📅 Создан: {new_user.created_at.strftime('%d.%m.%Y %H:%M:%S')}")
            print()
            print("⚠️  ВАЖНО: Временный пароль")
            print("=" * 60)
            print(f"   Пароль: {default_password}")
            print()
            print("   ⚠️  ОБЯЗАТЕЛЬНО измените пароль с помощью команды:")
            print(f"      python change_password.py {username} <ваш_новый_пароль>")
            print()
            print("=" * 60)
            print("✅ Операция завершена успешно!")
            print("=" * 60)
            
            return True
            
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Ошибка: {str(e)}")
        print("=" * 60)
        print("❌ Операция завершена с ошибкой")
        print()
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
        
    finally:
        db.close()


def main() -> None:
    """Main function."""
    print()
    print("=" * 60)
    print("🔧 Скрипт обновления email администратора SSV")
    print("=" * 60)
    print()
    print("📝 Этот скрипт выполнит:")
    print("   • Найдет пользователя 'SSV' в базе данных")
    print("   • Обновит email на ssvnauka@gmail.com")
    print("   • Убедится что пользователь является суперпользователем")
    print("   • Если пользователь не найден - создаст нового")
    print()
    
    # Confirm before proceeding
    try:
        response = input("❓ Продолжить? (y/n): ").strip().lower()
        if response not in ['y', 'yes', 'д', 'да']:
            print()
            print("❌ Операция отменена пользователем")
            print()
            sys.exit(0)
    except KeyboardInterrupt:
        print()
        print("\n❌ Операция прервана пользователем")
        print()
        sys.exit(0)
    
    print()
    
    # Update admin email
    success = update_admin_email()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
