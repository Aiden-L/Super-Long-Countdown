# Super-Long-Countdown
This is a widget that provides a countdown for as long as you want.

这是一个可以提供超长倒计时的小程序，采用Tkinter作为GUI

该小程序具有基本计时器，开始计时，暂停计时，重置计时的功能，不同的是，该计时器可以自定义任何时长，甚至负数（用于正计时，或显示超时时间）

倒计时进度可以保存，下次打开还可以继续计时

#### 打包指南
```shell
pyinstaller -F -w clock.py
```
```shell
pyinstaller -F -w clock.py -i favicon.ico
```

#### 当前功能更新：

- 未暂停直接关闭也可以自动保存计时进度
- 新增自定义计时时间功能
- 新增计时器重置功能，可以在暂停计时的时候重置计时器

#### 当前bug修复&版本进度：

- 修复了按钮可以重复点击导致计时故障的问题
- 修复了重置窗口处于主窗口下方的问题
- 修复超时时间显示不正确的问题
- ###### Version 1.0.0
- 修复了应用内图标不清晰的问题
