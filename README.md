# Bank notification box

## Giới thiệu
Bank notification box là một ứng dụng Python giúp bạn theo dõi các giao dịch mới nhất từ API của SePay. Ứng dụng này hỗ trợ hiển thị danh sách giao dịch trên một trang web tự host và có thể là một loa thông báo giao dịch khi có giao dịch mới.

## Tính năng
- Tự động kiểm tra giao dịch mới từ API SePay.
- Hiển thị danh sách giao dịch gần nhất trên giao diện web.
- Phát thông báo âm thanh khi có tiền vào.
- Chạy nền liên tục, cập nhật giao dịch mỗi 2 giây.

> [!WARNING]
> Hiện tại Sepay chỉ hỗ trợ gói free với 50 giao dịch/tháng và hỗ trợ các ngân hàng như : VPBank, ACB, VietinBank, MBBank, BIDV, MSB, TPBank, KienLongBank, OCB. Nếu muốn thì bạn có thể nâng gói cao hơn.

## Cách cài đặt
### Yêu cầu
- Python 3.7 trở lên
- pip (trình quản lý gói Python)
- Các thư viện cần thiết được liệt kê trong `requirements.txt` và mpv

### Cài đặt
1. **Clone repository** (hoặc tải mã nguồn về):
   ```bash
   git clone https://github.com/Tphat77923/bank-noti-box.git
   cd bank-noti-box
   ```

2. **Cài đặt các thư viện cần thiết :**


   ```bash
   pip install -r requirements.txt
   ```
   + các thư viện trong requirements.txt chưa có thư viện [mpv](https://mpv.io/installation/) và cần được cài riêng theo [choco](https://www.liquidweb.com/blog/how-to-install-chocolatey-on-windows/) hoặc apt.
   ```bash
   sudo apt install mpv
   ```
   ```bash
   choco install mpvio
   ```
4. **Thêm API Key Sepay**
   - Đăng ký tài khoản sepay tại [đây](https://sepay.vn/) và chọn plan có hỗ trợ ngân hàng của bạn
   - Vào [đây](https://my.sepay.vn/bankaccount) chọn kết nối tài khoản và làm theo hướng dẫn
   - Vào [đây](https://my.sepay.vn/companyapi) chọn Thêm API Access, đặt tên rồi chọn thêm
   - Copy đoạn mã api quay lại mã nguồn đã tải về
   - Thay đổi tên file `.env.example` thành `.env`
   - Mở file `.env`
   - Thay đổi giá trị `your_api_key` thành API Key của bạn

5. **Chạy ứng dụng:**
   ```bash
   python app.py
   ```

6. **Truy cập giao diện web:**
   - Mở trình duyệt và nhập: `http://localhost:3000`

## Cách sử dụng
- Chương trình sẽ tự động theo dõi và cập nhật danh sách giao dịch.
- Khi có giao dịch mới với số tiền vào (`amount_in` > 0), ứng dụng sẽ phát thông báo bằng giọng nói.
- Bạn có thể kiểm tra danh sách giao dịch mới nhất trên giao diện web.

## Đóng góp
Mọi đóng góp đều được hoan nghênh! Hãy gửi pull request hoặc báo cáo lỗi nếu bạn gặp sự cố.

## Giấy phép
Ứng dụng này được phát hành theo giấy phép Apache-2.0 license.
