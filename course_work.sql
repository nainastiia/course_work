CREATE DATABASE coursework;
USE cousework;
CREATE TABLE Clients (
    client_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    surname VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(50)
);
INSERT INTO Clients (name, surname, phone, email) VALUES
('Олена', 'Іваненко', '+380501112233', 'olena@gmail.com'),
('Андрій', 'Петренко', '+380631234567', 'andriy@mail.com'),
('Марія', 'Коваль', '+380671112233', 'maria@mail.com'),
('Ігор', 'Сидоренко', '+380971234567', 'igor@gmail.com'),
('Світлана', 'Мельник', '+380661234567', 'svitlana@mail.com');

CREATE TABLE Rooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    room_number INT UNIQUE,
    type VARCHAR(50),
    price DECIMAL(8,2),
    status VARCHAR(20) DEFAULT 'available'
);
INSERT INTO Rooms (room_number, type, price, status) VALUES
(101, 'Single', 500.00, 'available'),
(102, 'Double', 750.00, 'occupied'),
(103, 'Suite', 1500.00, 'available'),
(201, 'Double', 800.00, 'available'),
(202, 'Suite', 1600.00, 'occupied');

CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,           
    client_id INT NOT NULL,                           
    room_id INT NOT NULL,                                
    check_in DATE NOT NULL,                              
    check_out DATE NOT NULL,                            
    total_amount DECIMAL(10,2) NOT NULL,               
    booking_status ENUM('confirmed','cancelled','completed') DEFAULT 'confirmed', 
    FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE CASCADE
);
INSERT INTO bookings (client_id, room_id, check_in, check_out, total_amount, booking_status) VALUES
(1, 1, '2025-11-20', '2025-11-25', 2500.00, 'confirmed'),
(2, 1, '2025-11-18', '2025-11-22', 3000.00, 'confirmed'),
(3, 1, '2025-11-19', '2025-11-23', 6000.00, 'confirmed'),
(4, 2, '2025-11-21', '2025-11-24', 2400.00, 'confirmed'),
(5, 2, '2025-11-20', '2025-11-22', 3200.00, 'confirmed');

CREATE TABLE MenuItems (
    dish_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    category VARCHAR(30),
    price DECIMAL(8,2)
);
INSERT INTO MenuItems (name, category, price) VALUES
('Борщ', 'Супи', 100.00),
('Салат Цезар', 'Салати', 150.00),
('Стейк Рібай', 'Основні страви', 250.00),
('Паста Карбонара', 'Основні страви', 180.00),
('Чай Зелений', 'Напої', 45.00),
('Кава Лате', 'Напої', 70.00);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT,
    dish_id INT,
    order_date DATE,
    quantity INT,
    price DECIMAL(8,2),
    total_amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'new',
    FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE
);
INSERT INTO Orders (client_id, dish_id, order_date, quantity, price, total_amount, status) VALUES
(1, 6, '2025-11-18', 1, 70.00, 570.00, 'completed'),
(1, 3, '2025-11-18', 2, 250.00, 570.00, 'completed'),
(2, 2, '2025-11-18', 1, 150.00, 195.00, 'completed'),
(2, 5, '2025-11-18', 2, 45.00, 195.00, 'completed'),
(3, 4, '2025-11-19', 1, 180.00, 180.00, 'new'),
(4, 6, '2025-11-19', 2, 70.00, 140.00, 'new'),
(5, 1, '2025-11-18', 1, 100.00, 500.00, 'completed'),
(5, 2, '2025-11-18', 1, 150.00, 500.00, 'completed'),
(5, 3, '2025-11-18', 1, 250.00, 500.00, 'completed');

CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,                    
    booking_id INT,                              
    order_id INT,                                
    payment_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('cash','card','online') DEFAULT 'card',
    FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE
);
INSERT INTO Payments (client_id, booking_id, order_id, payment_date, amount, payment_method) VALUES
(1, 1, NULL, '2025-11-18', 2500.00, 'card'),       
(2, 2, NULL, '2025-11-18', 3000.00, 'cash'),      
(1, NULL, 1, '2025-11-18', 570.00, 'card'),        
(2, NULL, 2, '2025-11-18', 195.00, 'cash'),        
(5, 5, 9, '2025-11-18', 3700.00, 'online'); 