# open_gateway_hackathon

Monorepo con backend FastAPI y frontend React para integrar capacidades de Nokia Network as Code (NaC).

Referencia oficial NaC: https://networkascode.nokia.io/docs/getting-started

## 1) Requisitos previos

Necesitas instalar:

- Git
- Python 3.11+
- Node.js 20+
- npm 10+

Comprobación rápida:

```bash
git --version
python --version
node --version
npm --version
```

## 2) Clonar el repositorio

```bash
git clone <URL_DEL_REPO>
cd open_gateway_hackathon
```

## 3) Configurar y ejecutar el backend (FastAPI)

El backend vive en `backend/`.

### 3.1 Crear entorno virtual

Windows (PowerShell):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS (zsh/bash):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

### 3.2 Instalar dependencias

Windows y macOS:

```bash
pip install -r requirements.txt
```

### 3.3 Configurar variables de entorno

Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

macOS (zsh/bash):

```bash
cp .env.example .env
```

Edita `backend/.env` y configura tu token real:

```env
NAC_TOKEN=tu_token_real
APP_ENV=dev
API_PREFIX=/api/v1
```

### 3.4 Levantar backend

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend corriendo en:

- API base: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/swagger`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI: `http://127.0.0.1:8000/openapi.json`

## 4) Configurar y ejecutar el frontend (React + Vite)

Abre otra terminal (deja el backend corriendo) y ve a `frontend/`.

```bash
cd frontend
npm install
npm run dev
```

Frontend corriendo normalmente en:

- `http://localhost:5173`

### 4.1 (Opcional) Cambiar URL del backend en frontend

Por defecto, el frontend usa:

- `http://localhost:8000/api/v1`

Si necesitas otra URL, define `VITE_API_BASE_URL` antes de arrancar el frontend.

Windows (PowerShell):

```powershell
$env:VITE_API_BASE_URL="http://127.0.0.1:8000/api/v1"
npm run dev
```

macOS (zsh/bash):

```bash
VITE_API_BASE_URL="http://127.0.0.1:8000/api/v1" npm run dev
```

## 5) Flujo recomendado de primera ejecución

1. Clona el repositorio.
2. Configura backend (`venv`, `pip install`, `.env`).
3. Arranca backend y valida `http://127.0.0.1:8000/swagger`.
4. En otra terminal, arranca frontend.
5. Abre `http://localhost:5173` y prueba acciones de `PresenceCheck`.

## 6) Endpoints disponibles

Todos bajo prefijo `/api/v1`:

- `GET /api/v1/health`
- `POST /api/v1/nac/device-swap/date`
- `POST /api/v1/nac/device-swap/check`
- `POST /api/v1/nac/sim-swap/date` (placeholder 501)
- `POST /api/v1/nac/sim-swap/check` (placeholder 501)
- `POST /api/v1/nac/kyc/fill-in`
- `POST /api/v1/nac/kyc/match` (placeholder 501)
- `POST /api/v1/nac/kyc/tenure` (placeholder 501)
- `POST /api/v1/nac/location/verify` (placeholder 501)

## 7) Notas de implementación NaC

- Cliente SDK centralizado en `backend/app/services/nac/client.py`.
- Patrón SDK usado:
  - `import network_as_code as nac`
  - `nac.NetworkAsCodeClient(token=...)`
- Device Swap implementado con:
  - `client.devices.get(phone_number=...)`
  - `my_device.get_device_swap_date()`
  - `my_device.verify_device_swap(max_age=...)`
- KYC Fill-in implementado con:
  - `client.kyc.request_customer_info(phone_number=...)`
- SIM Swap y Location están preparados como placeholders (`501`) hasta confirmar método exacto del SDK en tu scope/producto.

## 8) Troubleshooting rápido

- Error de activación en PowerShell: ejecuta PowerShell como usuario normal y usa `Set-ExecutionPolicy -Scope Process Bypass` si tu política bloquea scripts.
- `python` no encontrado en macOS: usa `python3`.
- Puerto ocupado (`8000` o `5173`): cambia puerto en comandos de `uvicorn` o `vite`.
- Respuestas `502` en endpoints NaC: revisa `NAC_TOKEN` y permisos/scopes de tu cuenta NaC.
