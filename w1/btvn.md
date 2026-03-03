## [GiHub REST API](https://docs.github.com/en/rest/quickstart?apiVersion=2022-11-28)
- Endpoint cơ bản: https://api.github.com/users/{username}
- Dữ liệu trả về: JSON chứa thông tin cá nhân, số lượng follower, và link đến các tài nguyên khác.
- Xác thực: Truy vấn công khai hoặc dùng Personal Access Token
- API này được theo chuẩn.RESTful, sử dụng các phương thức HTTP để thao tác với dữ liệu.

## [OpenWeatherMap API](https://openweathermap.org/api/one-call-3?collection=one_call_api_3.0)
- Endpoint cơ bản: https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}
- Có tham số truy vấn, yêu cầu API Key ngay cả với bản miễn phí.

## [Hypixel Public API](https://api.hypixel.net/)
- Endpoint cơ bản: https://api.hypixel.net/v2/player?uuid={uuid}

- Trả về dữ liệu người chơi. Ngoài ra còn trả về các header như `RateLimit-Remaining` để giúp ứng dụng tự điều chỉnh tốc độ tạo request.
- Yêu cầu gửi API Key qua HTTP Header thay vì URL