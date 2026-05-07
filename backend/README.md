# VisaAtGlance Backend

VisaAtGlance의 FastAPI backend다.

## 실행

루트에서 실행:

```bash
make visa-backend-dev
```

또는 backend 폴더에서 직접 실행:

```bash
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

기본 주소:

```text
http://localhost:8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## 확인

```bash
make visa-backend-check
```

위 명령은 Python compile check와 pytest를 실행한다.
