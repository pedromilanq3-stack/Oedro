FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY bundle.part*.b64 /tmp/
RUN python - <<'PY'
import base64, zipfile
from pathlib import Path
parts = sorted(Path('/tmp').glob('bundle.part*.b64'))
encoded = ''.join(part.read_text() for part in parts)
raw = base64.b64decode(encoded, validate=True)
Path('/tmp/bundle.zip').write_bytes(raw)
with zipfile.ZipFile('/tmp/bundle.zip') as z:
    z.extractall('/app')
PY

RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements-server.txt && \
    python -m pip install --no-deps .

EXPOSE 8080

CMD ["python", "-m", "entity0.server"]
