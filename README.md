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

- black .
- flake8

## Scrum e Kanban

https://www.notion.so/alamodepaula/1eb26ce7c924809dacf7d8f22d8affd7?v=1eb26ce7c9248128a855000cbd1be625

## Draw.io

https://drive.google.com/file/d/1_YbgWN59S5cpgL3xcH2ykbN-KMC8_6ls/view?usp=sharing

## Link para o github keyboard
https://graphite.dev/guides/closing-issues-with-pull-requests-in-github

### Passo a passo para fechar/associar-se a uma isuue:
    1° Verifique o codigo da issue, para isso entre na aba de issue do projeto.
    2° Copie esse codigo pois iremos utilizar ele 
    3° Após feito toda a modificação siga esses passos para subir o seu commit
        * git checkout -b {DEV-numero da branch} -> ese numero da branch é sequiencial então se a ultima foi 005 a sua será 006
        * git add .
        * git commit -m "DEV-005  Texto do que foi feito - fix #código da issue"
        * git push origin DEV-NUMERO DA SUA BRANCH
        * git checkout main 
        

    4° Esse fix basicamente é uma keyord para fechar a issue 

### Para criar uma issue 
    1°ir na aba de issues no github.
    2°clicar em "New issue"
    3°Colocar um título.
    4°(Opcional) resposabilizar alguém pra resolver essa issue
    5°colocar a label corresponde com essa issue.
    6°Clicar em "Create"

