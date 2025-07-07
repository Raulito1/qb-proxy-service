poetry install
poetry run uvicorn src.main:app --reload
# qb-proxy-service

A FastAPI microservice proxy for fetching QuickBooks Online Aged Receivable Detail reports.

## Features

- **OAuth2 Login Flow**: Initiate QuickBooks Online OAuth2 via `/login` and `/auth`.
- **Proxy Endpoint**: `/api/qb/reports/aging` returns JSON from the `AgedReceivableDetail` report.
- **In-Memory Token Store**: Demo token storage (replace with Redis or database in production).
- **Automatic Docs**: Interactive Swagger UI at `/docs` and ReDoc at `/redoc`.
- **Development Friendly**: Live reload via Uvicorn’s `--reload`.

## Prerequisites

- Python 3.10 or newer
- [Poetry](https://python-poetry.org/) for dependency management
- QuickBooks Online Developer account with **Client ID**, **Client Secret**, and **Realm ID**

## Getting Started

1. **Clone the repository**

   ```bash
   git clone git@github.com:<your-org>/qb-proxy-service.git
   cd qb-proxy-service
   ```

2. **Install dependencies**

   ```bash
   poetry install
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:

   ```dotenv
   QB_CLIENT_ID=your_client_id
   QB_CLIENT_SECRET=your_client_secret
   QB_REALM_ID=your_realm_id
   QB_REDIRECT_URI=http://localhost:8000/auth
   ```

4. **Run the service**

   ```bash
   poetry run uvicorn src.main:app --reload --port 8000
   ```

## Usage

- **Login & Authenticate**  
  Visit `http://localhost:8000/login` in your browser, complete the QuickBooks consent, and you will be redirected to the docs page with your token stored.

- **Fetch the Aging Report**  
  ```bash
  curl http://localhost:8000/api/qb/reports/aging
  ```

- **Swagger UI**  
  Accessible at: `http://localhost:8000/docs`

- **ReDoc**  
  Accessible at: `http://localhost:8000/redoc`

## Configuration & Deployment

- Use **Poetry** for consistent environments and lockfiles.

## License

This project is licensed under the MIT License.