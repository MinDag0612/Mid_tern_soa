-- 1. Tạo database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = N'TuitionDB')
BEGIN
    CREATE DATABASE TuitionDB;
END
GO

USE TuitionDB;
GO

-- 2. Bảng account
IF OBJECT_ID('dbo.account', 'U') IS NOT NULL DROP TABLE dbo.account;
CREATE TABLE dbo.account (
    id INT IDENTITY(1,1) PRIMARY KEY,
    userName VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- 3. Bảng CustomerInfor
IF OBJECT_ID('dbo.CustomerInfor', 'U') IS NOT NULL DROP TABLE dbo.CustomerInfor;
CREATE TABLE dbo.CustomerInfor (
    id INT IDENTITY(1,1) PRIMARY KEY,
    fullName VARCHAR(50) NOT NULL,
    phoneNumber VARCHAR(20) UNIQUE,
    email VARCHAR(50) UNIQUE,
    balance FLOAT
);

-- 4. Bảng history
IF OBJECT_ID('dbo.history', 'U') IS NOT NULL DROP TABLE dbo.history;
CREATE TABLE dbo.history (
    id INT IDENTITY(1,1) PRIMARY KEY,
    idTransaction VARCHAR(20) UNIQUE,
    studentId VARCHAR(20),
    tuition FLOAT,
    dayComplete DATETIME,
    payer VARCHAR(50),
    email VARCHAR(50) UNIQUE
);

-- 5. Bảng tuition
IF OBJECT_ID('dbo.tuition', 'U') IS NOT NULL DROP TABLE dbo.tuition;
CREATE TABLE dbo.tuition (
    idTransaction VARCHAR(20) PRIMARY KEY,
    studentId VARCHAR(20),
    studentName VARCHAR(50),
    tuition FLOAT
);

-- 6. Ràng buộc quan hệ (có thể điều chỉnh nếu bạn muốn liên kết chặt chẽ hơn)
-- account 1-1 CustomerInfor
ALTER TABLE dbo.CustomerInfor
ADD CONSTRAINT FK_CustomerInfor_Account
FOREIGN KEY (id) REFERENCES dbo.account(id);

-- CustomerInfor 1-n history (qua email)
ALTER TABLE dbo.history
ADD CONSTRAINT FK_History_CustomerInfor
FOREIGN KEY (email) REFERENCES dbo.CustomerInfor(email);

-- history 1-n tuition (qua idTransaction)
ALTER TABLE dbo.tuition
ADD CONSTRAINT FK_Tuition_History
FOREIGN KEY (idTransaction) REFERENCES dbo.history(idTransaction);

INSERT INTO dbo.account (userName, password)
VALUES 
    ('admin', 'admin123'),
    ('student01', 'pass01'),
    ('student02', 'pass02');

SET IDENTITY_INSERT CustomerInfor ON;
INSERT INTO dbo.CustomerInfor (id, fullName, phoneNumber, email, balance)
VALUES
    (1, 'Nguyen Van A', '0901234567', 'a@example.com', 5000000),
    (2, 'Tran Thi B',   '0912345678', 'b@example.com', 3000000),
    (3, 'Le Van C',     '0923456789', 'c@example.com', 4500000);
SET IDENTITY_INSERT CustomerInfor OFF;


INSERT INTO dbo.history (idTransaction, studentId, tuition, dayComplete, payer, email)
VALUES
    ('TXN001', 'ST001', 1500000, GETDATE(), 'Nguyen Van A', 'a@example.com'),
    ('TXN002', 'ST002', 2000000, GETDATE(), 'Tran Thi B',   'b@example.com');

INSERT INTO dbo.tuition (idTransaction, studentId, studentName, tuition)
VALUES
    ('TXN001', 'ST001', 'Nguyen Van A', 1500000),
    ('TXN002', 'ST002', 'Tran Thi B',   2000000);

select * from tuition