-- =====================================================================
-- Кейс-задача № 4. Схема БД для WEB-приложения (MS SQL Server)
-- Эквивалент SQLite-схемы из app.py, но в синтаксисе T-SQL.
-- Применяется при развёртывании на MS SQL Server (как требует задание).
-- =====================================================================

IF DB_ID('TourismWeb') IS NULL
    CREATE DATABASE TourismWeb;
GO
USE TourismWeb;
GO

IF OBJECT_ID('dbo.requests', 'U') IS NOT NULL DROP TABLE dbo.requests;
IF OBJECT_ID('dbo.tours', 'U')    IS NOT NULL DROP TABLE dbo.tours;
GO

CREATE TABLE dbo.tours (
    tour_id  INT IDENTITY(1,1) PRIMARY KEY,
    title    NVARCHAR(150) NOT NULL,
    country  NVARCHAR(100) NOT NULL,
    nights   INT NOT NULL CHECK (nights > 0),
    price    DECIMAL(10,2) NOT NULL CHECK (price >= 0)
);
GO

CREATE TABLE dbo.requests (
    request_id INT IDENTITY(1,1) PRIMARY KEY,
    tour_id    INT NOT NULL,
    client     NVARCHAR(150) NOT NULL,
    phone      NVARCHAR(20)  NOT NULL,
    persons    INT NOT NULL CHECK (persons > 0),
    created_at DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    CONSTRAINT fk_requests_tour FOREIGN KEY (tour_id) REFERENCES dbo.tours(tour_id)
);
GO

INSERT INTO dbo.tours (title, country, nights, price) VALUES
    (N'Турция всё включено', N'Турция', 7, 45000),
    (N'Выходные в Риме',     N'Италия', 3, 60000),
    (N'Пляжный Пхукет',      N'Таиланд', 10, 85000);
GO
