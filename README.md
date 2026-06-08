# ALIMQUICAL® AI EXECUTIVE PLATFORM

Plataforma SaaS con múltiples agentes de inteligencia artificial especializados para la gestión empresarial.

## Arquitectura

```
┌─────────────────────────────────────┐
│          PWA Frontend (Next.js)      │
│  Dashboard │ Reuniones │ CRM │ Docs  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        API Gateway (FastAPI)         │
└──────────────┬──────────────────────┘
               │
    ┌──────────┼─────────────┐
    │          │             │
    ▼          ▼             ▼
 Agentes IA  PostgreSQL   Qdrant
              DB          Vector DB
```

## Stack Tecnológico

### Frontend
- Next.js 16 (App Router)
- TypeScript + Tailwind CSS v4
- shadcn/ui (20+ componentes)
- PWA (Service Worker + Manifest)

### Backend
- Python FastAPI
- PostgreSQL (SQLAlchemy ORM)
- Qdrant (Vector Database)
- Redis + Celery (Tareas asíncronas)

### Agentes IA
- Chief Executive Agent (Coordinador)
- Meeting Secretary (Reuniones)
- Business Analyst (Análisis)
- Document Intelligence (Documentos)
- CRM Agent (Clientes)
- Scheduling Agent (Agenda)
- Memory Agent (Memoria vectorial)
- Legal Assistant (Legal)
- Financial Agent (Financiero)
- Notification Agent (WhatsApp/Email)
- Sales Agent (Ventas)

## Inicio Rápido

### Prerrequisitos
- Node.js 22+
- Python 3.12+
- pnpm
- Docker Desktop

### Windows
```bash
scripts\setup.bat
```

### Manual
```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
pnpm install
pnpm dev
```

## Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

| Variable | Descripción |
|----------|-------------|
| DATABASE_URL | PostgreSQL connection string |
| SECRET_KEY | JWT secret key |
| OPENAI_API_KEY | OpenAI API key |
| ANTHROPIC_API_KEY | Anthropic API key |
| QDRANT_URL | Qdrant vector DB URL |
| WHATSAPP_API_TOKEN | WhatsApp Business API token |

## Despliegue

### Vercel (Frontend)
```bash
cd frontend
vercel --prod
```

### Railway (Backend)
```bash
cd backend
railway up
```
