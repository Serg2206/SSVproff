# Change Password Script - User Guide

## Overview

The `change_password.py` script has been **enhanced** to support both:
1. ✅ **Updating passwords** for existing users
2. ✅ **Creating new users** if they don't exist

## What Changed?

### Before
- ❌ Could only update passwords for existing users
- ❌ Failed with error when user doesn't exist: "Пользователь 'SSV' не найден в базе данных"

### After
- ✅ Updates passwords for existing users
- ✅ **Creates new users automatically** if they don't exist
- ✅ New users are created with:
  - Default email: `{username}@example.com`
  - Role: Superuser (full admin rights)
  - Status: Active

## Usage

### Basic Syntax
```bash
python change_password.py <username> <new_password>
```

### Example 1: Update Existing User Password
```bash
python change_password.py admin newpassword123
```

**Output:**
```
🔄 Изменение пароля пользователя
============================================================
👤 Пользователь найден: admin
🔒 Хеширование нового пароля...
✅ Успешно! Пароль для пользователя 'admin' был изменён
📧 Email: admin@example.com
🔑 Роль: Суперпользователь
📊 Статус: Активен
🕐 Обновлено: 2025-10-16 23:22:47.618074
============================================================
✅ Операция завершена успешно!
```

### Example 2: Create New User
```bash
python change_password.py SSV SSV1963ssv
```

**Output:**
```
➕ Создание нового пользователя
============================================================
👤 Пользователь 'SSV' не найден
📝 Создание нового пользователя...
🔒 Хеширование пароля...
✅ Успешно! Новый пользователь 'SSV' создан
📧 Email: SSV@example.com
🔑 Роль: Суперпользователь
📊 Статус: Активен
🕐 Создан: 2025-10-16 23:22:39.534899
============================================================
✅ Операция завершена успешно!

⚠️  Рекомендации:
   1. Email по умолчанию: SSV@example.com
   2. Пользователь создан с правами суперпользователя
   3. Измените email при необходимости через интерфейс
```

## Password Requirements

- Minimum length: **6 characters**
- Maximum length: Unlimited (bcrypt will handle it)
- No special character requirements (but recommended for security)

## Features

### Automatic User Detection
The script automatically detects whether a user exists:
- If user exists → Updates password
- If user doesn't exist → Creates new user

### Secure Password Hashing
All passwords are hashed using **bcrypt** before storage:
- Industry-standard encryption
- Salt automatically generated
- Passwords never stored in plain text

### Default User Settings (for new users)
| Field | Value |
|-------|-------|
| Email | `{username}@example.com` |
| Role | Superuser (Admin) |
| Status | Active |
| Created | Current timestamp |

## Testing Results

### ✅ Test 1: Create New User 'SSV'
```bash
python change_password.py SSV SSV1963ssv
```
**Result:** ✅ SUCCESS - User created successfully

### ✅ Test 2: Update Existing User 'admin'
```bash
python change_password.py admin newpassword123
```
**Result:** ✅ SUCCESS - Password updated successfully

### ✅ Test 3: Database Verification
Users in database after testing:
- testuser (Regular user)
- admin (Superuser)
- newuser (Regular user)
- **SSV (Superuser)** ← New user created by script

## Error Handling

### Invalid Arguments
```bash
python change_password.py
```
**Output:**
```
❌ Неверное количество аргументов
============================================================
📖 Использование:
   python change_password.py <username> <new_password>

📝 Примеры:
   python change_password.py admin newpassword123
   python change_password.py john secretpassword

💡 Скрипт выполнит:
   • Если пользователь существует → обновит пароль
   • Если пользователь не существует → создаст нового пользователя
============================================================
```

### Password Too Short
```bash
python change_password.py testuser 123
```
**Output:**
```
❌ Ошибка: Пароль должен содержать минимум 6 символов
```

### Empty Username
```bash
python change_password.py "" password123
```
**Output:**
```
❌ Ошибка: Имя пользователя не может быть пустым
```

## Git Changes

### Commit Details
- **Branch:** `feat/comprehensive-config-no-workflows`
- **Commit:** `fix: Update change_password.py to support user creation`
- **Files Changed:** `api/change_password.py`
- **Status:** ✅ Successfully pushed to remote

### Changes Summary
```
+108 insertions
-105 deletions
```

**Key improvements:**
1. Added `update_or_create_user()` function
2. Automatic user creation with sensible defaults
3. Enhanced error messages in Russian
4. Better user feedback with emojis
5. Comprehensive validation

## Recommendations

### Security Best Practices
1. **Change default passwords immediately** after user creation
2. **Update email addresses** from default `{username}@example.com`
3. **Use strong passwords** (mix of letters, numbers, symbols)
4. **Review user permissions** regularly

### Production Use
1. Consider adding email validation
2. Implement password strength requirements
3. Add email notifications for new users
4. Log user creation/password changes

## Location

- **Script Path:** `/home/ubuntu/github_repos/SSVproff/api/change_password.py`
- **Repository:** `https://github.com/Serg2206/SSVproff`
- **Branch:** `feat/comprehensive-config-no-workflows`

## Support

For issues or questions:
1. Check the help message: `python change_password.py`
2. Review error messages for guidance
3. Consult this guide

---

**Last Updated:** October 16, 2025  
**Script Version:** 2.0 (Enhanced with user creation support)
