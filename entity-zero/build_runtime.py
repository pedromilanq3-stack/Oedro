from __future__ import annotations

import base64
import io
import zipfile
from pathlib import Path

root = Path.cwd()
encoded = ''.join((root / f'bundle.part{i}.b64').read_text() for i in range(1, 6))
raw = base64.b64decode(encoded, validate=True)
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    z.extractall(root)
print('ENTITY-0 runtime extracted')
