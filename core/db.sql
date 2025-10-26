-- Schema và dữ liệu mẫu cho MySQL
-- Sử dụng cùng cấu hình với docker-compose (database TuitionDB, user sa/12345)

CREATE DATABASE IF NOT EXISTS TuitionDB
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE TuitionDB;

-- Xóa bảng cũ nếu tồn tại (đảm bảo thứ tự do ràng buộc khóa ngoại)
DROP TABLE IF EXISTS payment_otp;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS tuition;
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
    balance DECIMAL(15,2) NOT NULL DEFAULT 0,
    CONSTRAINT FK_CustomerInfor_Account FOREIGN KEY (id) REFERENCES account(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bảng tuition lưu các khoản phải đóng
CREATE TABLE tuition (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idTransaction VARCHAR(20) NOT NULL UNIQUE,
    studentId VARCHAR(20) NOT NULL,
    studentName VARCHAR(50) NOT NULL,
    tuition DECIMAL(15,2) NOT NULL,
    is_paid TINYINT(1) NOT NULL DEFAULT 0,
    paid_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bảng history ghi nhận giao dịch thanh toán thành công
CREATE TABLE history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idTransaction VARCHAR(20) NOT NULL UNIQUE,
    studentId VARCHAR(20) NOT NULL,
    tuition DECIMAL(15,2) NOT NULL,
    dayComplete DATETIME NOT NULL,
    payer VARCHAR(50) NOT NULL,
    email VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'SUCCESS',
    customer_id INT NULL,
    CONSTRAINT FK_History_Tuition FOREIGN KEY (idTransaction) REFERENCES tuition(idTransaction) ON DELETE CASCADE,
    CONSTRAINT FK_History_CustomerInfor FOREIGN KEY (customer_id) REFERENCES CustomerInfor(id) ON DELETE SET NULL,
    CONSTRAINT FK_History_CustomerEmail FOREIGN KEY (email) REFERENCES CustomerInfor(email) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bảng payment_otp quản lý OTP cho từng giao dịch
CREATE TABLE payment_otp (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idTransaction VARCHAR(20) NOT NULL,
    otp_code VARCHAR(10) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_PaymentOtp_Tuition FOREIGN KEY (idTransaction) REFERENCES tuition(idTransaction) ON DELETE CASCADE,
    INDEX idx_payment_otp_transaction (idTransaction)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dữ liệu mẫu
INSERT INTO account (id, userName, password) VALUES
    (1, 'admin', '$argon2id$v=19$m=65536,t=3,p=4$c/Ymj4DqrZdIbEfk9PGrMg$Py0BxZ0tIO8d+PaiF5kQBX15IWfTqI4+vAhc4E9nfpo'),
    (2, 'student01', '$argon2id$v=19$m=65536,t=3,p=4$GkcEhlywxisXiQ/ISYqw8A$WtBSuIzraRFpw1bpK2C3EZ6/Rpe0190JOY5gcR/ya/0'),
    (3, 'student02', '$argon2id$v=19$m=65536,t=3,p=4$pycZecLhHB/gA4sBjMlPNA$MImdvw5rVt1zCiBJrurjQKpRJW7NGNkDX+xnNx9olPg');

INSERT INTO CustomerInfor (id, fullName, phoneNumber, email, balance) VALUES
    (1, 'Nguyen Van A', '0901234567', 'a@example.com', 5000000),
    (2, 'Tran Thi B',   '0912345678', 'b@example.com', 3000000),
    (3, 'Le Van C',     '0923456789', 'c@example.com', 4500000);

INSERT INTO tuition (id, idTransaction, studentId, studentName, tuition, is_paid, paid_at) VALUES
    (1, 'TXN001', 'ST001', 'Nguyen Van A', 1500000, 1, NOW()),
    (2, 'TXN002', 'ST002', 'Tran Thi B',   2000000, 1, NOW()),
    (3, 'TXN003', 'ST003', 'Le Van C',     1800000, 0, NULL);

INSERT INTO history (id, idTransaction, studentId, tuition, dayComplete, payer, email, status, customer_id) VALUES
    (1, 'TXN001', 'ST001', 1500000, NOW(), 'Nguyen Van A', 'a@example.com', 'SUCCESS', 1),
    (2, 'TXN002', 'ST002', 2000000, NOW(), 'Tran Thi B',   'b@example.com', 'SUCCESS', 2);
