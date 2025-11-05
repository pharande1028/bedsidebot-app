@echo off
color 0A
echo.
echo ██████╗ ███████╗██████╗ ███████╗██╗██████╗ ███████╗██████╗  ██████╗ ████████╗
echo ██╔══██╗██╔════╝██╔══██╗██╔════╝██║██╔══██╗██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
echo ██████╔╝█████╗  ██║  ██║███████╗██║██║  ██║█████╗  ██████╔╝██║   ██║   ██║   
echo ██╔══██╗██╔══╝  ██║  ██║╚════██║██║██║  ██║██╔══╝  ██╔══██╗██║   ██║   ██║   
echo ██████╔╝███████╗██████╔╝███████║██║██████╔╝███████╗██████╔╝╚██████╔╝   ██║   
echo ╚═════╝ ╚══════╝╚═════╝ ╚══════╝╚═╝╚═════╝ ╚══════╝╚═════╝  ╚═════╝    ╚═╝   
echo.
echo                           🏥 LOCAL DEVELOPMENT MODE 🏥
echo.

set FLASK_ENV=development
set PORT=8080

echo [INFO] Starting BedsideBot locally...
echo [INFO] URL: http://localhost:8080
echo [INFO] Press Ctrl+C to stop
echo.

python app.py

pause