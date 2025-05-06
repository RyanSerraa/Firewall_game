# Firewall_game

Para baixar a blibioteca --> pip install pygame

Criar ambiente virtual no windonws: python -m venv .venv

Criar ambiente virtual no linux: python3 -m venv .venv

Ativar no windowns:
Activate no .venv\Scripts\activate

Linux: source .venv/bin/activate
Baixar lib para gerar exe 
pip install pyinstaller
Gerar o exe do Jogo: pyinstaller --onefile --windowed --add-data="mapaMundi.png:." main.py

