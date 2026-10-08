"""Мини-библиотека для чистых схем к рефлексивным отчётам (SVG -> PNG).

Использование:
    from draw_schemes import S, INK, MUTED, BLUE, BLUEL, RED, REDL, GRAY
    s = S(1200, 640, "Схема 2. Название", "Подзаголовок: откуда схема")
    s.box(x, y, w, h, "текст\nв две строки", fill=BLUEL, stroke=BLUE)
    s.circ(cx, cy, r, "узел"); s.ar(x1, y1, x2, y2, color=RED); s.t(x, y, "подпись")
    s.save("02_platforma")   # пишет 02_platforma.svg и .png (2x)

Палитра: INK/MUTED для обычного, BLUE для того, что сработало или есть,
RED для разрывов, рисков и того, чего нет. Нужен пакет cairosvg:
    pip install cairosvg --break-system-packages
Набор схем собирается из тех же примитивов: S.box, S.ar, S.circ, S.t.
"""
import cairosvg, html
INK="#2B2B2B"; MUTED="#6B6B6B"; BLUE="#2F5D8A"; BLUEL="#E6EEF6"; RED="#B5473A"; REDL="#F7E7E4"; GRAY="#F2F2F2"
F="DejaVu Sans"
def esc(s): return html.escape(s)
class S:
    def __init__(s,w,h,title,sub=None):
        s.w,s.h=w,h; s.o=[]
        s.o.append(f'<rect width="{w}" height="{h}" fill="white"/>')
        s.o.append('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker><marker id="ab" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>'%(INK,BLUE,RED))
        s.t(30,44,title,22,"bold")
        if sub: s.t(30,72,sub,14,fill=MUTED)
    def t(s,x,y,txt,size=15,weight="normal",fill=INK,anchor="start",italic=False):
        lines=txt.split("\n")
        for i,l in enumerate(lines):
            s.o.append(f'<text x="{x}" y="{y+i*size*1.3}" font-family="{F}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{" font-style=\"italic\"" if italic else ""}>{esc(l)}</text>')
    def box(s,x,y,w,h,txt="",fill="white",stroke=INK,size=15,weight="normal",tfill=INK,rx=8,dash=None,sw=1.6,valign="mid"):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        s.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
        if txt:
            n=len(txt.split("\n")); lh=size*1.3
            ty=y+h/2-(n-1)*lh/2+size*0.35 if valign=="mid" else y+size+10
            s.t(x+w/2,ty,txt,size,weight,tfill,"middle")
    def ar(s,x1,y1,x2,y2,color=INK,dash=None,sw=1.8,both=False,curve=None):
        m={"#2F5D8A":"ab",RED:"ar"}.get(color,"a"); d=f' stroke-dasharray="{dash}"' if dash else ""
        st=f' marker-start="url(#{m})"' if both else ""
        if curve:
            cx,cy=curve; p=f'M{x1},{y1} Q{cx},{cy} {x2},{y2}'
        else: p=f'M{x1},{y1} L{x2},{y2}'
        s.o.append(f'<path d="{p}" fill="none" stroke="{color}" stroke-width="{sw}" marker-end="url(#{m})"{st}{d}/>')
    def line(s,x1,y1,x2,y2,color=INK,sw=1.6,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        s.o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}/>')
    def circ(s,cx,cy,r,txt="",fill="white",stroke=INK,size=15,weight="normal",tfill=INK,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        s.o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"{d}/>')
        if txt:
            n=len(txt.split("\n")); lh=size*1.3
            s.t(cx,cy-(n-1)*lh/2+size*0.35,txt,size,weight,tfill,"middle")
    def poly(s,pts,fill="white",stroke=INK,sw=1.6,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        s.o.append(f'<polygon points="{" ".join(f"{a},{b}" for a,b in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def save(s,name):
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.w}" height="{s.h}" viewBox="0 0 {s.w} {s.h}">'+"".join(s.o)+'</svg>'
        open(name+".svg","w").write(svg)
        cairosvg.svg2png(bytestring=svg.encode(),write_to=name+".png",output_width=s.w*2)

