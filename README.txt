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
├── alembic/            # Migration scripts (Alembic)
├── alembic.ini         # Cấu hình Alembic
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
- `APP_RELOAD`: đặt `true` để Uvicorn auto reload (chỉ dùng môi trường dev).
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
2. Đảm bảo MySQL đang chạy và các biến trong `.env` trỏ đúng tới database (đặt `APP_RELOAD=true` nếu muốn auto reload khi phát triển).
3. Khởi tạo schema và dữ liệu mẫu bằng Alembic:
   ```bash
   alembic upgrade head
   ```
   Lệnh này sẽ tạo các bảng `account`, `CustomerInfor`, `tuition`, `history`, `payment_otp` và seed dữ liệu mẫu.
4. Khởi chạy FastAPI:
   ```bash
   uvicorn api.main:app --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8000} --reload
   ```
5. Truy cập `http://127.0.0.1:8000` để kiểm tra.

## Triển khai với Docker Compose

1. Cập nhật `.env` theo nhu cầu (thông tin database sẽ được dùng để tạo user/DB trong container MySQL).
2. Xây dựng và chạy toàn bộ stack (API + MySQL):
   ```bash
   docker compose up --build
   ```
3. Chạy migration sau khi container MySQL sẵn sàng:
   ```bash
   docker compose exec api alembic upgrade head
   ```
4. API sẽ lắng nghe tại `http://localhost:${APP_PORT}` và MySQL mở cổng 3306 cho máy chủ.
5. Dừng dịch vụ khi không dùng:
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

- Script `core/db.sql` tương ứng với các migration hiện tại (phục vụ khi cần khởi tạo thủ công).
- Nếu muốn refresh dữ liệu bằng script SQL thuần:
  ```bash
  mysql -u sa -p TuitionDB < core/db.sql
  ```

> Lần đầu chạy Docker Compose có thể hơi lâu do MySQL khởi tạo dữ liệu. Hãy chờ healthcheck báo `healthy` trước khi gọi API.

## Form đăng nhập demo

- API chạy tại `http://localhost:${APP_PORT:-8000}` với endpoint `POST /accounts/login`.
- Front-end thuần HTML/CSS nằm trong `frontend/static` với cấu trúc:
  - `pages/`: chứa `login.html`, `home.html`.
  - `styles/`: CSS dùng chung (`base.css`).
  - `scripts/`: logic xử lý form (`login.js`).
- Chạy front-end local:
  ```bash
  uvicorn frontend.app:app --host 0.0.0.0 --port 3000 --reload
  ```
- Hoặc sử dụng Docker Compose (service `frontend`) rồi truy cập `http://localhost:3000`.
- Form gọi API đăng nhập; đăng nhập thành công tự chuyển đến trang `home` (đang để trống để phát triển tiếp), còn lỗi sẽ hiển thị thông báo trên form.
