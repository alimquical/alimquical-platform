@echo off
echo ========================================
echo  Alimquical AI Executive Platform Setup
echo ========================================
echo.

echo [1/5] Verificando requisitos...
where node >nul 2>nul || (echo ERROR: Node.js no instalado && exit /b 1)
where python >nul 2>nul || (echo ERROR: Python no instalado && exit /b 1)
where pnpm >nul 2>nul || (echo Instalando pnpm... && npm install -g pnpm)

echo [2/5] Configurando backend...
cd backend
if not exist ".env" copy ..\.env.example .env
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
cd ..

echo [3/5] Configurando frontend...
cd frontend
pnpm install
cd ..

echo [4/5] Generando iconos PWA...
python scripts/generate_icons.py

echo [5/5] Iniciando servicios...
docker-compose up -d postgres qdrant redis

echo.
echo ========================================
echo  Setup completado!
echo.
echo  Para iniciar el backend:
echo    cd backend ^&^& .venv\Scripts\activate ^&^& uvicorn main:app --reload
echo.
echo  Para iniciar el frontend:
echo    cd frontend ^&^& pnpm dev
echo.
echo  Dashboard: http://localhost:3000
echo  API Docs: http://localhost:8000/docs
echo ========================================
pause
