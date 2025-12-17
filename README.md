# Hotel & Restaurant Management API
Цей проєкт — REST API на Flask для керування системою готелю/ресторану. 
Він забезпечує повноцінний CRUD для:
- клієнтів
- бронювань
- елементів меню
- замовлень
- оплат

Документація доступна через **Swagger UI (Flasgger)**.

---

## Структура проєкту
course_work/ 
- app.py / містить логіку роботи інформаційної системи
- db.py / використовується для підключення до бази даних
- README.md / містить опис проєкту
- course_work.sql / містить SQL-скрипт створення бази даних

---

## Встановлення та запуск
### 1. Створити віртуальне середовище
```bash
python -m venv venv
source venv/bin/activate     # Linux / macOS
venv\Scripts\activate        # Windows
```

### 2. Імпортування бібліотек
```bash
pip install flask
pip install flasgger
pip install mysql-connector-python
```

### 3. Запуск сервера
```bash
python app.py
```
1. Сервер запускається за адресою:
- http://127.0.0.1:5000/
2. Відкрийте її у браузері.
3. Вас буде автоматично перенаправлено на сторінку API-документації (`/apidocs/`).
Окремо відкривати її не потрібно.
 
---

## Доступні операції
### Clients
- GET /clients — отримати всіх клієнтів
- POST /clients — створити клієнта
- PUT /clients/<id> — змінити клієнта
- DELETE /clients/<id> — видалити клієнта

### Bookings
- GET /bookings - отримати всі бронювання
- POST /bookings - створити бронювання
- PUT /bookings/<id> - змінити бронювання
- DELETE /bookings/<id> - видалити бронювання

### Menu Items
- GET /menuitems - отримати всі елементи меню
- POST /menuitems - створити елемент меню
- PUT /menuitems/<id> - змінити елемент меню
- DELETE /menuitems/<id> - видалити елемент меню

### Orders
- GET /orders - отримати всі замовлення
- POST /orders - створити замовлення
- PUT /orders/<id> - змінити замовлення
- DELETE /orders/<id> - видалити замовлення

### Payments
- GET /payments - отримати всі оплати
- POST /payments - створити оплату
- PUT /payments/<id> - змінити оплату
- DELETE /payments/<id> - видалити оплату

### Rooms
- GET /rooms - отримати всі кімнати 
- POST /rooms - створити кімнату
- PUT /rooms/<id> - змінити кімнату
- DELETE /rooms/<id> - видалити кімнату

---

## Автор курсової роботи
**Студентка групи ФЕП-23с – Най А. М.**
## Науковий керівник
**Асистент - Мисюк Р.В.**