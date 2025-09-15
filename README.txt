tải các thư viện cần thiết (tự coi đi tải nhiều quá quên r )

chạy project: uvicorn api.main:app --reload
host: http://127.0.0.1:8000 ==> thấy "Fast API success" là được

project/
│
├─ api/                 # Nơi khai báo các API endpoint (Router FastAPI)
│   ├─ account.py       # API đăng nhập, test kết nối
│   └─ tuition.py       # API lấy thông tin học phí
│
├─ core/
│   └─ connDB.py        # Kết nối SQL Server, tạo Session DB
│
├─ models/              # Pydantic model (schema request/response)
│   ├─ account_model.py
│   └─ tuition_model.py
│
├─ repository/          # Tầng truy vấn dữ liệu (SQL, ORM)
│   ├─ account_repository.py
│   └─ tuition_repository.py
│
├─ service/             # Tầng nghiệp vụ (business logic)
│   ├─ account_service.py
│   └─ tuition_service.py
│
└─ main.py              # Điểm khởi chạy ứng dụng FastAPI

Luồng hoạt động

1️⃣ Client (Postman / Frontend) gửi request (vd: /account/login).
2️⃣ api/: Router nhận request → gọi service.
3️⃣ service/: Xử lý nghiệp vụ (kiểm tra dữ liệu, verify mật khẩu, logic tính toán) → gọi repository.
4️⃣ repository/: Thực hiện truy vấn DB (SQLAlchemy) → trả dữ liệu thô.
5️⃣ service/: Chuyển dữ liệu thành Pydantic model.
6️⃣ api/: Trả JSON về cho client.