# Selenium Automation Test - UTC Login

Kiểm thử module đăng nhập tại `https://vanphongdientu.utc.edu.vn/Login` bằng
Python, Selenium WebDriver, pytest, Excel và Allure Report.

## Yêu cầu

- Windows, Python 3.11+ và Google Chrome
- Kết nối Internet trong lần chạy đầu tiên

## Chạy project

Mở PowerShell tại thư mục project và chạy:

```powershell
.\run_tests.bat
```

Script tự tạo môi trường Python, cài thư viện, mở Chrome để chạy test và tạo
report tại `report/allure-report/index.html`.

Chạy một test case hoặc chạy ẩn:

```powershell
.\run_tests.bat -k TC_LOGIN_005
$env:HEADLESS = "1"; .\run_tests.bat
```

Mở Allure report:

```powershell
.\.tools\allure-2.46.1\bin\allure.bat open report\allure-report
```

TC_LOGIN_007 cần tài khoản hợp lệ:

```powershell
$env:UTC_USERNAME = "tai_khoan_cua_ban"
$env:UTC_PASSWORD = "mat_khau_cua_ban"
.\run_tests.bat -k TC_LOGIN_007
```

Test case nằm trong `test_cases/login_test_cases.xlsx`. Credential thật không
được lưu trong Excel hoặc mã nguồn.
