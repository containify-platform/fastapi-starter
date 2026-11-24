# FastAPI starter

[![Deploy on Containify](https://containify.cloud/deploy-button.svg)](https://containify.cloud/templates/fastapi)

A small [FastAPI](https://fastapi.tiangolo.com/) app with SQLAlchemy, Alembic migrations and
Postgres, served by Uvicorn, ready to deploy on [Containify](https://containify.cloud).

- `GET /`: a hello message and how many notes are stored
- `GET /notes`, `POST /notes` (`{"text": "..."}`): a tiny table in Postgres
- `GET /health`: the health check, with no database call
- `GET /docs`: FastAPI's interactive API docs

Dependencies are managed with [uv](https://docs.astral.sh/uv/) (`pyproject.toml` and `uv.lock`).

## Run it locally

```bash
docker run -d --name pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=app -p 5432:5432 postgres:17
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Then open http://localhost:8000.

## Deploy on Containify

[![Deploy on Containify](https://containify.cloud/deploy-button.svg)](https://containify.cloud/templates/fastapi)

One click deploys it on [Containify](https://containify.cloud). The [template page](https://containify.cloud/templates/fastapi) shows what it creates, and passwords, connection strings and the HTTPS address are filled in for you.

Deploy the **FastAPI starter** template from the Containify catalogue. It adds this app and a
private Postgres database, wires `DATABASE_URL` between them, and runs `alembic upgrade head`
as the pre-deploy command on every deploy.

To build your own app from it, fork this repository and point the app's source at your fork.

### Notes

- `DATABASE_URL` may start with `postgres://` or `postgresql://`; `app/db.py` rewrites it to
  use the psycopg 3 driver.
- Uvicorn listens on `::` port 8000 and trusts the edge's `X-Forwarded-*` headers, since HTTPS
  ends at Containify's edge.
- Add a migration with `uv run alembic revision --autogenerate -m "..."` and commit it.

## License

MIT

---

Made by [Containify](https://containify.cloud): deploy apps, databases and workers from a Git repo or an image, with per-second billing. [Docs](https://containify.cloud/docs) · [Templates](https://containify.cloud/templates)
