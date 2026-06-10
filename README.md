# LabLeaf Backend

Backend FastAPI para o frontend da LabLeaf.

## API compatível com o frontend

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `POST /api/analyses`
- `GET /api/subscription`

Também expõe as rotas alternativas:
- `POST /auth/cadastro`
- `POST /auth/login`
- `POST /auth/logout`

## Instalação local

1. Copie `.env.example` para `.env`
2. Preencha `SUPABASE_URL`, `SUPABASE_KEY` e `JWT_SECRET`
3. `pip install -r requirements.txt`
4. `uvicorn main:app --reload`

## Deploy no Render

Use `render.yaml` ou crie um novo Web Service:

- Environment: Python 3
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

Defina as variáveis de ambiente no Render:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `JWT_SECRET`
- `PLANTID_API_KEY` (opcional)
