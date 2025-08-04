# SJF (Shortest Job First) Scheduler Simulator

Chương trình mô phỏng thuật toán lập lịch SJF (Shortest Job First) với giao diện đồ họa.

## Mô tả

Thuật toán SJF là một thuật toán lập lịch CPU không ưu tiên (non-preemptive) chọn tiến trình có thời gian thực thi (burst time) ngắn nhất để thực hiện trước.

## Tính năng

- ✅ Giao diện đồ họa thân thiện với người dùng
- ✅ Nhập thông tin tiến trình (Process ID, Burst Time, Arrival Time)
- ✅ Hiển thị bảng kết quả chi tiết
- ✅ Tính toán thời gian chờ và thời gian hoàn thành
- ✅ Biểu đồ Gantt trực quan
- ✅ Thống kê tổng quan (thời gian chờ trung bình, thời gian hoàn thành trung bình)

## Yêu cầu hệ thống

- Python 3.6+
- tkinter (thường có sẵn với Python)
- matplotlib
- numpy

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/nviethung04/SJF-Shortest-Job-First.git
cd SJF-Shortest-Job-First
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install matplotlib numpy
```

## Cách sử dụng

1. Chạy chương trình:
```bash
python main.py
```

2. Nhập thông tin tiến trình:
   - **Process ID**: Tên hoặc ID của tiến trình
   - **Burst Time**: Thời gian thực thi của tiến trình
   - **Arrival Time**: Thời gian đến của tiến trình (mặc định là 0)

3. Nhấn "Thêm tiến trình" để thêm tiến trình vào danh sách

4. Nhấn "Thực hiện SJF" để chạy thuật toán và xem kết quả

## Ví dụ

Giả sử có 4 tiến trình:
- P1: Burst Time = 6, Arrival Time = 0
- P2: Burst Time = 8, Arrival Time = 1  
- P3: Burst Time = 7, Arrival Time = 2
- P4: Burst Time = 3, Arrival Time = 3

Thuật toán SJF sẽ sắp xếp và thực hiện theo thứ tự burst time tăng dần.

## Cấu trúc file

- `main.py`: File chính chứa giao diện đồ họa
- `sjf_algorithm.py`: Module xử lý logic thuật toán SJF
- `README.md`: Tài liệu hướng dẫn

## Thuật toán SJF

### Ưu điểm:
- Tối ưu hóa thời gian chờ trung bình
- Hiệu quả với các job có thời gian thực thi ngắn

### Nhược điểm:
- Có thể gây starvation cho các job có thời gian thực thi dài
- Cần biết trước burst time của các tiến trình

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request.

## Giấy phép

MIT License
