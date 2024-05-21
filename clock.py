import base64
import json
import os
import pathlib
import tkinter as tk
import time

from icon import img
from tkinter import simpledialog
from tkinter.messagebox import showerror

file_path = os.path.join(pathlib.Path.home(), 'AppData\Local\clock_config.json')

default_ui_configs = {
    'bg_color': '#ffffff',
    'btn_color': '#ffffff',
    'font_color': '#000000',
    'top_most': True,
    'alpha': 0.8
}

config_info = {}
if os.path.exists(file_path):
    config_info = json.load(open(file_path))
    if not ('bg_color' in config_info['ui_configs']
            and 'btn_color' in config_info['ui_configs']
            and 'font_color' in config_info['ui_configs']
            and 'top_most' in config_info['ui_configs']
            and 'alpha' in config_info['ui_configs']):

        config_info['ui_configs'] = default_ui_configs
else:
    time_h, time_m, time_s = 600, 0, 0
    total_seconds = int(time_h) * 3600 + int(time_m) * 60 + int(time_s)
    config_info = {
        'ui_configs': default_ui_configs,
        "time_left": total_seconds,
        "log": []
    }

root = tk.Tk()

# 设置图标
with open("jMWFRdx2iLDfvc0crBee_tmp.ico", "wb+") as tmp:
    tmp.write(base64.b64decode(img))
root.iconbitmap("jMWFRdx2iLDfvc0crBee_tmp.ico")
os.remove("jMWFRdx2iLDfvc0crBee_tmp.ico")

root.geometry("300x170")  # 设置客户端大小
root.resizable(False, False)  # 设置客户端大小不可变
root.title("Super Long Countdown")  # 设置客户端标题
root.configure(bg=config_info['ui_configs']['bg_color'])

# 设置标题栏颜色
root.wm_attributes("-topmost", config_info['ui_configs']['top_most'])  # 窗口置顶
# root.wm_attributes("-transparentcolor", bg_color)  # 透明的颜色
root.wm_attributes("-alpha", config_info['ui_configs']['alpha'])  # 透明度

# 居中的布局用的主框架
main_frame = tk.Frame(root, bg=config_info['ui_configs']['bg_color'])
main_frame.pack(anchor='center')


# 更新时间显示
def update_label(label_time_left):
    if label_time_left < 0:
        label_time_left = -label_time_left
        begin_hours, begin_remainder = divmod(label_time_left, 3600)
        begin_minutes, begin_seconds = divmod(begin_remainder, 60)
        time_label.config(text='-{:d}:{:02d}:{:02d}'.format(begin_hours, begin_minutes, begin_seconds))
    else:
        begin_hours, begin_remainder = divmod(label_time_left, 3600)
        begin_minutes, begin_seconds = divmod(begin_remainder, 60)
        time_label.config(text='{:d}:{:02d}:{:02d}'.format(begin_hours, begin_minutes, begin_seconds))


# 时间显示Label
time_label = tk.Label(main_frame, font=('calibri', 40, 'bold'), pady=20, fg=config_info['ui_configs']['font_color'], bg=config_info['ui_configs']['bg_color'])
update_label(config_info["time_left"])
time_label.grid(column=0, row=0, columnspan=3)


# 时间更新主逻辑
def time_counter():
    global counter_timer
    global current_time_left
    current_time_left = config_info["time_left"] - int(time.time() - begin_time)
    update_label(current_time_left)
    counter_timer = time_label.after(100, time_counter)  # 1000ms后再次调用time()函数，即1s后刷新显示


lock = True


# 开始按钮的功能
def func_begin():
    global lock
    if lock:
        lock = False
        global begin_time
        begin_time = time.time()
        print("开始按钮被点击")
        # 运行时间更新函数
        time_counter()


# 暂停按钮的功能
def func_pause():
    global lock
    if not lock:
        lock = True
        print("暂停按钮被点击")
        time_label.after_cancel(counter_timer)
        func_record()


# 重置按钮的功能
def func_restart():
    global lock
    if lock:
        print("重置按钮被点击")
        while (True):
            input_time = simpledialog.askstring(title='重置计时', prompt='请输入倒计时的时间，如 300:00:00')
            if not input_time:
                break
            try:
                time_h, time_m, time_s = input_time.split(":")
                if 60 > int(time_m) >= 0 and 60 > int(time_s) >= 0:
                    config_info["time_left"] = int(time_h) * 3600 + int(time_m) * 60 + int(time_s)
                    update_label(config_info["time_left"])
                    break
                else:
                    showerror('错误', '输入值不符合规则，请重新输入')
            except Exception:
                showerror('错误', '输入值不符合规则，请重新输入')


# 写记录
def func_record():
    config_info["log"].append([begin_time, time.time(), current_time_left])
    config_info["time_left"] = current_time_left
    with open(file_path, "w") as f:
        f.write(json.dumps(config_info))
    print("进度已保存")

font_color = config_info['ui_configs']['font_color']
btn_color = config_info['ui_configs']['btn_color']

btn1 = tk.Button(main_frame, text="开始", padx=8, pady=5, command=func_begin, fg=font_color, bg=btn_color)
btn2 = tk.Button(main_frame, text="暂停", padx=8, pady=5, command=func_pause, fg=font_color, bg=btn_color)
btn3 = tk.Button(main_frame, text="重置", padx=8, pady=5, command=func_restart, fg=font_color, bg=btn_color)

btn1.grid(column=0, row=1)
btn2.grid(column=1, row=1)
btn3.grid(column=2, row=1)


def on_closing():
    try:
        func_record()
    except Exception:
        pass
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
