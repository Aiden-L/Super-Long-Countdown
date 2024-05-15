import json
import os
import tkinter as tk
import time
from tkinter import simpledialog

file_path = "clock_config.json"

root = tk.Tk()
root.geometry("300x160")  # 设置客户端大小
# root.resizable(0, 0)  # 设置客户端大小不可变
root.title("Python 倒计时")  # 设置客户端标题
main_frame = tk.Frame(root)
main_frame.pack(anchor='center')


time_info = {}
if os.path.exists(file_path):
    time_info = json.load(open(file_path))
else:
    # 倒计时时间
    input_time = simpledialog.askstring(title='初始化', prompt='请输入倒计时的时间，如 300:00:00')
    time_h, time_m, time_s = input_time.split(":")
    total_seconds = int(time_h) * 3600 + int(time_m) * 60 + int(time_s)
    time_info = {
        "time_left": total_seconds,
        "log": []
    }


# 时间显示Label
time_label = tk.Label(main_frame, font=('calibri', 40, 'bold'), pady=20, foreground='#FF7F00')
begin_hours, begin_remainder = divmod(time_info["time_left"], 3600)
begin_minutes, begin_seconds = divmod(begin_remainder, 60)
time_label.config(text='{:d}:{:02d}:{:02d}'.format(begin_hours, begin_minutes, begin_seconds))
time_label.grid(column=0, row=0, columnspan=2)


def time_counter():
    global counter_timer
    global current_time_left
    current_time_left = time_info["time_left"] - int(time.time() - begin_time)
    hours, remainder = divmod(current_time_left, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_label.config(text='{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds))
    counter_timer = time_label.after(100, time_counter)  # 1000ms后再次调用time()函数，即1s后刷新显示

lock = True
# 按钮控件
def func_begin():
    global lock
    if lock:
        lock = False
        global begin_time
        begin_time = time.time()
        print("开始按钮被点击")
        # 运行时间更新函数
        time_counter()

btn1 = tk.Button(main_frame, text="开始", command=func_begin)

def func_pause():
    global lock
    if not lock:
        lock = True
        print("暂停按钮被点击")
        time_label.after_cancel(counter_timer)
        func_record()

def func_record():
    time_info["log"].append([begin_time, time.time(), current_time_left])
    time_info["time_left"] = current_time_left
    with open(file_path, "w") as f:
        f.write(json.dumps(time_info))
    print("进度已保存")


btn2 = tk.Button(main_frame, text="暂停", command=func_pause)

btn1.grid(column=0, row=1)
btn2.grid(column=1, row=1)

def on_closing():
    try:
        func_record()
    except Exception:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()



