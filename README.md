# 🌳 Trees Everywhere — Youshop Django Test

Este projeto foi desenvolvido como parte do processo seletivo da Youshop (2025), com o objetivo de gerenciar o plantio de árvores por voluntários ao redor do mundo.

## 📦 Tecnologias

- Python 3.12
- Django 5.2
- SQLite (padrão do Django)


Compatível com versões Python `>=3.11`

## 🚀 Funcionalidades

- Autenticação de usuários
- Associação de usuários a múltiplas contas
- Registro de árvores plantadas (local e tipo)
- Visualização das próprias árvores
- Visualização das árvores dos membros das mesmas contas
- Detalhamento e adição de árvores
- API REST para listar árvores do usuário atual
- Interface administrativa para gerenciar contas, usuários e árvores
- Testes automatizados para garantir funcionamento correto

## 📂 Execução local

1. Clone o projeto:

```bash
git clone https://github.com/seu-usuario/trees-everywhere.git
cd trees-everywhere

2. Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Aplique as migrações do banco de dados:

```bash
python manage.py migrate
```

5. (Opcional) Crie um superusuário para acessar o admin:

```bash
python manage.py createsuperuser
```

6. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

7. Acesse o sistema em [http://localhost:8000](http://localhost:8000)

---

## 🧪 Executando os testes

Para rodar os testes automatizados:

```bash
python manage.py test
```

---

## 📄 Autor

Desenvolvido por Marivaldo Pedro