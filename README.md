# Mini AI-Native Dev Lab

Laboratório local para aprender, de forma simples, como frontend, backend, API e banco trabalham juntos.

## O que tem neste projeto

- **Frontend** — a página que você vê no navegador (`frontend/`)
- **Backend** — o programa Python que processa os pedidos (`backend/`)
- **API** — os endereços HTTP do backend, como `/projects`
- **Banco** — SQLite com a lista de projetos (`/data/lab.db`)
- **Docker Compose** — sobe frontend e backend juntos
- **AGENTS.md** — regras para o agente de IA no editor

## Como executar

Na pasta do projeto:

```bash
docker compose up --build
```

## Como testar

| O quê | Endereço |
| --- | --- |
| Página (frontend) | http://localhost:8080 |
| Lista de projetos (API) | http://localhost:8000/projects |
| Documentação da API | http://localhost:8000/docs |

Na página, clique em **Carregar projetos**. A lista deve vir da API.

Para parar os serviços: `Ctrl+C` no terminal e, se precisar, `docker compose down`.
