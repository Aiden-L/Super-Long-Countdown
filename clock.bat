@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
call C:\Users\aiden\anaconda3\Scripts\activate.bat C:\Users\aiden\anaconda3
python clock.py
