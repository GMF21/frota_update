import pygame
import datetime
from frota import Frota
from veiculo import Veiculo, EletricCar

pygame.init()

W, H = 1000, 640
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Sistema de Gestão de Frotas")

FONT = pygame.font.Font(None, 26)
FONT_B = pygame.font.Font(None, 30)
CLOCK = pygame.time.Clock()

BG = (210, 210, 210)
PANEL = (225, 225, 225)
BORDER = (140, 140, 140)
TEXT = (25, 25, 25)
BTN = (200, 200, 200)
BTN_H = (185, 185, 185)
SEL = (150, 200, 150)
SEL_H = (135, 190, 135)

frota = Frota()
try:
    frota.load_inventory()
except:
    pass

ui_logs = []

def ui_log(texto):
    ts = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ui_logs.insert(0, f"[{ts}] {texto}")

class Button:
    def __init__(self, rect, label, action, selectable=False):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.action = action
        self.hover = False
        self.selectable = selectable
        self.selected = False

    def handle(self, e):
        if e.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(e.pos)
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.rect.collidepoint(e.pos):
                self.action()

    def draw(self):
        if self.selectable and self.selected:
            color = SEL_H if self.hover else SEL
        else:
            color = BTN_H if self.hover else BTN
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BORDER, self.rect, 2)
        t = FONT.render(self.label, True, TEXT)
        screen.blit(t, (self.rect.x + 12, self.rect.y + (self.rect.h - t.get_height()) // 2))

class TextInput:
    def __init__(self, rect, placeholder=""):
        self.rect = pygame.Rect(rect)
        self.text = ""
        self.active = False
        self.placeholder = placeholder

    def handle(self, e, numeric=False, letters_only=False):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self.active = self.rect.collidepoint(e.pos)

        if e.type == pygame.KEYDOWN and self.active:
            if e.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return

            ch = e.unicode

            if numeric:
                if ch.isdigit() or ch in ",.":
                    self.text += ch
                return

            if letters_only:
                if ch.isalpha() or ch in " -":
                    self.text += ch
                return

            self.text += ch

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, (70, 130, 180) if self.active else BORDER, self.rect, 2)
        txt = self.text if self.text else self.placeholder
        col = TEXT if self.text else (120, 120, 120)
        t = FONT.render(txt, True, col)
        screen.blit(t, (self.rect.x + 8, self.rect.y + 6))

    def value(self):
        return self.text.strip()

    def clear(self):
        self.text = ""

class TextArea:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.lines = []
        self.scroll = 0

    def set_lines(self, lines):
        self.lines = lines
        self.scroll = 0

    def visible(self):
        return max(1, (self.rect.h - 16) // 24)

    def handle(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 4:
                self.scroll = max(0, self.scroll - 1)
            elif e.button == 5:
                self.scroll = min(max(0, len(self.lines) - self.visible()), self.scroll + 1)

    def draw(self):
        pygame.draw.rect(screen, (245, 245, 245), self.rect)
        pygame.draw.rect(screen, BORDER, self.rect, 2)
        y = self.rect.y + 10
        for i in range(self.scroll, min(len(self.lines), self.scroll + self.visible())):
            t = FONT.render(self.lines[i], True, (10, 10, 10))
            screen.blit(t, (self.rect.x + 10, y))
            y += 24

msg = ""
msg_time = 0

def notify(t):
    global msg, msg_time
    msg = t
    msg_time = pygame.time.get_ticks()

def draw_msg():
    global msg
    if not msg:
        return
    dt = pygame.time.get_ticks() - msg_time
    if dt > 7000:
        msg = ""
        return
    alpha = 255 - int((dt / 7000) * 255)
    s = FONT_B.render(msg, True, (120, 90, 0))
    s.set_alpha(alpha)
    screen.blit(s, (30, H - 45))

panel = pygame.Rect(20, 20, W - 40, 260)

label_marca_add = "Marca:"
label_modelo = "Modelo:"
label_ano = "Ano:"
label_auto = "Autonomia(km):"
label_preco = "Preço(€):"
label_tipo = "Tipo:"
label_search = "Pesquisar Marca:"

left_label_x = 70
gap = 14
max_left_label_w = max(
    FONT.size(label_marca_add)[0],
    FONT.size(label_modelo)[0],
    FONT.size(label_ano)[0],
    FONT.size(label_auto)[0],
    FONT.size(label_tipo)[0],
    FONT.size(label_search)[0]
)
left_input_x = left_label_x + max_left_label_w + gap

row1_y = 70
row2_y = 110
row3_y = 150
row4_y = 190
row5_y = 230

in_marca_add = TextInput((left_input_x, row1_y, 260, 30), "ex: BMW")
in_modelo = TextInput((left_input_x, row2_y, 260, 30), "ex: M3")
in_ano = TextInput((left_input_x, row3_y, 260, 30), "ex: 2020")
in_auto = TextInput((left_input_x, row4_y, 260, 30), "obrigatório se elétrico (km)")
in_search = TextInput((left_input_x, row5_y, 260, 30), "ex: BMW")

preco_label_x = 520
preco_label_w = FONT.size(label_preco)[0]
preco_input_x = preco_label_x + preco_label_w + gap
in_preco = TextInput((preco_input_x, row1_y, 210, 30), "ex: 2000")

area = TextArea((20, 350, W - 40, H - 380))

selected_type = None

def set_type(t):
    global selected_type
    selected_type = t
    btn_comb.selected = (t == "combustao")
    btn_elec.selected = (t == "eletrico")
    if t == "combustao":
        in_auto.clear()

def fmt(v):
    if isinstance(v, EletricCar):
        return f"Tipo: Elétrico | {v.marca} {v.modelo} ({v.ano}) | Preço: {v.preco:.2f}€ | Autonomia: {v.autonomia} km"
    return f"Tipo: Combustão | {v.marca} {v.modelo} ({v.ano}) | Preço: {v.preco:.2f}€"

def refresh_all():
    area.set_lines(ui_logs + [fmt(v) for v in frota.veiculos])

def refresh_search():
    q = in_search.value()
    if not q:
        refresh_all()
        notify("A mostrar todos")
        return
    resultados = frota.filter(q)
    if not resultados:
        area.set_lines(ui_logs)
        notify("Essa marca não está no inventário")
        return
    area.set_lines(ui_logs + [fmt(v) for v in resultados])
    notify(f"Resultados: {q}")

def clear_search():
    in_search.clear()
    refresh_all()
    notify("Pesquisa limpa")

def add():
    m = in_marca_add.value()
    modelo = in_modelo.value()
    ano_txt = in_ano.value()
    p = in_preco.value().replace(",", ".")
    a = in_auto.value()

    if selected_type is None:
        notify("Escolhe o tipo: Combustão ou Elétrico")
        return
    if not m:
        notify("Marca vazia")
        return
    if not modelo:
        notify("Modelo vazio")
        return
    if not ano_txt or not ano_txt.isdigit():
        notify("Ano inválido (só números)")
        return

    ano = int(ano_txt)
    if ano < 1950 or ano > 2100:
        notify("Ano inválido")
        return

    try:
        preco = float(p)
    except:
        notify("Preço inválido")
        return

    if selected_type == "combustao":
        v = Veiculo(m, modelo, ano, preco)
        frota.adicionarVeiculo(v)
        ui_log(f"Carro adicionado (Combustão): {m} {modelo} {ano}")
        notify("Carro (Combustão) adicionado")
    else:
        if not a:
            notify("Autonomia é obrigatória para elétrico")
            return
        if not a.isdigit():
            notify("Autonomia inválida (inteiro)")
            return
        autonomia = int(a)
        v = EletricCar(m, modelo, ano, preco, autonomia)
        frota.adicionarVeiculo(v)
        ui_log(f"Carro adicionado (Elétrico): {m} {modelo} {ano} | Autonomia {autonomia} km")
        notify("Carro (Elétrico) adicionado")

    in_marca_add.clear()
    in_modelo.clear()
    in_ano.clear()
    in_preco.clear()
    in_auto.clear()
    refresh_all()

def exportar():
    frota.export_inventory()
    ui_log("Inventário exportado (CSV)")
    notify("Inventário exportado")

def desconto():
    frota.aplicar_desconto(10)
    ui_log("Desconto aplicado: 10%")
    refresh_all()
    notify("Desconto 10% aplicado")

def draw_label(txt, x, input_box):
    s = FONT.render(txt, True, TEXT)
    y = input_box.rect.centery - s.get_height() // 2
    screen.blit(s, (x, y))

def draw_label_y(txt, x, y_center):
    s = FONT.render(txt, True, TEXT)
    screen.blit(s, (x, y_center - s.get_height() // 2))

btn_add = Button((785, 205, 190, 45), "Adicionar Veículo", add)
btn_desc = Button((20, 290, 220, 40), "Aplicar Desconto", desconto)
btn_search = Button((258, 290, 220, 40), "Pesquisar", refresh_search)
btn_clear = Button((496, 290, 220, 40), "Limpar Pesquisa", clear_search)
btn_exp = Button((734, 290, 220, 40), "Exportar Inventário", exportar)

type_btn_w = 145
type_btn_h = 32
btn_comb = Button((preco_input_x, row2_y, type_btn_w, type_btn_h), "Combustão", lambda: set_type("combustao"), selectable=True)
btn_elec = Button((preco_input_x + type_btn_w + 18, row2_y, type_btn_w, type_btn_h), "Elétrico", lambda: set_type("eletrico"), selectable=True)

refresh_all()

running = True
while running:
    screen.fill(BG)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        in_marca_add.handle(e, numeric=False)
        in_modelo.handle(e, numeric=False)
        in_ano.handle(e, numeric=True)

        in_preco.handle(e, numeric=True)
        in_auto.handle(e, numeric=True)
        in_search.handle(e, letters_only=True)

        area.handle(e)

        for b in [btn_add, btn_desc, btn_search, btn_clear, btn_exp, btn_comb, btn_elec]:
            b.handle(e)

    pygame.draw.rect(screen, PANEL, panel)
    pygame.draw.rect(screen, BORDER, panel, 2)

    screen.blit(FONT_B.render("Sistema de Gestão de Frotas", True, TEXT), (35, 28))

    draw_label(label_marca_add, left_label_x, in_marca_add)
    in_marca_add.draw()

    draw_label(label_modelo, left_label_x, in_modelo)
    in_modelo.draw()

    draw_label(label_ano, left_label_x, in_ano)
    in_ano.draw()

    draw_label(label_preco, preco_label_x, in_preco)
    in_preco.draw()

    draw_label_y(label_tipo, preco_label_x, btn_comb.rect.centery)
    btn_comb.draw()
    btn_elec.draw()

    draw_label(label_auto, left_label_x, in_auto)
    in_auto.draw()

    draw_label(label_search, left_label_x, in_search)
    in_search.draw()

    btn_add.draw()

    btn_desc.draw()
    btn_search.draw()
    btn_clear.draw()
    btn_exp.draw()

    area.draw()
    draw_msg()

    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()
