# Automation test module đăng nhập UTC

Bộ kiểm thử Selenium WebDriver bằng Python cho trang
`https://vanphongdientu.utc.edu.vn/Login`.

## Công nghệ

- Python 3.11+
- Selenium WebDriver 4
- pytest
- openpyxl để đọc test case từ Excel
- Page Object Model

## Chạy và quan sát trên trình duyệt

Trên Windows, nhấp đúp `run_tests.bat` hoặc chạy:

```powershell
.\run_tests.bat
```

Chrome được mở ở chế độ hiển thị mặc định. Selenium Manager tự tìm/tải driver
phù hợp với Chrome. Có thể tăng thời gian quan sát từng thao tác:

```powershell
$env:ACTION_DELAY = "2"
$env:BROWSER_CLOSE_DELAY = "3"
.\run_tests.bat
```

Chạy một test case cụ thể:

```powershell
.\run_tests.bat -k TC_LOGIN_005
```

Chỉ khi cần chạy ẩn (ví dụ CI):

```powershell
$env:HEADLESS = "1"
.\run_tests.bat
```

## Cấu trúc

```text
test_cases/login_test_cases.xlsx  # Danh sách test case và expected result
src/pages/login_page.py           # Page Object của màn hình đăng nhập
src/utils/excel_reader.py         # Đọc dữ liệu Excel
tests/test_login.py               # Test runner data-driven
tests/conftest.py                 # Khởi tạo Chrome, delay, screenshot khi lỗi
artifacts/screenshots/            # Ảnh chụp tự động khi test thất bại
```

Các ca kiểm thử dùng dữ liệu giả rõ ràng và không thử dò tài khoản thật.
