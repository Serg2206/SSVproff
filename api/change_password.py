#!/usr/bin/env python3
"""
Скрипт для изменения пароля пользователя в системе SSVproff

Использование:
    python change_password.py <имя_пользователя> <новый_пароль>

Пример:
    python change_password.py admin MyNewSecurePassword123

Требования:
    - Новый пароль должен быть минимум 8 символов
    - Пользователь должен существовать в базе данных
"""

import sys
import os
from pathlib import Path

# Добавляем путь к модулям приложения
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash


def validate_password(password: str) -> tuple[bool, str]:
    """
    Валидация нового пароля
    
    Args:
        password: Пароль для проверки
        
    Returns:
        tuple: (успешность проверки, сообщение об ошибке)
    """
    if len(password) < 8:
        return False, "❌ Ошибка: Пароль должен содержать минимум 8 символов"
    
    if len(password) > 72:
        return False, "❌ Ошибка: Пароль не может быть длиннее 72 символов"
    
    return True, ""


def change_user_password(username: str, new_password: str) -> bool:
    """
    Изменение пароля пользователя
    
    Args:
        username: Имя пользователя
        new_password: Новый пароль (будет захеширован)
        
    Returns:
        bool: True если пароль успешно изменён, False в противном случае
    """
    # Валидация пароля
    is_valid, error_message = validate_password(new_password)
    if not is_valid:
        print(error_message)
        return False
    
    # Создание сессии базы данных
    db = SessionLocal()
    
    try:
        # Поиск пользователя по имени
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            print(f"❌ Ошибка: Пользователь '{username}' не найден в базе данных")
            return False
        
        # Хеширование нового пароля
        print(f"🔐 Хеширование нового пароля...")
        hashed_password = get_password_hash(new_password)
        
        # Обновление пароля в базе данных
        user.hashed_password = hashed_password
        db.commit()
        
        print(f"✅ Успешно! Пароль для пользователя '{username}' был изменён")
        print(f"📧 Email: {user.email}")
        print(f"🔑 Роль: {'Суперпользователь' if user.is_superuser else 'Обычный пользователь'}")
        print(f"📊 Статус: {'Активен' if user.is_active else 'Неактивен'}")
        print(f"🕒 Обновлено: {user.updated_at}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при изменении пароля: {str(e)}")
        db.rollback()
        return False
        
    finally:
        db.close()


def print_usage():
    """Вывод инструкции по использованию"""
    print("=" * 70)
    print("📝 Скрипт изменения пароля пользователя SSVproff")
    print("=" * 70)
    print()
    print("Использование:")
    print("    python change_password.py <имя_пользователя> <новый_пароль>")
    print()
    print("Пример:")
    print("    python change_password.py admin MyNewSecurePassword123")
    print()
    print("Требования:")
    print("    • Новый пароль должен содержать минимум 8 символов")
    print("    • Новый пароль не может быть длиннее 72 символов")
    print("    • Пользователь должен существовать в базе данных")
    print()
    print("=" * 70)


def main():
    """Основная функция"""
    # Проверка аргументов командной строки
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)
    
    username = sys.argv[1]
    new_password = sys.argv[2]
    
    print()
    print("=" * 70)
    print("🔄 Изменение пароля пользователя")
    print("=" * 70)
    print()
    
    # Изменение пароля
    success = change_user_password(username, new_password)
    
    print()
    print("=" * 70)
    
    if success:
        print("✅ Операция завершена успешно!")
        sys.exit(0)
    else:
        print("❌ Операция завершена с ошибкой")
        sys.exit(1)


if __name__ == "__main__":
    main()
