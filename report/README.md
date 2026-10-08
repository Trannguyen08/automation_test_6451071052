# Báo cáo kiểm thử

Sau mỗi lần chạy `run_tests.bat`, báo cáo Allure HTML được tạo tại:

```text
report/allure-report/        # Website báo cáo Allure
report/allure-report/index.html
```

Thư mục `report/allure-results/` chỉ là dữ liệu trung gian và được tự động xóa
sau khi Allure tạo báo cáo thành công. `report/allure-report/` không nằm trong
`.gitignore`, vì vậy có thể được đưa vào Git khi cần.

Allure CLI được cài cục bộ vào `.tools/` trong lần chạy đầu tiên. Mở báo cáo bằng:

```powershell
.\.tools\allure-2.46.1\bin\allure.bat open report\allure-report
```

