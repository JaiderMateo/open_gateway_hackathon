# open_gateway_hackathon

Monorepo con backend FastAPI y frontend React para integrar capacidades de Nokia Network as Code (NaC).

Referencia NaC: https://networkascode.nokia.io/docs/getting-started

## Estructura

- `backend/`: API FastAPI versionada en `/api/v1`
- `frontend/`: App React + Vite + TypeScript

## Backend

### Requisitos

- Python 3.11+

### Setup

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Configura `NAC_TOKEN` en `.env`.

### Ejecutar backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints

- `GET /api/v1/health`
- `POST /api/v1/nac/device-swap/date`
- `POST /api/v1/nac/device-swap/check`
- `POST /api/v1/nac/sim-swap/date` (placeholder 501)
- `POST /api/v1/nac/sim-swap/check` (placeholder 501)
- `POST /api/v1/nac/kyc/fill-in`
- `POST /api/v1/nac/kyc/match` (placeholder 501)
- `POST /api/v1/nac/kyc/tenure` (placeholder 501)
- `POST /api/v1/nac/location/verify` (placeholder 501)

## Frontend

### Requisitos

- Node.js 20+

### Setup y ejecución

```bash
cd frontend
npm install
npm run dev
```

Si necesitas otro host backend, define `VITE_API_BASE_URL`.

## Notas de NaC

- Cliente SDK centralizado en `backend/app/services/nac/client.py`.
- Patrón SDK:
  - `import network_as_code as nac`
  - `nac.NetworkAsCodeClient(token=...)`
- Device Swap implementado con:
  - `client.devices.get(phone_number=...)`
  - `my_device.get_device_swap_date()`
  - `my_device.verify_device_swap(max_age=...)`
- KYC Fill-in implementado con:
  - `client.kyc.request_customer_info(phone_number=...)`
- SIM Swap y Location quedan listos como placeholders con `501 Not Implemented` hasta confirmar método exacto del SDK para tu producto/scope habilitado.
