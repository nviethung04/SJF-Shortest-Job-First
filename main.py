"""
Chương trình mô phỏng thuật toán SJF (Shortest Job First)
Giao diện đồ họa sử dụng tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from sjf_algorithm import SJFScheduler
import numpy as np

class SJFSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng thuật toán SJF (Shortest Job First)")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.scheduler = SJFScheduler()
        self.create_widgets()
        
    def create_widgets(self):
        """Tạo giao diện người dùng"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid weight
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="MÔ PHỎNG THUẬT TOÁN SJF", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame nhập liệu
        input_frame = ttk.LabelFrame(main_frame, text="Nhập thông tin tiến trình", padding="10")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Nhập Process ID
        ttk.Label(input_frame, text="Process ID:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.pid_var = tk.StringVar()
        self.pid_entry = ttk.Entry(input_frame, textvariable=self.pid_var, width=10)
        self.pid_entry.grid(row=0, column=1, padx=(0, 10))
        
        # Nhập Burst Time
        ttk.Label(input_frame, text="Burst Time:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.burst_var = tk.StringVar()
        self.burst_entry = ttk.Entry(input_frame, textvariable=self.burst_var, width=10)
        self.burst_entry.grid(row=0, column=3, padx=(0, 10))
        
        # Nhập Arrival Time
        ttk.Label(input_frame, text="Arrival Time:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.arrival_var = tk.StringVar(value="0")
        self.arrival_entry = ttk.Entry(input_frame, textvariable=self.arrival_var, width=10)
        self.arrival_entry.grid(row=0, column=5, padx=(0, 10))
        
        # Nút thêm tiến trình
        add_btn = ttk.Button(input_frame, text="Thêm tiến trình", command=self.add_process)
        add_btn.grid(row=0, column=6, padx=(10, 0))
        
        # Nút xóa tất cả
        clear_btn = ttk.Button(input_frame, text="Xóa tất cả", command=self.clear_all)
        clear_btn.grid(row=0, column=7, padx=(5, 0))
        
        # Nút thực hiện SJF
        schedule_btn = ttk.Button(input_frame, text="Thực hiện SJF", command=self.run_sjf)
        schedule_btn.grid(row=0, column=8, padx=(5, 0))
        
        # Frame hiển thị kết quả
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        result_frame.columnconfigure(0, weight=1)
        result_frame.columnconfigure(1, weight=1)
        result_frame.rowconfigure(1, weight=1)
        
        # Bảng hiển thị tiến trình
        process_frame = ttk.LabelFrame(result_frame, text="Danh sách tiến trình", padding="5")
        process_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Treeview để hiển thị tiến trình
        columns = ("PID", "Burst Time", "Arrival Time", "Waiting Time", "Turnaround Time", "Completion Time")
        self.process_tree = ttk.Treeview(process_frame, columns=columns, show="headings", height=8)
        
        # Cấu hình cột
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=80, anchor=tk.CENTER)
        
        # Scrollbar cho treeview
        tree_scroll = ttk.Scrollbar(process_frame, orient=tk.VERTICAL, command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.process_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        process_frame.columnconfigure(0, weight=1)
        process_frame.rowconfigure(0, weight=1)
        
        # Frame thống kê
        stats_frame = ttk.LabelFrame(result_frame, text="Thống kê", padding="10")
        stats_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.stats_text = tk.Text(stats_frame, height=8, width=30, state=tk.DISABLED)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        stats_scroll = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_scroll.set)
        stats_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.rowconfigure(0, weight=1)
        
        # Frame biểu đồ Gantt
        gantt_frame = ttk.LabelFrame(result_frame, text="Biểu đồ Gantt", padding="5")
        gantt_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        gantt_frame.columnconfigure(0, weight=1)
        gantt_frame.rowconfigure(0, weight=1)
        
        # Matplotlib figure cho Gantt chart
        self.fig, self.ax = plt.subplots(figsize=(12, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, gantt_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def add_process(self):
        """Thêm tiến trình mới"""
        try:
            pid = self.pid_var.get().strip()
            burst_time = int(self.burst_var.get())
            arrival_time = int(self.arrival_var.get())
            
            if not pid:
                messagebox.showerror("Lỗi", "Vui lòng nhập Process ID!")
                return
            
            if burst_time <= 0:
                messagebox.showerror("Lỗi", "Burst Time phải là số dương!")
                return
                
            if arrival_time < 0:
                messagebox.showerror("Lỗi", "Arrival Time không được âm!")
                return
            
            # Kiểm tra trùng PID
            for process in self.scheduler.processes:
                if process.pid == pid:
                    messagebox.showerror("Lỗi", f"Process ID '{pid}' đã tồn tại!")
                    return
            
            self.scheduler.add_process(pid, burst_time, arrival_time)
            self.update_process_display()
            
            # Xóa input
            self.pid_var.set("")
            self.burst_var.set("")
            self.arrival_var.set("0")
            
            messagebox.showinfo("Thành công", f"Đã thêm tiến trình {pid}")
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho Burst Time và Arrival Time!")
    
    def clear_all(self):
        """Xóa tất cả tiến trình"""
        self.scheduler.clear_processes()
        self.update_process_display()
        self.clear_stats()
        self.clear_gantt_chart()
        messagebox.showinfo("Thành công", "Đã xóa tất cả tiến trình!")
    
    def run_sjf(self):
        """Thực hiện thuật toán SJF"""
        if not self.scheduler.processes:
            messagebox.showwarning("Cảnh báo", "Vui lòng thêm ít nhất một tiến trình!")
            return
        
        # Thực hiện lập lịch
        scheduled_processes = self.scheduler.schedule()
        
        # Cập nhật hiển thị
        self.update_process_display()
        self.update_stats()
        self.draw_gantt_chart()
        
        messagebox.showinfo("Thành công", "Đã hoàn thành lập lịch SJF!")
    
    def update_process_display(self):
        """Cập nhật hiển thị danh sách tiến trình"""
        # Xóa dữ liệu cũ
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        # Thêm dữ liệu mới
        for process in self.scheduler.processes:
            values = (
                process.pid,
                process.burst_time,
                process.arrival_time,
                process.waiting_time,
                process.turnaround_time,
                process.completion_time if process.completion_time > 0 else "-"
            )
            self.process_tree.insert("", tk.END, values=values)
    
    def update_stats(self):
        """Cập nhật thống kê"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        stats_info = f"""THỐNG KÊ THUẬT TOÁN SJF
━━━━━━━━━━━━━━━━━━━━━━━━━

Số tiến trình: {len(self.scheduler.processes)}

Tổng thời gian chờ: {self.scheduler.total_waiting_time}

Tổng thời gian hoàn thành: {self.scheduler.total_turnaround_time}

Thời gian chờ trung bình: 
{self.scheduler.avg_waiting_time:.2f}

Thời gian hoàn thành trung bình: 
{self.scheduler.avg_turnaround_time:.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━

Thuật toán SJF chọn tiến trình
có burst time ngắn nhất để 
thực hiện trước.

Ưu điểm:
• Tối ưu hóa thời gian chờ
• Hiệu quả với job ngắn

Nhược điểm:  
• Starvation cho job dài
• Cần biết trước burst time"""
        
        self.stats_text.insert(1.0, stats_info)
        self.stats_text.config(state=tk.DISABLED)
    
    def clear_stats(self):
        """Xóa thống kê"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.config(state=tk.DISABLED)
    
    def draw_gantt_chart(self):
        """Vẽ biểu đồ Gantt"""
        self.ax.clear()
        
        gantt_data = self.scheduler.get_gantt_chart_data()
        
        if not gantt_data:
            self.ax.text(0.5, 0.5, 'Chưa có dữ liệu', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes, fontsize=12)
            self.canvas.draw()
            return
        
        # Tạo màu sắc cho từng tiến trình
        colors = plt.cm.Set3(np.linspace(0, 1, len(gantt_data)))
        
        y_pos = 0
        max_time = max(data['end_time'] for data in gantt_data)
        
        for i, data in enumerate(gantt_data):
            # Vẽ thanh cho tiến trình
            rect = patches.Rectangle(
                (data['start_time'], y_pos), 
                data['duration'], 
                0.8, 
                linewidth=1, 
                edgecolor='black', 
                facecolor=colors[i],
                alpha=0.7
            )
            self.ax.add_patch(rect)
            
            # Thêm label
            self.ax.text(
                data['start_time'] + data['duration']/2, 
                y_pos + 0.4, 
                f"P{data['pid']}", 
                ha='center', 
                va='center', 
                fontweight='bold',
                fontsize=10
            )
            
            # Thêm thời gian bắt đầu và kết thúc
            self.ax.text(data['start_time'], y_pos - 0.15, 
                        f"{data['start_time']}", ha='center', fontsize=8)
            self.ax.text(data['end_time'], y_pos - 0.15, 
                        f"{data['end_time']}", ha='center', fontsize=8)
        
        # Cấu hình trục
        self.ax.set_xlim(0, max_time + 1)
        self.ax.set_ylim(-0.5, 1.5)
        self.ax.set_xlabel('Thời gian', fontsize=12)
        self.ax.set_title('Biểu đồ Gantt - Thuật toán SJF', fontsize=14, fontweight='bold')
        
        # Ẩn trục Y
        self.ax.set_yticks([])
        
        # Thiết lập grid
        self.ax.grid(True, axis='x', alpha=0.3)
        
        # Cập nhật canvas
        self.fig.tight_layout()
        self.canvas.draw()
    
    def clear_gantt_chart(self):
        """Xóa biểu đồ Gantt"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, 'Biểu đồ Gantt sẽ hiển thị sau khi chạy SJF', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=self.ax.transAxes, fontsize=12)
        self.canvas.draw()

def main():
    """Hàm chính"""
    root = tk.Tk()
    app = SJFSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
