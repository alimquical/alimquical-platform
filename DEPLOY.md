# GUIA COMPLETA DE DEPLOY - ALIMQUICAL AI EXECUTIVE PLATFORM

## 1. PRE-REQUISITOS

- Cuenta en [Vercel](https://vercel.com) (frontend)
- Cuenta en [Railway](https://railway.app) o [Render](https://render.com) (backend)
- PostgreSQL en [Supabase](https://supabase.com) o [Neon](https://neon.tech)
- [GitHub](https://github.com) para el repositorio
- Vercel CLI: `npm i -g vercel`
- Git: [Descargar](https://git-scm.com/download/win)

## 2. GIT - SUBIR REPOSITORIO

```bash
cd C:\Users\PC\Documents\EXTERNOS IA\ALIMQUICAL_AI_EXECUTIVE_PLATFORM

git init
git add .
git commit -m "Initial commit: Alimquical AI Executive Platform"

# Crear repo en GitHub y luego:
git remote add origin https://github.com/TU_USUARIO/alimquical-platform.git
git branch -M main
git push -u origin main
```

## 3. BACKEND - RAILWAY

### 3.1 Crear proyecto en Railway

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# En la carpeta backend
cd backend
railway init
railway link
```

### 3.2 Variables de entorno en Railway

Ir a Railway Dashboard > Tu proyecto > Variables y agregar:

| Variable | Valor |
|----------|-------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/alimquical` |
| `SECRET_KEY` | `genera-una-clave-segura-de-64-caracteres` |
| `ENVIRONMENT` | `production` |
| `OPENAI_API_KEY` | `sk-tu-api-key` |
| `QDRANT_URL` | URL de Qdrant cloud |
| `SENTRY_DSN` | Tu DSN de Sentry |
| `WHATSAPP_API_TOKEN` | Token de WhatsApp Business |
| `ADMIN_EMAIL` | `admin@alimquical.com` |
| `ADMIN_PASSWORD` | `tu-contraseña-super-segura` |
| `CORS_ORIGINS` | `https://appmovilvercel.vercel.app` |

### 3.3 Generar SECRET_KEY segura

```bash
# En terminal:
python -c "import secrets; print(secrets.token_hex(32))"
# Copiar el resultado y usarlo como SECRET_KEY
```

### 3.4 Deploy

```bash
railway up
# Railway detectará automáticamente el Dockerfile
```

### 3.5 Seed Admin (después del deploy)

```bash
railway run "python scripts/seed_admin.py"
```

## 4. BASE DE DATOS - SUPABASE

### 4.1 Crear proyecto en Supabase

1. Ir a [supabase.com](https://supabase.com)
2. Crear nuevo proyecto
3. En Settings > Database > Connection string
4. Copiar connection string (reemplazar `[YOUR-PASSWORD]`)

### 4.2 Configurar PostgreSQL

```sql
-- En Supabase SQL Editor, ejecutar:
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### 4.3 Migraciones automáticas

Al iniciar el backend por primera vez con SQLAlchemy, las tablas se crean automáticamente (`Base.metadata.create_all`).

## 5. FRONTEND - VERCEL

### 5.1 Configurar variables en Vercel CLI

```bash
cd frontend

# Login en Vercel
vercel login

# Configurar variables de entorno (seguras, no hardcodeadas)
vercel env add NEXT_PUBLIC_API_URL
# Pegar: https://tu-backend.railway.app

vercel env add NEXT_PUBLIC_APP_NAME
# Pegar: Alimquical
```

### 5.2 Deploy a producción

```bash
# Deploy inicial
vercel --prod

# El output mostrará la URL: https://appmovilvercel.vercel.app
```

### 5.3 Deploys posteriores

```bash
vercel --prod
```

### 5.4 Verificar PWA en producción

Visitar: `https://appmovilvercel.vercel.app`

Abrir Chrome DevTools > Application > Manifest:
- [OK] Manifest presente
- [OK] Icon 192x192
- [OK] Icon 512x512
- [OK] Display standalone

Chrome Android mostrará "Instalar aplicación".

## 6. SISTEMA DE SUSCRIPCIONES

### Planes disponibles

| Plan | Precio | Reuniones | Usuarios |
|------|--------|-----------|----------|
| **Starter** | $29.99/mes | 50/mes | 1 |
| **Business** | $99.99/mes | 500/mes | 10 |
| **Corporate** | $299.99/mes | Ilimitadas | Ilimitados |

### Integración con Stripe (recomendada)

```bash
# En backend/.env agregar:
STRIPE_SECRET_KEY=sk_live_tu_key
STRIPE_WEBHOOK_SECRET=whsec_tu_webhook
```

El modelo `Subscription` en `backend/models/subscription.py` ya está preparado con campos para Stripe (`stripe_subscription_id`, `stripe_customer_id`).

### Crear usuarios de prueba

```bash
# Admin (tú)
cd backend
python ../scripts/seed_admin.py

# Usuario plan Starter
python ../scripts/create_test_user.py --plan starter

# Usuario plan Business
python ../scripts/create_test_user.py --plan business

# Usuario plan Corporate
python ../scripts/create_test_user.py --plan corporate
```

## 7. CREDENCIALES POR DEFECTO

### Super Admin (TÚ)
| Campo | Valor |
|-------|-------|
| Email | `admin@alimquical.com` |
| Password | `Admin123!` |
| Rol | Super Admin |
| Plan | Corporate (ilimitado) |

### Usuario Starter
| Campo | Valor |
|-------|-------|
| Email | `usuario@starter.com` |
| Password | `Demo123!` |

### Usuario Business
| Campo | Valor |
|-------|-------|
| Email | `usuario@business.com` |
| Password | `Demo123!` |

### Usuario Corporate
| Campo | Valor |
|-------|-------|
| Email | `usuario@corporate.com` |
| Password | `Demo123!` |

> **IMPORTANTE**: Cambiar estas contraseñas en producción.

## 8. VERIFICACION PWA

Una vez desplegado, visitar:
```
https://appmovilvercel.vercel.app
```

### Chrome DevTools > Application > Manifest
```
Name:           Alimquical
Short name:     Alimquical
Display:        standalone
Start URL:      /
Theme color:    #1565C0
Icons:          192x192 [OK], 512x512 [OK]
```

### Chrome Android
1. Abrir Chrome en Android
2. Ir a `https://appmovilvercel.vercel.app`
3. Esperar 30 segundos
4. Aparecerá banner "Instalar aplicación" o menú > "Instalar app"

## 9. DOMINIO PERSONALIZADO (OPCIONAL)

### Vercel
```bash
vercel domains add alimquical.com
# Configurar DNS apuntando a Vercel
```

### Railway
```bash
railway domain --domain api.alimquical.com
```

## 10. MONITOREO

### Sentry (errores)
```bash
# Ya configurado en backend/core/config.py
# Solo agregar SENTRY_DSN en variables de entorno
```

### Vercel Analytics
```bash
# Desde dashboard de Vercel, habilitar Analytics
```

## 11. CI/CD AUTOMATICO

Cada `git push` a main disparará deploy automático en:
- Vercel (frontend)
- Railway (backend)

## 12. ARQUITECTURA FINAL

```
Frontend: https://appmovilvercel.vercel.app  (Vercel)
Backend:  https://tu-app.railway.app          (Railway)
DB:       postgresql://...@supabase.co:5432  (Supabase)
Vector:   https://tu-cluster.cloud.qdrant.io (Qdrant Cloud)
Redis:    redis://...@redis.cloud             (Upstash Redis)
```
