# Hệ thống quản lý học phí (FastAPI + MySQL)

Ứng dụng FastAPI cung cấp API đăng nhập và tra cứu học phí, sử dụng MySQL làm cơ sở dữ liệu. Tài liệu này hướng dẫn cấu hình biến môi trường, chạy bằng Python thuần hoặc triển khai với Docker Compose (kèm container MySQL).

## Cấu trúc thư mục chính

```
.
├── api/                # Khai báo các router FastAPI
│   ├── account.py
│   └── tuition.py
├── core/
│   └── connDB.py       # Khởi tạo kết nối MySQL (SQLAlchemy)
├── repositories/       # Tầng truy vấn dữ liệu
├── schemas/            # Định nghĩa schema Pydantic
├── services/           # Xử lý nghiệp vụ
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.txt
```

## Biến môi trường (`.env`)

Sao chép file mẫu và cập nhật thông tin theo môi trường của bạn:

```
cp .env.example .env
```

Các biến quan trọng:

- `APP_HOST`, `APP_PORT`: host/port mà Uvicorn lắng nghe.
- `DB_HOST`, `DB_PORT`: địa chỉ và cổng MySQL (mặc định sử dụng service `mysql` trong Docker).
- `DB_NAME`: tên database.
- `DB_USER`, `DB_PASSWORD`: tài khoản ứng dụng để kết nối MySQL.
- `DB_ROOT_PASSWORD`: mật khẩu root (dùng khi khởi tạo MySQL trong Docker).
- `DB_CHARSET`: charset mặc định (giữ `utf8mb4`).

## Chạy local với Python

1. Tạo môi trường ảo và cài phụ thuộc:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Đảm bảo MySQL đang chạy và các biến trong `.env` trỏ đúng tới database.
3. Khởi chạy FastAPI:
   ```bash
   uvicorn api.main:app --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8000} --reload
   ```
4. Truy cập `http://127.0.0.1:8000` để kiểm tra.

## Triển khai với Docker Compose

1. Cập nhật `.env` theo nhu cầu (thông tin database sẽ được dùng để tạo user/DB trong container MySQL).
2. Xây dựng và chạy toàn bộ stack (API + MySQL):
   ```bash
   docker compose up --build
   ```
3. API sẽ lắng nghe tại `http://localhost:${APP_PORT}` và MySQL mở cổng 3306 cho máy chủ.
4. Dừng dịch vụ khi không dùng:
   ```bash
   docker compose down
   ```

### Chạy nền (detached) và xem log

- Chạy dịch vụ ở chế độ nền:
  ```bash
  docker compose up --build -d
  ```
- Xem log của API:
  ```bash
  docker compose logs -f api
  ```
- Tắt toàn bộ stack khi hoàn tất:
  ```bash
  docker compose down
  ```

## Khởi tạo dữ liệu MySQL

- Script `core/db.sql` đã chuyển sang cú pháp MySQL, tạo database `TuitionDB` và dữ liệu mẫu.
- Nếu chạy MySQL ngoài Docker, import script bằng:
  ```bash
  mysql -u sa -p TuitionDB < core/db.sql
  ```
- Khi dùng Docker Compose, có thể chạy ngay trong container:
  ```bash
  docker compose exec mysql mysql -u sa -p TuitionDB < /app/core/db.sql
  ```

> Lần đầu chạy Docker Compose có thể hơi lâu do MySQL khởi tạo dữ liệu. Hãy chờ healthcheck báo `healthy` trước khi gọi API.
