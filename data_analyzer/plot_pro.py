# 这是一个采用自定义色环的尝试
import matplotlib.pyplot as plt
import datetime

# 设置字体为Microsoft YaHei
plt.rcParams['font.family'] = 'Microsoft YaHei'

# 输入数据
data = [
    [1715727600, 1715734800],
    [1715738400, 1715752800],
    [1715760000, 1715785200],
    [1715814000, 1715857200],
    [1715911200, 1715943600],
    [1716022800, 1716030000],
    [1716084000, 1716090000],
    [1716168600, 1716179400],
    [1716183000, 1716193800],
    [1716193800, 1716206400],
    [1716246000, 1716264000],
    [1716271200, 1716282000]
]

# 将时间戳转换为日期和时间
converted_data = [(datetime.datetime.fromtimestamp(start), datetime.datetime.fromtimestamp(end)) for start, end in data]

# 将数据按天分组
grouped_data = {}
for start, end in converted_data:
    day = start.date()
    if day not in grouped_data:
        grouped_data[day] = []
    grouped_data[day].append((start.time(), end.time()))

# matplotlib提供了许多内置的颜色循环，比如tab10、tab20、tab20b等等
colors = plt.cm.tab20b.colors

# 设置绘图
fig, ax = plt.subplots(figsize=(12, 8))

# 绘制每一天的工作时间段
for day_index, (day, times) in enumerate(sorted(grouped_data.items())):
    total_duration = 0  # 用于计算每天的总时长
    for idx, (start_time, end_time) in enumerate(times):
        start_hour = start_time.hour + start_time.minute / 60
        end_hour = end_time.hour + end_time.minute / 60
        duration = end_hour - start_hour
        total_duration += duration
        # 绘制工作时间段
        ax.bar(day_index, duration, bottom=start_hour, width=0.8, color=colors[idx % len(colors)])
        # 标注每段时间的时长
        ax.text(day_index, start_hour + duration / 2, f'{duration:.2f}h', ha='center', va='center', color='white')

    # 标注每天的总时长
    ax.text(day_index, 24, f'总时长: {total_duration:.2f}h', ha='center', va='bottom')

# 设置x轴
ax.set_xticks(range(len(grouped_data)))
ax.set_xticklabels([day.strftime('%Y-%m-%d') for day in sorted(grouped_data.keys())], rotation=45)

# 设置y轴
ax.set_yticks(range(25))
ax.set_yticklabels([f'{h}:00' for h in range(25)])

# 添加标签和标题
ax.set_ylabel('时间')
ax.set_xlabel('日期')
ax.set_title('工作时间分布图', pad=20)

# 显示网格
ax.grid(True, linestyle='--', alpha=0.7)

# 显示图形
plt.tight_layout()
plt.show()
