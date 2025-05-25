# Firewall_game

## Configuração

- Criar ambiente virtual no windonws: python -m venv .venv
- Criar ambiente virtual no linux: python3 -m venv .venv

- Ativar no windowns: .venv\Scripts\activate
- Ativar no Linux: .venv/bin/activate

- baixar as dependências: pip install -r requirements.txt
- Gerar o exe do Jogo: pyinstaller --onefile --windowed --add-data="mapaMundi.png:." main.py
- Se baixar alguma lib que não esteja no requirements.txt, rode "pip freeze > requirements.txt" para atualizar o requirements.txt

## Comandos antes do commit

black .
flake8

## Scrum e Kanban

https://www.notion.so/alamodepaula/1eb26ce7c924809dacf7d8f22d8affd7?v=1eb26ce7c9248128a855000cbd1be625

## Draw.io

https://drive.google.com/file/d/1_YbgWN59S5cpgL3xcH2ykbN-KMC8_6ls/view?usp=sharing
