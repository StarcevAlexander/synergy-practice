-- =====================================================================
-- Кейс-задача № 3. База данных «Туризм»
-- СУБД: MySQL 8.x (диалект совместим с MySQL Workbench)
-- Состав: 3 таблицы-справочника + 1 таблица-справочник (туры)
--         + 1 таблица переменной информации (заказы туров).
-- =====================================================================

DROP DATABASE IF EXISTS tourism;
CREATE DATABASE tourism CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tourism;

-- ---------------------------------------------------------------------
-- Справочник 1. Страны/направления
-- ---------------------------------------------------------------------
CREATE TABLE countries (
    country_id   INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    visa_required TINYINT(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Справочник 2. Отели
-- ---------------------------------------------------------------------
CREATE TABLE hotels (
    hotel_id     INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(150) NOT NULL,
    stars        TINYINT NOT NULL CHECK (stars BETWEEN 1 AND 5),
    country_id   INT NOT NULL,
    CONSTRAINT fk_hotels_country
        FOREIGN KEY (country_id) REFERENCES countries(country_id)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Справочник 3. Клиенты
-- ---------------------------------------------------------------------
CREATE TABLE clients (
    client_id    INT AUTO_INCREMENT PRIMARY KEY,
    full_name    VARCHAR(150) NOT NULL,
    phone        VARCHAR(20),
    email        VARCHAR(120) UNIQUE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Справочник 4. Туры (предоставляемые услуги)
-- ---------------------------------------------------------------------
CREATE TABLE tours (
    tour_id      INT AUTO_INCREMENT PRIMARY KEY,
    title        VARCHAR(150) NOT NULL,
    hotel_id     INT NOT NULL,
    nights       INT NOT NULL CHECK (nights > 0),
    price_per_person DECIMAL(10,2) NOT NULL CHECK (price_per_person >= 0),
    CONSTRAINT fk_tours_hotel
        FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Таблица переменной информации. Заказы туров
-- Внешние ключи ссылаются на ключевые атрибуты справочников.
-- ---------------------------------------------------------------------
CREATE TABLE orders (
    order_id     INT AUTO_INCREMENT PRIMARY KEY,
    client_id    INT NOT NULL,
    tour_id      INT NOT NULL,
    order_date   DATE NOT NULL,
    persons      INT NOT NULL CHECK (persons > 0),
    status       ENUM('новый','оплачен','завершён','отменён') NOT NULL DEFAULT 'новый',
    CONSTRAINT fk_orders_client
        FOREIGN KEY (client_id) REFERENCES clients(client_id),
    CONSTRAINT fk_orders_tour
        FOREIGN KEY (tour_id) REFERENCES tours(tour_id)
) ENGINE=InnoDB;

CREATE INDEX idx_orders_client ON orders(client_id);
CREATE INDEX idx_orders_tour   ON orders(tour_id);
CREATE INDEX idx_orders_date   ON orders(order_date);

-- =====================================================================
-- Тестовые данные
-- =====================================================================
INSERT INTO countries (name, visa_required) VALUES
    ('Турция', 0),
    ('Италия', 1),
    ('Таиланд', 0);

INSERT INTO hotels (name, stars, country_id) VALUES
    ('Antalya Resort', 5, 1),
    ('Roma Centrale', 4, 2),
    ('Phuket Beach', 4, 3);

INSERT INTO clients (full_name, phone, email) VALUES
    ('Иванов Иван Иванович', '+79001112233', 'ivanov@example.com'),
    ('Петрова Анна Сергеевна', '+79004445566', 'petrova@example.com');

INSERT INTO tours (title, hotel_id, nights, price_per_person) VALUES
    ('Турция всё включено', 1, 7, 45000.00),
    ('Выходные в Риме', 2, 3, 60000.00),
    ('Пляжный Пхукет', 3, 10, 85000.00);

INSERT INTO orders (client_id, tour_id, order_date, persons, status) VALUES
    (1, 1, '2026-06-20', 2, 'оплачен'),
    (2, 3, '2026-07-01', 1, 'новый'),
    (1, 2, '2026-07-10', 3, 'новый');

-- =====================================================================
-- Примеры аналитических запросов
-- =====================================================================

-- 1) Полная информация по заказам со стоимостью
SELECT o.order_id,
       c.full_name,
       t.title           AS tour,
       co.name           AS country,
       h.name            AS hotel,
       o.persons,
       (t.price_per_person * o.persons) AS total_cost,
       o.status
FROM orders o
JOIN clients   c  ON c.client_id  = o.client_id
JOIN tours     t  ON t.tour_id    = o.tour_id
JOIN hotels    h  ON h.hotel_id   = t.hotel_id
JOIN countries co ON co.country_id = h.country_id
ORDER BY o.order_date;

-- 2) Выручка по странам
SELECT co.name AS country,
       SUM(t.price_per_person * o.persons) AS revenue
FROM orders o
JOIN tours t      ON t.tour_id = o.tour_id
JOIN hotels h     ON h.hotel_id = t.hotel_id
JOIN countries co ON co.country_id = h.country_id
GROUP BY co.name
ORDER BY revenue DESC;
