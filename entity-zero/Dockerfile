FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY bundle.part1.b64 /tmp/bundle.part1.b64
COPY bundle.part2.b64 /tmp/bundle.part2.b64
COPY bundle.part3.b64 /tmp/bundle.part3.b64
COPY bundle.part4.b64 /tmp/bundle.part4.b64
COPY bundle.part5.b64 /tmp/bundle.part5.b64

RUN python -c "import base64,zipfile; from pathlib import Path; encoded=''.join(Path(f'/tmp/bundle.part{i}.b64').read_text() for i in range(1,6)); Path('/tmp/bundle.zip').write_bytes(base64.b64decode(encoded, validate=True)); zipfile.ZipFile('/tmp/bundle.zip').extractall('/app')"

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements-server.txt
RUN python -m pip install --no-deps .

EXPOSE 8080

CMD ["python", "-m", "entity0.server"]
