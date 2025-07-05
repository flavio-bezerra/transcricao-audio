@echo off
REM Obtém o diretório onde o .bat está localizado
cd /d "%~dp0"

REM Executa o Streamlit no diretório atual
streamlit run app.py

pause