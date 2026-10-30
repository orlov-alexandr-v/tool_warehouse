@echo off
cls
echo Запуск сервера...
start "" uvicorn main:app --reload

:check_port
timeout /T 2 /NOBREAK >nul
powershell -Command "try { $socket = New-Object Net.Sockets.TcpClient('127.0.0.1', 8000); $socket.Close(); exit 0 } catch { exit 1 }" >nul
if %errorlevel%==0 (
    goto open_browser
) else (
    goto check_port
)

:open_browser
echo Сервер запущен, открываем браузер...
start chrome http://127.0.0.1:8000