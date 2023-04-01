

# PIPA

O PIPA é uma plataforma com foco em centralizar o gerenciamento de autorização de diversos serviços de autorização.


### Configuração do Ambiente
É obrigatório ter as seguintes dependências instaladas para o build do projeto:

- Python3
- PostgreSQL
- Node.js


Instalar dependências, em /backend, digitar o comando:
```cli
python3 -m pip install -r requirements.txt
```

Instalar dependências, em /frontend, digitar o comando:
```cli
npm install
```

Criar banco de dados, em /db, digitar o comando:
```cli
python3 init_db.py
```

Executar o programa
```cli
/backend:  python3 server.py
/frontend: npm start
```


### Tecnologias

- Python
- Flask
- React.js
- PostgreSQL


