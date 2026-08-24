from __future__ import annotations

import base64
import io
import os
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

BASE = 'https://raw.githubusercontent.com/pedromilanq3-stack/Oedro/entity-zero-server/entity-zero'
RUNTIME = Path('/tmp/entity-zero-runtime')
RUNTIME.mkdir(parents=True, exist_ok=True)

parts = []
for i in range(1, 6):
    url = f'{BASE}/bundle.part{i}.b64'
    with urllib.request.urlopen(url, timeout=60) as r:
        parts.append(r.read().decode('ascii'))

bundle = base64.b64decode(''.join(parts))
with zipfile.ZipFile(io.BytesIO(bundle)) as z:
    z.extractall(RUNTIME)

subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(RUNTIME / 'requirements-server.txt')], check=True)
subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-deps', str(RUNTIME)], check=True)

os.chdir(RUNTIME)
os.execv(sys.executable, [sys.executable, '-m', 'entity0.server'])
