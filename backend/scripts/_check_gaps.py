import json
from pathlib import Path

manifest = json.loads(Path('static/signs/manifest.json').read_text())
flist = json.loads(Path('static/signs/originals/ivc2tyc_cache/_file_list.json').read_text())
available = set(flist['available'])

gaps = ['M349','M355','M356','M357','M369','M377','M378','M383','P324','P332']
for sid in gaps:
    entry = manifest.get(sid, {})
    src = entry.get('source', 'MISSING')
    n = int(sid[1:]) if sid[1:].isdigit() else -1
    in_ivc = n in available if n > 0 else False
    print(f"{sid}: source={src!r}, ivc2tyc_num={n}, in_dataset={in_ivc}")
