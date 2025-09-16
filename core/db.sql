-- Schema và dữ liệu mẫu cho MySQL
-- Sử dụng cùng cấu hình với docker-compose (database TuitionDB, user sa/12345)

CREATE DATABASE IF NOT EXISTS TuitionDB
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE TuitionDB;

-- Xóa bảng cũ nếu tồn tại (đảm bảo thứ tự do ràng buộc khóa ngoại)
DROP TABLE IF EXISTS tuition;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS CustomerInfor;
DROP TABLE IF EXISTS account;

-- Bảng account
CREATE TABLE account (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userName VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bảng CustomerInfor (1-1 với account qua khóa chính)
CREATE TABLE CustomerInfor (
    id INT PRIMARY KEY,
    fullName VARCHAR(50) NOT NULL,
    phoneNumber VARCHAR(20) UNIQUE,
    email VARCHAR(50) UNIQUE,
    balance DECIMAL(15,2),
    CONSTRAINT FK_CustomerInfor_Account FOREIGN KEY (id) REFERENCES account(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bảng history
CREATE TABLE history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idTransaction VARCHAR(20) UNIQUE,
    studentId VARCHAR(20),
    tuition DECIMAL(15,2),
    dayComplete DATETIME,
    payer VARCHAR(50),
    email VARCHAR(50),
    CONSTRAINT FK_History_CustomerInfor FOREIGN KEY (email) REFERENCES CustomerInfor(email) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bảng tuition
CREATE TABLE tuition (
    idTransaction VARCHAR(20) PRIMARY KEY,
    studentId VARCHAR(20),
    studentName VARCHAR(50),
    tuition DECIMAL(15,2),
    CONSTRAINT FK_Tuition_History FOREIGN KEY (idTransaction) REFERENCES history(idTransaction) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu mẫu
INSERT INTO account (userName, password) VALUES
    ('admin', '$2b$12$ByWI/aiBcz5.ojnuAKJ.ueuwT1MPL2X5vd5Klx5yDsRkk0.PoX1dS'),
    ('student01', '$2b$12$J0/ryTNcS0btK0uRkTj0f.zASkMVRWRnxytSQ01BGBqoxz.M3aTDq'),
    ('student02', '$2b$12$CQaG1mDCWWwMJ2bAS1gBBub8wA8G1ARqlMRy2oGcuWQzypI6JapBG');

INSERT INTO CustomerInfor (id, fullName, phoneNumber, email, balance) VALUES
    (1, 'Nguyen Van A', '0901234567', 'a@example.com', 5000000),
    (2, 'Tran Thi B',   '0912345678', 'b@example.com', 3000000),
    (3, 'Le Van C',     '0923456789', 'c@example.com', 4500000);

INSERT INTO history (idTransaction, studentId, tuition, dayComplete, payer, email) VALUES
    ('TXN001', 'ST001', 1500000, NOW(), 'Nguyen Van A', 'a@example.com'),
    ('TXN002', 'ST002', 2000000, NOW(), 'Tran Thi B',   'b@example.com');

INSERT INTO tuition (idTransaction, studentId, studentName, tuition) VALUES
    ('TXN001', 'ST001', 'Nguyen Van A', 1500000),
    ('TXN002', 'ST002', 'Tran Thi B',   2000000);
