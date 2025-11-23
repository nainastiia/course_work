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
coursework2/ 
- app.py
- db.py
- README.md

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

## Доступні ендпоінти
### Clients
- GET /clients — отримати всіх клієнтів
- POST /clients — створити клієнта
- PUT /clients/<id> — змінити клієнта
- DELETE /clients/<id> — видалити клієнта

### Bookings
- GET /bookings
- POST /bookings
- PUT /bookings/<id>
- DELETE /bookings/<id>

### Menu Items
- GET /menuitems
- POST /menuitems
- PUT /menuitems/<id>
- DELETE /menuitems/<id>

### Orders
- GET /orders
- POST /orders
- PUT /orders/<id>
- DELETE /orders/<id>

### Payments
- GET /payments
- POST /payments
- PUT /payments/<id>
- DELETE /payments/<id>

### Rooms
- GET /rooms
- POST /rooms
- PUT /rooms/<id>
- DELETE /rooms/<id>

---

## Автор курсової роботи
**Студентка групи ФЕП-23с – Най А. М.**
## Науковий керівник
**Асистент - Мисюк Р.В.**