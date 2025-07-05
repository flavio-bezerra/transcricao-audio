# Atualiza pip para garantir que esteja na versão mais recente
Write-Host "Atualizando pip..."
python -m pip install --upgrade pip

# Instala as bibliotecas do requirements.txt
if (Test-Path "requirements.txt") {
    Write-Host "Instalando as dependências do requirements.txt..."
    pip install -r requirements.txt
} else {
    Write-Host "Arquivo requirements.txt não encontrado."
}

# Instala o FFmpeg usando winget
Write-Host "Instalando FFmpeg..."
winget install --id=Gyan.FFmpeg --silent

Write-Host "Tudo pronto! Dependências e FFmpeg foram instalados."