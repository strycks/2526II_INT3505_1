# So sánh các API Specification với nhau

| Tiêu chí | OpenAPI (Swagger) | API Blueprint | RAML | TypeSpec |
| :--- | :--- | :--- | :--- | :--- |
| **Triết lý thiết kế** | Tập trung vào sự đầy đủ và khả năng tương thích. | Ưu tiên sự đơn giản và khả năng đọc hiểu nhanh. | Tập trung vào việc tái sử dụng các thành phần API. | Sử dụng tư duy lập trình để sinh ra tài liệu. |
| **Định dạng file** | JSON hoặc YAML | Markdown (APIB) | YAML (RAML) | Cú pháp giống TypeScript (TSP) |
| **Độ phổ biến** | Rất cao | Trung bình | Trung bình (phổ biến trong hệ sinh thái MuleSoft) | Đang tăng trưởng nhanh (Microsoft hậu thuẫn) |
| **Khả năng đọc (Human-readable)** | Trung bình (File YAML dài rất khó theo dõi). | Rất cao (Trông như một file hướng dẫn thông thường). | Cao (Cấu trúc phân tầng rõ ràng). | Cao (Đối với lập trình viên). |
| **Khả năng tái sử dụng** | Thấp (Phải dùng `$ref` khá rườm rà). | Trung bình. | Rất cao (Có cơ chế Traits, Resource Types). | Cực cao (Hỗ trợ kế thừa, Generic, Mixins như code). |
| **Công cụ (Tooling)** | Cực kỳ phong phú (Swagger UI, Postman, Codegen). | Aglio, Apiary, Snowcrash. | API Console, raml2html, Anypoint Platform. | Compiler (tsp), hỗ trợ VS Code mạnh. |
---