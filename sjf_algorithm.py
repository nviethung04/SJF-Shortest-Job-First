"""
Thuật toán SJF (Shortest Job First) - Non-preemptive
Module xử lý logic thuật toán lập lịch SJF
"""

class Process:
    def __init__(self, pid, burst_time, arrival_time=0):
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0

class SJFScheduler:
    def __init__(self):
        self.processes = []
        self.total_waiting_time = 0
        self.total_turnaround_time = 0
        self.avg_waiting_time = 0
        self.avg_turnaround_time = 0
    
    def add_process(self, pid, burst_time, arrival_time=0):
        """Thêm tiến trình vào danh sách"""
        process = Process(pid, burst_time, arrival_time)
        self.processes.append(process)
    
    def clear_processes(self):
        """Xóa tất cả tiến trình"""
        self.processes.clear()
    
    def schedule(self):
        """Thực hiện thuật toán SJF"""
        if not self.processes:
            return []
        
        # Sắp xếp theo arrival time trước, sau đó theo burst time
        self.processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
        
        current_time = 0
        completed_processes = []
        remaining_processes = self.processes.copy()
        
        while remaining_processes:
            # Tìm các tiến trình đã đến
            available_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
            
            if not available_processes:
                # Nếu không có tiến trình nào, chuyển đến thời điểm tiến trình tiếp theo đến
                current_time = min(remaining_processes, key=lambda x: x.arrival_time).arrival_time
                continue
            
            # Chọn tiến trình có burst time ngắn nhất
            selected_process = min(available_processes, key=lambda x: x.burst_time)
            
            # Tính toán thời gian
            selected_process.waiting_time = current_time - selected_process.arrival_time
            selected_process.completion_time = current_time + selected_process.burst_time
            selected_process.turnaround_time = selected_process.completion_time - selected_process.arrival_time
            
            current_time = selected_process.completion_time
            
            # Thêm vào danh sách hoàn thành và xóa khỏi danh sách chờ
            completed_processes.append(selected_process)
            remaining_processes.remove(selected_process)
        
        # Tính toán thống kê
        self.calculate_statistics()
        
        return completed_processes
    
    def calculate_statistics(self):
        """Tính toán thống kê tổng quát"""
        if not self.processes:
            return
        
        self.total_waiting_time = sum(p.waiting_time for p in self.processes)
        self.total_turnaround_time = sum(p.turnaround_time for p in self.processes)
        
        n = len(self.processes)
        self.avg_waiting_time = self.total_waiting_time / n
        self.avg_turnaround_time = self.total_turnaround_time / n
    
    def get_gantt_chart_data(self):
        """Tạo dữ liệu cho biểu đồ Gantt"""
        scheduled_processes = self.schedule()
        gantt_data = []
        
        for process in scheduled_processes:
            start_time = process.completion_time - process.burst_time
            gantt_data.append({
                'pid': process.pid,
                'start_time': start_time,
                'end_time': process.completion_time,
                'duration': process.burst_time
            })
        
        return gantt_data
