import json
from pathlib import Path
out = Path('reports') / 'tiny_out.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('{"alpha": 1, "beta": [1, 2, 3]}', encoding='utf-8')
