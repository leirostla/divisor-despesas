from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).with_name("DER_models.png")
W, H = 3200, 2100


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


TITLE = font(64, True)
SUBTITLE = font(30)
ENTITY = font(31, True)
FIELD = font(23)
FIELD_BOLD = font(23, True)
LABEL = font(22, True)
FOOT = font(22)

BG = "#F8FAFC"
INK = "#142033"
MUTED = "#526071"
BLUE = "#2563EB"
BLUE_DARK = "#173F91"
HEADER = "#DCEAFE"
BOX = "#FFFFFF"
LINE = "#93A4B8"
ACCENT = "#EEF5FF"

entities = {
    "AUTH_USER": (80, 260, 680, 800, [
        ("PK", "id", "integer"), ("", "username", "string"),
        ("", "email", "string"), ("", "is_active", "boolean"),
    ]),
    "GRUPO": (910, 260, 1510, 800, [
        ("PK", "id", "integer"), ("", "nome", "varchar(100)"),
        ("", "descricao", "text, null"), ("", "data_criacao", "datetime"),
    ]),
    "DESPESA": (1740, 180, 2500, 880, [
        ("PK", "id", "integer"), ("FK", "grupo_id", "integer"),
        ("", "descricao", "varchar(255)"), ("", "observacao", "text, null"),
        ("", "valor_total", "decimal(10,2)"), ("", "data_despesa", "date"),
        ("FK", "criador_id", "integer"),
    ]),
    "PARTICIPANTE_GRUPO": (80, 1160, 840, 1800, [
        ("PK", "id", "integer"), ("FK", "grupo_id", "integer"),
        ("FK", "usuario_id", "integer"), ("", "nome", "varchar(100), null"),
        ("", "ativo", "boolean = true"),
    ]),
    "PARTICIPACAO_DESPESA": (1110, 1120, 1950, 1840, [
        ("PK", "id", "integer"), ("FK", "despesa_id", "integer"),
        ("FK", "participante_id", "integer"),
        ("", "valor_devido", "decimal(10,2) = 0.00"),
    ]),
    "PAGAMENTO": (2240, 1110, 3120, 1850, [
        ("PK", "id", "integer"), ("FK?", "valor_despesa_id", "integer, null"),
        ("FK?", "participante_grupo_pagador_id", "integer, null"),
        ("", "valor_pago", "decimal(10,2) = 0.00"),
    ]),
}


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
d.text((80, 55), "DER — Divisor de Despesas", font=TITLE, fill=INK)
d.text((82, 135), "Entidades e relacionamentos declarados em app_divide/models", font=SUBTITLE, fill=MUTED)


def entity(name, data):
    x1, y1, x2, y2, fields = data
    d.rounded_rectangle((x1, y1, x2, y2), radius=22, fill=BOX, outline=LINE, width=3)
    d.rounded_rectangle((x1, y1, x2, y1 + 88), radius=22, fill=HEADER, outline=BLUE_DARK, width=3)
    d.rectangle((x1, y1 + 55, x2, y1 + 88), fill=HEADER)
    d.text((x1 + 28, y1 + 25), name, font=ENTITY, fill=BLUE_DARK)
    row_h = (y2 - y1 - 100) / max(len(fields), 1)
    for i, (key, field, kind) in enumerate(fields):
        y = y1 + 103 + i * row_h
        if i:
            d.line((x1 + 20, y - 8, x2 - 20, y - 8), fill="#E3E9F1", width=2)
        if key:
            d.rounded_rectangle((x1 + 22, y + 6, x1 + 82, y + 42), radius=8, fill=ACCENT)
            d.text((x1 + 31, y + 11), key, font=FIELD_BOLD, fill=BLUE_DARK)
        d.text((x1 + 98, y + 10), field, font=FIELD_BOLD if key else FIELD, fill=INK)
        tw = d.textlength(kind, font=FIELD)
        d.text((x2 - 26 - tw, y + 10), kind, font=FIELD, fill=MUTED)


def relation(points, label, label_xy, optional=False):
    d.line(points, fill=BLUE if not optional else MUTED, width=5, joint="curve")
    x, y = label_xy
    bbox = d.textbbox((x, y), label, font=LABEL)
    d.rounded_rectangle((bbox[0] - 12, bbox[1] - 7, bbox[2] + 12, bbox[3] + 7), radius=8, fill=BG)
    d.text((x, y), label, font=LABEL, fill=BLUE_DARK if not optional else MUTED)


# Relações são desenhadas antes das entidades para que as caixas cubram as extremidades.
relation([(1510, 610), (1740, 610)], "1 possui N", (1518, 565))
relation([(380, 800), (380, 1160)], "1 participa em N", (405, 930))
relation([(1210, 800), (1210, 980), (560, 980), (560, 1160)], "1 possui N", (770, 940))
relation([(840, 1250), (1000, 1250), (1000, 920), (1900, 920), (1900, 880)], "1 cria N", (1180, 875))
relation([(2120, 880), (2120, 1000), (1530, 1000), (1530, 1120)], "1 divide em N", (1650, 960))
relation([(840, 1450), (1110, 1450)], "1 deve em N", (870, 1405))
relation([(2500, 730), (2850, 730), (2850, 1110)], "0..1 recebe N", (2600, 680), optional=True)
relation([(560, 1800), (560, 1885), (2080, 1885), (2080, 1490), (2240, 1490)], "0..1 realiza N", (1300, 1840), optional=True)

for name, data in entities.items():
    entity(name, data)

d.text((82, 1930), "Legenda: PK = chave primária  •  FK = chave estrangeira  •  FK? = chave estrangeira opcional", font=FOOT, fill=MUTED)
d.text((82, 1972), "CASCADE: Grupo, Usuário, Despesa e ParticipanteGrupo  •  SET_NULL: referências de Pagamento", font=FOOT, fill=MUTED)
d.text((82, 2014), "Os campos id são criados implicitamente pelo Django.", font=FOOT, fill=MUTED)

img.save(OUT, format="PNG", optimize=True, dpi=(220, 220))
print(OUT)
