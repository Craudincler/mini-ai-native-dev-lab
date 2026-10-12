# Arquitetura do Mini AI-Native Dev Lab

Este laboratório tem duas partes que rodam ao mesmo tempo:

1. a **página** (frontend), na porta 8080
2. o **servidor** (backend + API + banco), na porta 8000

O Docker Compose é quem liga as duas.

## Como os dados caminham

```
Você no navegador
        ↓
Frontend (Nginx + HTML/CSS/JS)     http://localhost:8080
        ↓  clique em "Carregar projetos"
        ↓  fetch GET /projects
Backend (FastAPI)                  http://localhost:8000
        ↓  lê a tabela projects
Banco SQLite                       /data/lab.db
        ↓
JSON volta para a página e a lista aparece
```

A página **não guarda** os projetos. Ela só pede e mostra. Quem guarda é o banco.

## Pastas e responsabilidades

| Pasta ou arquivo | Papel |
| --- | --- |
| `frontend/` | Tela: `index.html`, `style.css` e `app.js` |
| `backend/app/main.py` | API: rotas `/health` e `/projects` |
| `backend/app/database.py` | Cria o banco, insere exemplos e lista projetos |
| `backend/Dockerfile` | Receita da imagem Python do backend |
| `docker-compose.yml` | Sobe frontend e backend juntos |
| `AGENTS.md` | Regras para o agente de IA no editor |

## Por que duas portas?

O navegador abre a página em **8080**. O JavaScript pede dados em **8000**. São programas diferentes: um serve arquivos estáticos (Nginx); o outro executa Python (FastAPI).

O backend permite esse pedido vindo de `http://localhost:8080` (CORS). Sem isso, o navegador bloquearia a chamada.

## Persistência

O volume `lab_data` guarda `/data/lab.db`. Assim, os dados não somem só porque o container do backend reiniciou.

Na primeira subida, se a tabela estiver vazia, o backend grava três projetos de exemplo.
