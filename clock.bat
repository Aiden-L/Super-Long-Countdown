@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
call %HOMEPATH%\anaconda3\Scripts\activate.bat %HOMEPATH%\anaconda3
python clock.py
