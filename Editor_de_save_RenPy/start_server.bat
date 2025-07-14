@echo off
echo Instalando dependências necessárias...
pip install -r requirements.txt

echo.
echo Iniciando servidor local do Editor de Save RenPy...
echo Abra seu navegador em: http://localhost:5000
echo Pressione Ctrl+C para parar o servidor
echo.

python app.py

pause
