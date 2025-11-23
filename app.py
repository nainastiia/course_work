from flask import Flask, request, redirect, jsonify
from flasgger import Swagger
from db import get_connection

app = Flask(__name__)
swagger = Swagger(app)
@app.route('/')
def index():
    return redirect('/apidocs/')

@app.route('/clients', methods=['GET'])
def get_clients():
    """
    Отримати всіх клієнтів
    ---
    tags:
      - Clients
    summary: Виводить усіх клієнтів, які зареєстровані у базі даних
    description: |
      Цей метод дозволяє вивести інформацію про усіх клієнтів.
    responses:
      200:
        description: Список клієнтів
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)


@app.route('/clients', methods=['POST'])
def create_client():
    """
    Додати нового клієнта
    ---
    tags:
      - Clients
    summary: Додає нового клієнта до бази даних
    description: |
      Цей метод дозволяє створити нового клієнта.
      Потрібно вказати ім'я, прізвище, телефон та email.
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        example: Анастасія
        description: Ім'я клієнта
      - name: surname
        in: formData
        type: string
        required: true
        example: Мельник
        description: Прізвище клієнта
      - name: phone
        in: formData
        type: string
        required: true
        example: "380501234567"
        description: Номер телефону клієнта
      - name: email
        in: formData
        type: string
        required: true
        example: test@example.com
        description: Email клієнта
    responses:
      201:
        description: Клієнта успішно створено
    """
    data = request.form
    conn = get_connection()
    cursor = conn.cursor()

    sql = """INSERT INTO clients (name, surname, phone, email)
             VALUES (%s, %s, %s, %s)"""

    cursor.execute(sql, (
        data['name'],
        data['surname'],
        data['phone'],
        data['email']
    ))

    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({"message": "Client added", "client_id": new_id}), 201

@app.route('/clients/<int:id>', methods=['PUT'])
def update_client(id):
    """
    Оновити дані клієнта
    ---
    tags:
      - Clients
    summary: Оновлює інформацію про клієнта
    description: |
      Цей метод дозволяє оновити інформацію про клієнта.
      Потрібно обов'язково вказати id клієнта
      та заповнити тільки ті поля, які хочете змінити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: name
        in: formData
        type: string
      - name: surname
        in: formData
        type: string
      - name: phone
        in: formData
        type: string
      - name: email
        in: formData
        type: string
    responses:
      200:
        description: Дані успішно оновлено
    """
    data = request.form
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []
    for key in ['name', 'surname', 'phone', 'email']:
        if key in data:
            fields.append(f"{key}=%s")
            values.append(data[key])

    if not fields:
        return jsonify({"message": "Нічого оновлювати"}), 400

    sql = f"UPDATE clients SET {', '.join(fields)} WHERE client_id=%s"
    values.append(id)
    cur.execute(sql, tuple(values))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Client updated"})

@app.route('/clients/<int:id>', methods=['DELETE'])
def delete_client(id):
    """
    Видалити клієнта
    ---
    tags:
      - Clients
    summary: Видаляє клієнта з бази даних
    description: |
      Цей метод дозволяє видалити клієнта.
      Потрібно вказати лише id клієнта, якого хочете видалити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Клієнта успішно видалено
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM clients WHERE client_id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Deleted"}), 204

@app.route('/bookings', methods=['GET'])
def get_bookings():
    """
    Отримати всі бронювання
    ---
    tags:
      - Bookings
    summary: Виводить список усіх бронювань
    description: |
      Цей метод дозволяє отримати інформацію про всі бронювання.
    responses:
      200:
        description: Список бронювань
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM bookings")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/bookings', methods=['POST'])
def add_booking():
    """
    Додати нове бронювання
    ---
    tags:
      - Bookings
    summary: Додає нове бронювання до бази даних
    description: |
      Цей метод дозволяє створити нове бронювання.
      Потрібно вказати id клієнта, id кімнати,
      дату заїзду та виїзду, загальну суму та статус бронювання.
    parameters:
      - name: client_id
        in: formData
        type: integer
        required: true
        example: 1
      - name: room_id
        in: formData
        type: integer
        required: true
        example: 101
      - name: check_in
        in: formData
        type: string
        format: date
        required: true
        example: "2025-11-20"
      - name: check_out
        in: formData
        type: string
        format: date
        required: true
        example: "2025-11-25"
      - name: total_amount
        in: formData
        type: number
        required: true
        example: 5000
      - name: booking_status
        in: formData
        type: string
        enum: ['confirmed','cancelled','completed']
        required: true
    responses:
      201:
        description: Бронювання успішно створено
    """
    data = request.form
    conn = get_connection()
    cur = conn.cursor()
    sql = """INSERT INTO bookings(client_id, room_id, check_in, check_out, total_amount, booking_status)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cur.execute(sql, (data['client_id'], data['room_id'], data['check_in'], data['check_out'],
                      data['total_amount'], data['booking_status']))
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return jsonify({"message": "Booking created", "id": new_id})

@app.route('/bookings/<int:id>', methods=['PUT'])
def update_booking(id):
    """
    Оновити бронювання
    ---
    tags:
      - Bookings
    summary: Оновлює інформацію про бронювання
    description: |
      Цей метод дозволяє змінити деяку інформацію про бронювання.
      Потрібно обов'язково вказати id бронювання
      та заповнити тільки ті поля, які хочете змінити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: client_id
        in: formData
        type: integer
      - name: room_id
        in: formData
        type: integer
      - name: check_in
        in: formData
        type: string
        format: date
      - name: check_out
        in: formData
        type: string
        format: date
      - name: total_amount
        in: formData
        type: number
      - name: booking_status
        in: formData
        type: string
        enum: ['confirmed','cancelled']
    responses:
      200:
        description: Бронювання успішно оновлено
    """
    data = request.form
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []
    for key in ['client_id', 'room_id', 'check_in', 'check_out', 'total_amount', 'booking_status']:
        if key in data:
            fields.append(f"{key}=%s")
            values.append(data[key])

    if not fields:
        return jsonify({"message": "Нічого оновлювати"}), 400

    sql = f"UPDATE bookings SET {', '.join(fields)} WHERE booking_id=%s"
    values.append(id)
    cur.execute(sql, tuple(values))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Booking updated"})

@app.route('/bookings/<int:id>', methods=['DELETE'])
def delete_booking(id):
    """
    Видалити бронювання
    ---
    tags:
      - Bookings
    summary: Видаляє бронювання з бази даних
    description: |
      Цей метод дозволяє видалити бронювання.
      Потрібно вказати лише id бронювання, яке хочете видалити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Бронювання успішно видалено
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM bookings WHERE booking_id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Booking deleted"}), 204


@app.route('/menuitems', methods=['GET'])
def get_menu_items():
    """
    Отримати всі елементи меню
    ---
    tags:
      - Menu Items
    summary: Виводить список усіх елементів меню
    description: |
      Цей метод дозволяє вивести інформацію про елементи меню.
    responses:
      200:
        description: Список елементів меню
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM menuitems")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/menuitems', methods=['POST'])
def add_menu_item():
    """
    Додати новий елемент меню
    ---
    tags:
      - Menu Items
    summary: Додає новий елемент меню до бази даних
    description: |
      Цей метод дозволяє створити новий елемент меню.
      Потрібно вказати назву елемента, категорію, та ціну.
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        example: "Салат Цезар"
      - name: category
        in: formData
        type: string
        required: true
        example: "Салати"
      - name: price
        in: formData
        type: number
        required: true
        example: 150
    responses:
      201:
        description: Елемент меню успішно створено
    """
    data = request.form
    conn = get_connection()
    cur = conn.cursor()
    sql = """INSERT INTO menuitems(name, category, price)
             VALUES (%s, %s, %s)"""
    cur.execute(sql, (data['name'], data['category'], data['price']))
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return jsonify({"message": "Menu item created", "id": new_id})

@app.route('/menuitems/<int:id>', methods=['PUT'])
def update_menu_item(id):
    """
    Оновити елемент меню
    ---
    tags:
      - Menu Items
    summary: Оновлює дані елемента меню
    description: |
      Цей метод дозволяє змінити інформацію про елемент меню.
      Потрібно обов'язково вказати id елемента,
      та заповнити лише ті поля, які хочете змінити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: name
        in: formData
        type: string
      - name: category
        in: formData
        type: string
      - name: price
        in: formData
        type: number
    responses:
      200:
        description: Елемент меню успішно оновлено
    """
    data = request.form
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []
    for key in ['name', 'category', 'price']:
        if key in data:
            fields.append(f"{key}=%s")
            values.append(data[key])

    if not fields:
        return jsonify({"message": "Нічого оновлювати"}), 400

    sql = f"UPDATE menuitems SET {', '.join(fields)} WHERE dish_id=%s"
    values.append(id)
    cur.execute(sql, tuple(values))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Menu item updated"})

@app.route('/menuitems/<int:id>', methods=['DELETE'])
def delete_menu_item(id):
    """
    Видалити елемент меню
    ---
    tags:
      - Menu Items
    summary: Видаляє елемент меню з бази даних
    description: |
      Цей метод дозволяє видалити елемент меню.
      Потрібно вказати лише id елемента меню, що хочете видалити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Елемент меню успішно видалено
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM menuitems WHERE dish_id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Menu item deleted"}), 204


@app.route('/orders', methods=['GET'])
def get_orders():
    """
    Отримати всі замовлення
    ---
    tags:
      - Orders
    summary: Виводить список усіх замовлень.
    description: |
      Цей метод дозволяє вивести усю інформацію про замовлення.
    responses:
      200:
        description: Список замовлень
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM orders")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/orders', methods=['POST'])
def add_order():
    """
    Додати нове замовлення
    ---
    tags:
      - Orders
    summary: Додає нове замовлення до бази даних
    description: |
      Цей метод дозволяє створити нове замовлення.
      Потрібно вказати id клієнта, id страви,
      дату замовлення, кількість, ціну за 1,
      загальну ціну та статус замовлення .
    parameters:
      - name: client_id
        in: formData
        type: integer
        required: true
        example: 1
      - name: dish_id
        in: formData
        type: integer
        required: true
        example: 1
      - name: order_date
        in: formData
        type: string
        format: date-time
        required: true
        example: "2025-11-16 18:00:00"
      - name: quantity
        in: formData
        type: integer
        required: true
        example: 1
      - name: price
        in: formData
        type: number
        format: float
        required: true
        example: 100.00
      - name: total_amount
        in: formData
        type: number
        format: float
        required: true
        example: 1200.00
      - name: order_status
        in: formData
        type: string
        required: true
        example: new/completed
    responses:
      201:
        description: Замовлення успішно створено
    """
    data = request.form
    conn = get_connection()
    cur = conn.cursor()
    sql = """INSERT INTO orders(client_id, dish_id, order_date, quantity, price, total_amount, order_status)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(sql, (data['client_id'], data['dish_id'], data['order_date'], data['quantity'],  data['price'], data['total_amount'],  data['order_status']))
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return jsonify({"message": "Order created", "id": new_id})

@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    """
    Оновити замовлення
    ---
    tags:
      - Orders
    summary: Оновлює дані замовлення
    description: |
      Цей метод дозволяє оновити інформацію про замовлення.
      Потрібно обов'язково вказати id замовлення,
      та заповнити лише ті поля, які хочете змінити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: client_id
        in: formData
        type: integer
      - name: dish_id
        in: formData
        type: integer
      - name: order_date
        in: formData
        type: string
        format: date-time
      - name: quantity
        in: formData
        type: integer
      - name: price
        in: formData
        type: number
        format: float
      - name: total_amount
        in: formData
        type: number
        format: float
      - name: order_status
        in: formData
        type: string
    responses:
      200:
        description: Замовлення успішно оновлено
    """
    data = request.form
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []
    for key in ['client_id', 'dish_id', 'order_date', 'quantity', 'price', 'total_amount', 'order_status']:
        if key in data:
            fields.append(f"{key}=%s")
            values.append(data[key])

    if not fields:
        return jsonify({"message": "Нічого оновлювати"}), 400

    sql = f"UPDATE orders SET {', '.join(fields)} WHERE order_id=%s"
    values.append(id)
    cur.execute(sql, tuple(values))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Order updated"})

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    """
    Видалити замовлення
    ---
    tags:
      - Orders
    summary: Видаляє замовлення з бази даних
    description: |
      Цей метод дозволяє видалити замовлення.
      Потрібно вказати id замовлення, яке хочете видалити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Замовлення видалено
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE order_id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Order deleted"}), 204


@app.route('/payments', methods=['GET'])
def get_payments():
    """
    Отримати всі оплати
    ---
    tags:
      - Payments
    summary: Виводить список усіх оплат
    description: |
      Цей метод дозволяє вивести усю інформацію про оплати.
    responses:
      200:
        description: Список оплат
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM payments")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/payments', methods=['POST'])
def add_payment():
    """
    Додати нову оплату
    ---
    tags:
      - Payments
    summary: Додає нову оплату до бази даних
    description: |
      Цей метод дозволяє створити нову оплату.
      Потрібно вказати id клієнта, id бронювання,
      id замовлення, дату оплати, суму та спосіб оплати.
    parameters:
      - name: client_id
        in: formData
        type: integer
        required: true
        example: 1
      - name: booking_id
        in: formData
        type: integer
        required: false
        example: 1
      - name: order_id
        in: formData
        type: integer
        required: false
        example: 1
      - name: payment_date
        in: formData
        type: string
        format: date-time
        required: true
        example: "2025-11-16 18:30:00"
      - name: amount
        in: formData
        type: number
        format: float
        required: true
        example: 500.00
      - name: payment_method
        in: formData
        type: string
        enum: ['cash','card','online']
        required: true
    responses:
      201:
        description: Оплата успішно додана
    """
    data = request.form
    conn = get_connection()
    cur = conn.cursor()
    sql = """INSERT INTO payments(client_id, booking_id, order_id, payment_date, amount, payment_method)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cur.execute(sql, (
        data['client_id'], data.get('booking_id'), data.get('order_id'), data['payment_date'], data['amount'],
        data['payment_method']
    ))
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return jsonify({"message": "Payment added", "id": new_id})

@app.route('/payments/<int:id>', methods=['PUT'])
def update_payment(id):
    """
    Оновити оплату
    ---
    tags:
      - Payments
    summary: Оновлює дані оплати
    description: |
      Цей метод дозволяє оновити інформацію про оплату.
      Потрібно обов'язково вказати id оплати, та заповнити лише ті поля,
      які хочете змінити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: client_id
        in: formData
        type: integer
      - name: booking_id
        in: formData
        type: integer
      - name: order_id
        in: formData
        type: integer
      - name: payment_date
        in: formData
        type: string
        format: date-time
      - name: amount
        in: formData
        type: number
        format: float
      - name: payment_method
        in: formData
        type: string
    responses:
      200:
        description: Оплата успішно оновлена
    """
    data = request.form
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []
    for key in ['client_id', 'booking_id', 'order_id', 'payment_date', 'amount', 'payment_method']:
        if key in data:
            fields.append(f"{key}=%s")
            values.append(data[key])

    if not fields:
        return jsonify({"message": "Нічого оновлювати"}), 400

    sql = f"UPDATE payments SET {', '.join(fields)} WHERE payment_id=%s"
    values.append(id)
    cur.execute(sql, tuple(values))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Payment updated"})

@app.route('/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    """
    Видалити оплату
    ---
    tags:
      - Payments
    summary: Видаляє оплату з бази даних
    description: |
      Цей метод дозволяє видалити оплату.
      Потрібно вказати id оплати, яку хочете видалити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Оплата успішно видалена
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM payments WHERE payment_id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Payment deleted"}), 204


@app.route('/rooms', methods=['GET'])
def get_rooms():
    """
    Отримати всі номери готелю
    ---
    tags:
      - Rooms
    summary: Виводить список усіх номерів готелю
    description: |
      Цей метод дозволяє вивести усю інформацію про номери готелю.
    responses:
      200:
        description: Список номерів
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM rooms")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/rooms', methods=['POST'])
def add_room():
    """
    Додати новий номер
    ---
    tags:
      - Rooms
    summary: Додає новий номер до бази даних
    description: |
      Цей метод дозволяє створити новий номер.
      Потрібно вказати № номера, тип, ціну на 1 ніч та статус.
    parameters:
      - name: room_number
        in: formData
        type: integer
        required: true
        example: "101"
      - name: type
        in: formData
        type: string
        required: true
        example: "Люкс"
      - name: price
        in: formData
        type: number
        format: float
        required: true
        example: 2000.00
      - name: room_status
        in: formData
        type: string
        required: true
        example: available/booked/maintenance
    responses:
      201:
        description: Номер успішно додано
    """
    data = request.form
    conn = get_connection()
    cur = conn.cursor()
    sql = """INSERT INTO rooms(room_number, type, price, room_status)
             VALUES (%s, %s, %s, %s)"""
    cur.execute(sql, (
        data['room_number'], data['type'], data['price'], data['room_status']
    ))
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return jsonify({"message": "Room added", "id": new_id})

@app.route('/rooms/<int:id>', methods=['PUT'])
def update_room(id):
    """
    Оновити номер
    ---
    tags:
      - Rooms
    summary: Оновлює дані номера
    description: |
      Цей метод дозволяє оновити інформацію про номер.
      Потрібно обов'язково вказати id номера, та заповнити лише ті поля,
      які хочете змінити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: room_number
        in: formData
        type: integer
      - name: type
        in: formData
        type: string
      - name: price
        in: formData
        type: number
        format: float
      - name: room_status
        in: formData
        type: string
    responses:
      200:
        description: Номер успішно оновлено
    """
    data = request.form
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []
    for key in ['room_number', 'type', 'price', 'room_status']:
        if key in data:
            fields.append(f"{key}=%s")
            values.append(data[key])

    if not fields:
        return jsonify({"message": "Нічого оновлювати"}), 400

    sql = f"UPDATE rooms SET {', '.join(fields)} WHERE room_id=%s"
    values.append(id)
    cur.execute(sql, tuple(values))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Room updated"})

@app.route('/rooms/<int:id>', methods=['DELETE'])
def delete_room(id):
    """
    Видалити номер
    ---
    tags:
      - Rooms
    summary: Видаляє номер з бази даних
    description: |
      Цей метод дозволяє видалити номер.
      Потрібно обов'язково вказати id номера, який хочете видалити.
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Номер успішно видалено
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM rooms WHERE room_id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Room deleted"}), 204


if __name__ == '__main__':
    app.run(debug=True)
