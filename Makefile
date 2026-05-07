.PHONY: visa-install visa-frontend-install visa-backend-install visa-dev visa-frontend-dev visa-backend-dev visa-check visa-frontend-check visa-backend-check

visa-install: visa-frontend-install visa-backend-install

visa-frontend-install:
	cd frontend && npm install

visa-backend-install:
	cd backend && uv sync

visa-dev:
	$(MAKE) -j2 visa-backend-dev visa-frontend-dev

visa-frontend-dev:
	cd frontend && npm run dev

visa-backend-dev:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

visa-check: visa-frontend-check visa-backend-check

visa-frontend-check:
	cd frontend && npm run lint && npm run build

visa-backend-check:
	cd backend && uv run python -m compileall app && PYTHONPATH=. uv run pytest
