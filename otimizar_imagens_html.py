# Veja instruções no topo
from pathlib import Path
import re, shutil
from PIL import Image

ROOT=Path(__file__).parent.resolve()
IMG_RE=re.compile(r"<img\b[^>]*>",re.I|re.S)
SRC_RE=re.compile(r"""src\s*=\s*["']([^"']+)["']""",re.I)
WIDTH_RE=re.compile(r"""width\s*=\s*["']""",re.I)
HEIGHT_RE=re.compile(r"""height\s*=\s*["']""",re.I)

def get_size(path):
    if path.suffix.lower()==".svg":
        txt=path.read_text(encoding="utf-8",errors="ignore")
        w=re.search(r'width="([\d.]+)',txt)
        h=re.search(r'height="([\d.]+)',txt)
        if w and h: return int(float(w.group(1))),int(float(h.group(1)))
        return None
    with Image.open(path) as im:
        return im.size

mods=imgs=skip=0
for html in ROOT.rglob("*.html"):
    txt=html.read_text(encoding="utf-8",errors="ignore")
    changed=False
    def rep(m):
        nonlocal_changed=[False]
        global imgs,skip
        tag=m.group(0)
        s=SRC_RE.search(tag)
        if not s: skip+=1; return tag
        src=s.group(1)
        if src.startswith(("http","data:")): skip+=1; return tag
        p=(html.parent/src).resolve()
        if not p.exists(): skip+=1; return tag
        try: size=get_size(p)
        except: skip+=1; return tag
        if not size: skip+=1; return tag
        w,h=size
        nt=tag
        ch=False
        if not WIDTH_RE.search(nt):
            nt=nt[:-1]+f' width="{w}"'
            ch=True
        if not HEIGHT_RE.search(nt):
            nt=nt[:-1]+f' height="{h}">'
            ch=True
        if ch:
            nonlocal_changed[0]=True
        imgs+=1
        return nt
    new=IMG_RE.sub(rep,txt)
    if new!=txt:
        bak=html.with_suffix(".html.bak")
        if not bak.exists():
            shutil.copy2(html,bak)
        html.write_text(new,encoding="utf-8")
        mods+=1
print("Arquivos modificados:",mods)
print("Imagens processadas:",imgs)
print("Imagens ignoradas:",skip)
