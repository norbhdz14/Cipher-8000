"""
Contador de LP Yu-Gi-Oh! - Cipher
Autor: Ing. Norberto Hernández
Cédula profesional: 15061201
Cipher · Sistemas computacionales IoT
Arandas, Jalisco
"""
import csv
import io
import os
import random
import traceback
from datetime import datetime
from functools import wraps

from kivy.app import App
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.graphics.texture import Texture
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import escape_markup
from kivy.utils import get_color_from_hex as hx

# ---------- Paletas ----------
PALETAS = {
    "oscuro": {
        "AZUL": hx("#3F5FD0"),
        "CIAN": hx("#3CC8E8"),
        "MORADO": hx("#A33FE0"),
        "GRIS": hx("#A0A0A0"),
        "ROJO": hx("#E53935"),
        "VERDE": hx("#43A047"),
        "GRIS_CLARO": hx("#2B2B2B"),
        "FONDO_TARJ": hx("#1E1E1E"),
        "VENTANA": (0.1, 0.1, 0.1, 1),
        "TEXTO": (0.9, 0.9, 0.9, 1),
    },
    "claro": {
        "AZUL": hx("#3F5FD0"),
        "CIAN": hx("#1E9DB8"),
        "MORADO": hx("#A33FE0"),
        "GRIS": hx("#555555"),
        "ROJO": hx("#E53935"),
        "VERDE": hx("#43A047"),
        "GRIS_CLARO": hx("#DDDDDD"),
        "FONDO_TARJ": hx("#F4F6FC"),
        "VENTANA": (1, 1, 1, 1),
        "TEXTO": (0.2, 0.2, 0.2, 1),
    },
}

QUIEN = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(QUIEN, "logo.png")
LOGO2 = os.path.join(QUIEN, "cipher.png")

TELEGRAM = "https://t.me/CipherlosAltos"
BLOG = "https://norbhdz.blogspot.com"
GITHUB = "https://github.com/Norbhdz14"
PAYPAL = "https://paypal.me/norbhdz14"
KOFI = "https://ko-fi.com/cipherlosaltos"

LP_INICIAL = 8000
MAX_NOMBRE = 20

# ---------- Textos (ES y EN) ----------
TEXTOS = {
    "es": {
        "titulo": "Yu-Gi-Oh! LP Tracker",
        "sub": "Cipher · IoT & Sistemas",
        "j1": "Jugador 1",
        "j2": "Jugador 2",
        "victorias": "Victorias",
        "mas_win": "+Victoria",
        "turno": "Turno",
        "dado": "🎲 Dado",
        "moneda": "🪙 Moneda",
        "datos": "📊 Datos",
        "contacto": "Contacto y Apoyo",
        "reiniciar": "🔄 Siguiente Duelo",
        "cara": "¡CARA!",
        "cruz": "¡CRUZ!",
        "tema_claro": "Claro",
        "tema_oscuro": "Oscuro",
        "kb_titulo": "Modificar LP - {nombre}",
        "restar": "- Restar",
        "sumar": "+ Sumar",
        "hist_titulo": "Historial y Ciencia del Duelo",
        "tab_resumen": "Resumen",
        "tab_historial": "Historial",
        "tab_reporte": "Reporte",
        "res_total": "Movimientos totales: {n}",
        "res_turno": "Turno actual: {n}",
        "graf_lp_titulo": "Comparativa de LP Actuales",
        "graf_win_titulo": "Victorias de la Serie (Match)",
        "btn_copiar": "Copiar",
        "btn_txt": "Guardar TXT",
        "btn_csv": "Exportar CSV",
        "copiado": "Reporte copiado al portapapeles.",
        "guardado": "Archivo guardado",
        "err_guardar": "No se pudo guardar el archivo.",
        "err_ui": "Ocurrió un error inesperado. Intenta de nuevo.",
        "error": "Error",
        "listo": "Listo",
        "entendido": "Entendido",
        "enlace_copiado": "Enlace copiado",
        "contacto_titulo": "Acerca de / Contacto",
        "info_servicios": "[b]Cipher[/b]\nIng. Norberto Hernández\nCédula profesional: 15061201\nContador oficial de Yu-Gi-Oh! & Soluciones IoT.\n📍 Arandas, Jalisco",
        "btn_telegram": "Telegram: ",
        "btn_blog": "Visitar Blog",
        "btn_github": "GitHub (Código Fuente)",
        "lbl_apoyo": "Apoya el Desarrollo",
        "txt_apoyo": "Aplicación libre y gratuita para la comunidad de duelos. Considera apoyar el proyecto:",
        "btn_paypal": "💖 Donar vía PayPal",
        "btn_kofi": "☕ Apoyar en Ko-fi",
        "desarrollado": "Desarrollado por Ing. Norberto Hernández",
        "cerrar": "Cerrar",
        "confirmar_reset": "¿Reiniciar LP a 8000 para el siguiente duelo?",
        "si": "Sí",
        "no": "No",
        "nombres_titulo": "Configuración del Duelo",
        "nombres_nota": "Configura los nombres o usa el modo rápido predeterminado.",
        "nombres_ok": "Comenzar con nombres",
        "nombres_saltar": "⚡ Saltar / Usar por defecto",
        "modo_label": "Modalidad:",
        "modo_1": "Duelo Único (A 1 victoria)",
        "modo_3": "Mejor de 3 (A 2 victorias)",
        "fin_match_titulo": "¡Fin del Match!",
        "victoria_titulo": "Victoria de Duelo",
        "msg_campeon": "🏆 ¡{nom} ha ganado el Match ({w} victorias)!",
        "sistema": "Sistema",
        "evento": "Evento",
        "desc_btn": "Botón",
        "desc_half": "÷2 LP",
        "desc_keypad": "Teclado",
        "ev_inicio": "--- Inicio del Duelo ({modo}) ---",
        "ev_nuevo": "--- Siguiente Duelo en la Serie ---",
        "ev_turno": "--- Turno {n} ---",
        "ev_dado": "🎲 Resultado del Dado: {r}",
        "ev_moneda": "🪙 Moneda: {r}",
        "ev_win": "🏆 ¡{nom} gana el duelo! (Victorias: {w})",
        "ev_campeon": "🏆 ¡{nom} gana el Match definitivo con {w} victorias!",
        "ev_nombres": "Jugadores: {a} vs {b} [{modo}]",
        "res_jugador": "{nombre} → LP: {lp} | Victorias: {w}",
        "csv_cols": ["fecha_hora", "jugador", "lp_anterior", "lp_nuevo", "cambio", "descripcion"],
    },
    "en": {
        "titulo": "Yu-Gi-Oh! LP Tracker",
        "sub": "Cipher · IoT & Systems",
        "j1": "Player 1",
        "j2": "Player 2",
        "victorias": "Wins",
        "mas_win": "+Win",
        "turno": "Turn",
        "dado": "🎲 Dice",
        "moneda": "🪙 Coin",
        "datos": "📊 Data",
        "contacto": "Contact & Support",
        "reiniciar": "🔄 Next Duel",
        "cara": "HEADS!",
        "cruz": "TAILS!",
        "tema_claro": "Light",
        "tema_oscuro": "Dark",
        "kb_titulo": "Edit LP - {nombre}",
        "restar": "- Subtract",
        "sumar": "+ Add",
        "hist_titulo": "Duel History & Analytics",
        "tab_resumen": "Summary",
        "tab_historial": "History",
        "tab_reporte": "Report",
        "res_total": "Total logged moves: {n}",
        "res_turno": "Current turn: {n}",
        "graf_lp_titulo": "Current LP Comparison",
        "graf_win_titulo": "Match Wins",
        "btn_copiar": "Copy",
        "btn_txt": "Save TXT",
        "btn_csv": "Export CSV",
        "copiado": "Report copied to clipboard.",
        "guardado": "File saved",
        "err_guardar": "Could not save the file.",
        "err_ui": "An unexpected error occurred. Please try again.",
        "error": "Error",
        "listo": "Done",
        "entendido": "Got it",
        "enlace_copiado": "Link copied",
        "contacto_titulo": "About / Contact",
        "info_servicios": "[b]Cipher[/b]\nEng. Norberto Hernández\nProfessional License: 15061201\nOfficial Yu-Gi-Oh! Counter & IoT Solutions.\n📍 Arandas, Jalisco",
        "btn_telegram": "Telegram: ",
        "btn_blog": "Visit Blog",
        "btn_github": "GitHub (Source Code)",
        "lbl_apoyo": "Support Development",
        "txt_apoyo": "Free and open source app for the duel community. Consider supporting the project:",
        "btn_paypal": "💖 Donate via PayPal",
        "btn_kofi": "☕ Support on Ko-fi",
        "desarrollado": "Developed by Eng. Norberto Hernández",
        "cerrar": "Close",
        "confirmar_reset": "Reset LP to 8000 for the next duel?",
        "si": "Yes",
        "no": "No",
        "nombres_titulo": "Duel Setup",
        "nombres_nota": "Configure names or use fast default mode.",
        "nombres_ok": "Start with names",
        "nombres_saltar": "⚡ Skip / Use default",
        "modo_label": "Mode:",
        "modo_1": "Single Duel (First to 1 win)",
        "modo_3": "Best of 3 (First to 2 wins)",
        "fin_match_titulo": "Match Over!",
        "victoria_titulo": "Duel Victory",
        "msg_campeon": "🏆 {nom} wins the Match ({w} wins)!",
        "sistema": "System",
        "evento": "Event",
        "desc_btn": "Button",
        "desc_half": "÷2 LP",
        "desc_keypad": "Keypad",
        "ev_inicio": "--- Duel Start ({modo}) ---",
        "ev_nuevo": "--- Next Duel in Series ---",
        "ev_turno": "--- Turn {n} ---",
        "ev_dado": "🎲 Dice Result: {r}",
        "ev_moneda": "🪙 Coin: {r}",
        "ev_win": "🏆 {nom} wins the duel! (Wins: {w})",
        "ev_campeon": "🏆 {nom} wins the ultimate Match with {w} wins!",
        "ev_nombres": "Players: {a} vs {b} [{modo}]",
        "res_jugador": "{nombre} → LP: {lp} | Wins: {w}",
        "csv_cols": ["timestamp", "player", "lp_before", "lp_after", "change", "description"],
    },
}


# ---------- Blindaje contra excepciones de UI ----------
def blindado(fn):
    """Evita que una excepción dentro de un callback de UI cierre la app."""
    @wraps(fn)
    def envoltura(*a, **kw):
        try:
            return fn(*a, **kw)
        except Exception:
            traceback.print_exc()
            try:
                app = App.get_running_app()
                if app:
                    app.aviso(app.t("error"), app.t("err_ui"))
            except Exception:
                traceback.print_exc()
            return None
    return envoltura


# ---------- Utilidades gráficas ----------
def degradado(colores, n=64):
    tex = Texture.create(size=(n, 1), colorfmt="rgba")
    buf = bytearray()
    seg = len(colores) - 1
    for i in range(n):
        p = i / (n - 1) * seg
        k = min(int(p), seg - 1)
        f = p - k
        a, b = colores[k], colores[k + 1]
        for c in range(4):
            buf.append(int((a[c] + (b[c] - a[c]) * f) * 255))
    tex.blit_buffer(bytes(buf), colorfmt="rgba", bufferfmt="ubyte")
    return tex


TEX = degradado([hx("#3F5FD0"), hx("#3CC8E8"), hx("#A33FE0")])


def etiqueta(texto, halign="center", **kw):
    """Label que ajusta el texto al ancho y su altura al contenido."""
    kw.setdefault("size_hint_y", None)
    lb = Label(text=texto, halign=halign, **kw)
    lb.bind(width=lambda i, w: setattr(i, "text_size", (w, None)))
    lb.bind(texture_size=lambda i, s: setattr(i, "height", s[1] + dp(6)))
    return lb


class BotonGrad(Button):
    def __init__(self, **kw):
        super().__init__(background_normal="", background_down="",
                         background_color=(0, 0, 0, 0),
                         color=(1, 1, 1, 1), bold=True,
                         halign="center", valign="middle", **kw)
        with self.canvas.before:
            self.c = Color(1, 1, 1, 1)
            self.r = RoundedRectangle(texture=TEX, radius=[dp(10)])
        self.bind(pos=self._u, size=self._u)
        self.bind(size=lambda i, s: setattr(i, "text_size", (s[0] - dp(8), s[1])))

    def _u(self, *a):
        self.r.pos, self.r.size = self.pos, self.size

    def estilo(self, grad=True, color=None, txt=None):
        if grad:
            self.c.rgba = (1, 1, 1, 1)
            self.r.texture = TEX
        else:
            self.c.rgba = color
            self.r.texture = None
        if txt:
            self.color = txt


# ---------- Gráfica de barras ----------
class GraficaBarras(Widget):
    """
    Dibuja barras directamente en su propio canvas.
    - Nunca dibuja si width/height <= 0.
    - El redibujado se agenda con Clock (una sola vez por frame).
    - Cualquier error de dibujo se captura: una gráfica rota no cierra la app.
    """

    def __init__(self, valores, max_val, colores, pal, **kw):
        kw.setdefault("size_hint_y", None)
        kw.setdefault("height", dp(120))
        super().__init__(**kw)
        self.valores = [max(0, int(v)) for v in valores]
        self.max_val = max(1, int(max_val), max(self.valores, default=0))
        self.colores = list(colores) if colores else [hx("#3F5FD0"), hx("#3CC8E8")]
        self.pal = pal
        self._ev = None
        self.bind(pos=self._pedir_dibujo, size=self._pedir_dibujo)
        self._pedir_dibujo()

    def _pedir_dibujo(self, *a):
        if self._ev is None:
            self._ev = Clock.schedule_once(self._dibujar, 0)

    def on_parent(self, inst, parent):
        # Si el widget se destruye (cierra el popup), cancela el redibujado pendiente
        if parent is None and self._ev is not None:
            self._ev.cancel()
            self._ev = None

    def _dibujar(self, *a):
        self._ev = None
        try:
            w, h = self.size
            if w <= 0 or h <= 0:
                return
            izq, abajo, arriba = dp(16), dp(8), dp(14)
            aw, ah = w - 2 * izq, h - abajo - arriba
            n = len(self.valores)
            if n == 0 or aw <= 0 or ah <= 0:
                return

            slot = aw / float(n)
            bw = min(slot * 0.45, dp(50))

            self.canvas.clear()
            with self.canvas:
                Color(*self.pal["FONDO_TARJ"])
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
                for i, v in enumerate(self.valores):
                    cx = self.x + izq + slot * (i + 0.5)
                    alto = max(dp(6), min(1.0, v / float(self.max_val)) * ah)
                    Color(*self.colores[i % len(self.colores)])
                    RoundedRectangle(pos=(cx - bw / 2.0, self.y + abajo),
                                     size=(bw, alto), radius=[dp(4)])
        except Exception:
            traceback.print_exc()


class ContenedorGrafica(BoxLayout):
    """Título + barras + nombres y valores (Labels reales, con markup escapado)."""

    def __init__(self, titulo, etiquetas, valores, max_val, colores, pal, **kw):
        super().__init__(orientation="vertical", size_hint_y=None, height=dp(190),
                         spacing=dp(4), padding=dp(4), **kw)
        self.add_widget(Label(text=titulo, bold=True, font_size=sp(13), color=pal["AZUL"],
                              size_hint_y=None, height=dp(22), halign="center"))
        self.add_widget(GraficaBarras(valores, max_val, colores, pal))

        fila = BoxLayout(size_hint_y=None, height=dp(26), spacing=dp(10))
        for i, etq in enumerate(etiquetas):
            val = valores[i] if i < len(valores) else 0
            fila.add_widget(Label(text=f"[b]{escape_markup(str(etq))}[/b]: {val}", markup=True,
                                  color=pal["TEXTO"], font_size=sp(12), halign="center",
                                  shorten=True))
        self.add_widget(fila)


# ---------- Tarjeta de jugador ----------
class TarjetaJugador(Scatter):
    def __init__(self, num_j, app, **kw):
        super().__init__(do_rotation=False, do_scale=False, do_translation=False,
                         auto_bring_to_front=False, **kw)
        self.size_hint = (1, 1)
        self.num_j = num_j
        self.app = app
        self.lp = LP_INICIAL
        self.wins = 0
        self.rotado = False

        self.caja_interna = BoxLayout(orientation="vertical", padding=dp(8),
                                      spacing=dp(4), size_hint=(None, None))
        self.add_widget(self.caja_interna)
        self.bind(size=self._actualizar_tam)
        self.build_ui()

    def _actualizar_tam(self, *a):
        self.caja_interna.size = self.size
        if self.rotado:
            Clock.schedule_once(self._reaplicar_rotacion, 0)

    def _reaplicar_rotacion(self, *a):
        if self.rotado:
            self.rotation = 0
            self.rotation = 180

    def rotar(self, *a):
        self.rotado = not self.rotado
        self.rotation = 180 if self.rotado else 0

    def texto_nombre(self):
        return f"{self.app.nombre(self.num_j)} ({self.app.t('victorias')}: {self.wins})"

    def refrescar_nombre(self):
        self.lbl_nombre.text = self.texto_nombre()

    def reiniciar_lp(self):
        self.lp = LP_INICIAL
        self.build_ui()

    def build_ui(self):
        self.caja_interna.clear_widgets()
        pal, t = self.app.pal, self.app.t

        top = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(6))
        self.lbl_nombre = Label(text=self.texto_nombre(), bold=True,
                                color=pal["AZUL"], font_size=sp(14),
                                halign="left", valign="middle",
                                shorten=True, shorten_from="right")
        self.lbl_nombre.bind(size=lambda i, s: setattr(i, "text_size", s))
        top.add_widget(self.lbl_nombre)

        btn_win = Button(text=t("mas_win"), size_hint_x=None, width=dp(72),
                         background_normal="", background_color=pal["VERDE"],
                         color=(1, 1, 1, 1), font_size=sp(10), bold=True)
        btn_win.bind(on_release=self.sumar_win)
        top.add_widget(btn_win)

        if self.num_j == 1:
            btn_flip = Button(text="🔄 180°", size_hint_x=None, width=dp(64),
                              background_normal="", background_color=pal["GRIS_CLARO"],
                              color=pal["TEXTO"], font_size=sp(10), bold=True)
            btn_flip.bind(on_release=self.rotar)
            top.add_widget(btn_flip)

        self.caja_interna.add_widget(top)

        self.lbl_lp = Label(text=str(self.lp), bold=True, font_size=sp(42),
                            color=pal["VERDE"] if self.lp > 2000 else pal["ROJO"])
        self.caja_interna.add_widget(self.lbl_lp)

        grid = GridLayout(cols=4, spacing=dp(4), size_hint_y=None, height=dp(70))
        for v in (-1000, -500, -100, 100, 500, 1000, "half", "custom"):
            if v == "half":
                b = Button(text="÷2", background_normal="", background_color=pal["MORADO"],
                           color=(1, 1, 1, 1), bold=True, font_size=sp(12))
                b.bind(on_release=lambda *_: self.modificar_lp(self.lp // 2, set_val=True, desc="half"))
            elif v == "custom":
                b = Button(text="✏️", background_normal="", background_color=pal["AZUL"],
                           color=(1, 1, 1, 1), bold=True, font_size=sp(12))
                b.bind(on_release=self.abrir_teclado)
            else:
                col = pal["ROJO"] if v < 0 else pal["VERDE"]
                b = Button(text=f"{v:+d}", background_normal="", background_color=col,
                           color=(1, 1, 1, 1), bold=True, font_size=sp(11))
                b.bind(on_release=lambda *_, n=v: self.modificar_lp(n, desc="btn"))
            grid.add_widget(b)
        self.caja_interna.add_widget(grid)

    @blindado
    def sumar_win(self, *a):
        app, t = self.app, self.app.t
        self.wins += 1
        self.refrescar_nombre()
        nom_raw = app.nombres[self.num_j]
        nombre = app.nombre(self.num_j)
        app.log("win", jug=self.num_j, nom=nom_raw, w=self.wins)

        meta = 1 if app.match_modo == 1 else 2
        if self.wins >= meta:
            app.log("campeon", jug=self.num_j, nom=nom_raw, w=self.wins)
            app.aviso(t("fin_match_titulo"), t("msg_campeon", nom=nombre, w=self.wins))
            Clock.schedule_once(lambda *_: app.reiniciar_match_completo(), 0.5)
        else:
            app.aviso(t("victoria_titulo"), t("ev_win", nom=nombre, w=self.wins))
            app.reiniciar_duelo_serie()

    @blindado
    def modificar_lp(self, valor, set_val=False, desc="btn"):
        lp_ant = self.lp
        self.lp = max(0, valor) if set_val else max(0, self.lp + valor)

        pal = self.app.pal
        self.lbl_lp.text = str(self.lp)
        self.lbl_lp.color = pal["VERDE"] if self.lp > 2000 else pal["ROJO"]

        self.app.log("lp", jug=self.num_j, nom=self.app.nombres[self.num_j],
                     ant=lp_ant, nuevo=self.lp, cambio=self.lp - lp_ant, desc=desc)

    @blindado
    def abrir_teclado(self, *a):
        app, pal, t = self.app, self.app.pal, self.app.t
        cont = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        txt = TextInput(text="0", multiline=False, readonly=True, font_size=sp(24),
                        halign="center", size_hint_y=None, height=dp(50))
        cont.add_widget(txt)

        def teclear(s):
            if s == "⌫":
                txt.text = txt.text[:-1] or "0"
            elif txt.text == "0":
                txt.text = "0" if s in ("0", "00") else s
            elif len(txt.text) < 7:
                txt.text += s

        grid = GridLayout(cols=3, spacing=dp(4))
        for s in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "00", "⌫"):
            b = Button(text=s, font_size=sp(18))
            b.bind(on_release=lambda _, s=s: teclear(s))
            grid.add_widget(b)
        cont.add_widget(grid)

        acciones = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))
        b_restar = Button(text=t("restar"), background_normal="", background_color=pal["ROJO"],
                          color=(1, 1, 1, 1), bold=True)
        b_sumar = Button(text=t("sumar"), background_normal="", background_color=pal["VERDE"],
                         color=(1, 1, 1, 1), bold=True)
        acciones.add_widget(b_restar)
        acciones.add_widget(b_sumar)
        cont.add_widget(acciones)

        p = Popup(title=t("kb_titulo", nombre=app.nombre(self.num_j)), content=cont,
                  size_hint=(0.85, 0.7), background="",
                  background_color=pal["VENTANA"], title_color=pal["AZUL"])

        def aplicar(es_suma):
            try:
                val = int(txt.text)
            except ValueError:
                val = 0
            p.dismiss()
            if val > 0:
                self.modificar_lp(val if es_suma else -val, desc="keypad")

        b_restar.bind(on_release=lambda *_: aplicar(False))
        b_sumar.bind(on_release=lambda *_: aplicar(True))
        p.open()


# ---------- Centro de datos ----------
class CentroDatos(Popup):
    def __init__(self, app, **kw):
        pal = app.pal
        caja = BoxLayout(orientation="vertical", padding=dp(6), spacing=dp(6))
        tabs = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(4))
        cont = BoxLayout()
        b_cerrar = BotonGrad(text=app.t("cerrar"), size_hint_y=None, height=dp(40))

        for w in (tabs, cont, b_cerrar):
            caja.add_widget(w)

        super().__init__(title=app.t("hist_titulo"), content=caja,
                         size_hint=(0.95, 0.9), background="",
                         background_color=pal["VENTANA"], title_color=pal["AZUL"],
                         separator_color=pal["MORADO"], **kw)
        self.app, self.cont = app, cont
        self.txt_reporte = ""
        self.b_tab = []

        for i, k in enumerate(("tab_resumen", "tab_historial", "tab_reporte")):
            b = BotonGrad(text=app.t(k), font_size=sp(12))
            b.bind(on_release=lambda _, i=i: self.mostrar(i))
            tabs.add_widget(b)
            self.b_tab.append(b)

        b_cerrar.bind(on_release=self.dismiss)
        self.mostrar(0)

    @blindado
    def mostrar(self, i):
        pal = self.app.pal
        for j, b in enumerate(self.b_tab):
            if j == i:
                b.estilo(grad=True, txt=(1, 1, 1, 1))
            else:
                b.estilo(grad=False, color=pal["GRIS_CLARO"], txt=pal["TEXTO"])
        self.cont.clear_widgets()
        self.cont.add_widget((self.pag_resumen, self.pag_historial, self.pag_reporte)[i]())

    def pag_resumen(self):
        app, pal, t = self.app, self.app.pal, self.app.t
        sv = ScrollView()
        caja = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10), size_hint_y=None)
        caja.bind(minimum_height=caja.setter("height"))

        modo_txt = t("modo_1") if app.match_modo == 1 else t("modo_3")
        for texto, col, tam, neg in (
                (f"{t('modo_label')} {modo_txt}", pal["AZUL"], 13, True),
                (t("res_total", n=len(app.historial)), pal["TEXTO"], 13, False),
                (t("res_turno", n=app.turno), pal["MORADO"], 13, True)):
            lb = Label(text=texto, color=col, font_size=sp(tam), bold=neg,
                       size_hint_y=None, height=dp(22))
            caja.add_widget(lb)

        nombres = [app.nombre(1), app.nombre(2)]

        lps = [app.j1.lp, app.j2.lp]
        colores_lp = [pal["VERDE"] if lp > 2000 else pal["ROJO"] for lp in lps]
        caja.add_widget(ContenedorGrafica(t("graf_lp_titulo"), nombres, lps,
                                          LP_INICIAL, colores_lp, pal))

        wins = [app.j1.wins, app.j2.wins]
        meta = 1 if app.match_modo == 1 else 2
        caja.add_widget(ContenedorGrafica(t("graf_win_titulo"), nombres, wins,
                                          meta, [pal["AZUL"], pal["CIAN"]], pal))

        sv.add_widget(caja)
        return sv

    def pag_historial(self):
        app, pal = self.app, self.app.pal
        sv = ScrollView()
        box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(2))
        box.bind(minimum_height=box.setter("height"))
        for h in reversed(app.historial):
            box.add_widget(etiqueta(app.texto_evento(h), halign="left",
                                    color=pal["TEXTO"], font_size=sp(12)))
        sv.add_widget(box)
        return sv

    def pag_reporte(self):
        app, pal, t = self.app, self.app.pal, self.app.t
        self.txt_reporte = "\n".join(app.texto_evento(h) for h in app.historial)
        caja = BoxLayout(orientation="vertical", spacing=dp(6))
        sv = ScrollView()
        sv.add_widget(etiqueta(self.txt_reporte, halign="left", valign="top",
                               color=pal["TEXTO"], font_size=sp(12)))
        caja.add_widget(sv)

        fila = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(6))
        for clave, fn in (("btn_copiar", self.copiar), ("btn_txt", self.guardar_txt),
                          ("btn_csv", self.guardar_csv)):
            b = BotonGrad(text=t(clave))
            b.bind(on_release=fn)
            fila.add_widget(b)
        caja.add_widget(fila)
        return caja

    @blindado
    def copiar(self, *a):
        Clipboard.copy(self.txt_reporte)
        self.app.aviso(self.app.t("listo"), self.app.t("copiado"))

    @blindado
    def guardar_txt(self, *a):
        ruta = self.app.guardar_archivo("reporte_duelo.txt", self.txt_reporte)
        self._avisar_guardado(ruta)

    @blindado
    def guardar_csv(self, *a):
        app, t = self.app, self.app.t
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(t("csv_cols"))
        for h in app.historial:
            d = h["d"]
            if h["tipo"] == "lp":
                w.writerow([h["ts"], app.nombre_en(d["jug"], d["nom"]), d["ant"], d["nuevo"],
                            d["cambio"], t("desc_" + d["desc"])])
            else:
                w.writerow([h["ts"], t("sistema"), "", "", "", app.texto_evento(h, con_hora=False)])
        ruta = app.guardar_archivo("historial_duelo.csv", buf.getvalue(), bom=True)
        self._avisar_guardado(ruta)

    def _avisar_guardado(self, ruta):
        t = self.app.t
        if ruta:
            self.app.aviso(t("guardado"), ruta)
        else:
            self.app.aviso(t("listo"), t("err_guardar"))


# ---------- Aplicación ----------
class YugiohCounterApp(App):
    title = "Yu-Gi-Oh! LP Tracker - Cipher"

    def build(self):
        self.lang = "es"
        self.modo_oscuro = True
        self.pal = PALETAS["oscuro"]
        Window.clearcolor = self.pal["VENTANA"]
        try:
            Window.softinput_mode = "below_target"
        except Exception:
            pass

        self.turno = 1
        self.historial = []
        self.nombres = {1: None, 2: None}  # None = nombre por defecto (traducible)
        self.match_modo = 3                # 1 = duelo único, 3 = mejor de 3
        self._popup_nombres = None
        self._popup_datos = None

        self.raiz = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(6))
        self.j1 = TarjetaJugador(1, self)
        self.j2 = TarjetaJugador(2, self)
        self.armar_ui()

        self.log("inicio", modo=self.match_modo)
        return self.raiz

    def on_start(self):
        Clock.schedule_once(self.pedir_nombres, 0.4)

    # ----- Idioma / nombres -----
    def t(self, clave, **kw):
        txt = TEXTOS[self.lang].get(clave, clave)
        return txt.format(**kw) if kw and isinstance(txt, str) else txt

    def nombre_en(self, idx, nom):
        return nom or self.t(f"j{idx}")

    def nombre(self, idx):
        return self.nombre_en(idx, self.nombres[idx])

    # ----- Interfaz principal -----
    def armar_ui(self):
        pal, t = self.pal, self.t
        self.raiz.clear_widgets()

        cab = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(6))
        if os.path.exists(LOGO):
            cab.add_widget(Image(source=LOGO, size_hint_x=None, width=dp(50)))

        t_box = BoxLayout(orientation="vertical")
        for texto, col, tam, neg in ((t("titulo"), pal["AZUL"], 16, True),
                                     (t("sub"), pal["GRIS"], 10, False)):
            lb = Label(text=texto, color=col, font_size=sp(tam), bold=neg,
                       halign="left", valign="middle")
            lb.bind(size=lambda i, s: setattr(i, "text_size", s))
            t_box.add_widget(lb)
        cab.add_widget(t_box)

        b_tema = BotonGrad(text=t("tema_claro") if self.modo_oscuro else t("tema_oscuro"),
                           size_hint_x=None, width=dp(58), font_size=sp(10))
        b_tema.bind(on_release=self.alternar_tema)
        cab.add_widget(b_tema)

        b_lang = BotonGrad(text="EN" if self.lang == "es" else "ES",
                           size_hint_x=None, width=dp(44), font_size=sp(11))
        b_lang.bind(on_release=self.alternar_idioma)
        cab.add_widget(b_lang)
        self.raiz.add_widget(cab)

        self.raiz.add_widget(self.j1)

        barra = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(4))
        self.lbl_turno = Label(text=f"{t('turno')}: {self.turno}", bold=True,
                               color=pal["MORADO"], size_hint_x=0.8)
        b_sig = Button(text="+1", size_hint_x=None, width=dp(36), background_normal="",
                       background_color=pal["GRIS_CLARO"], color=pal["TEXTO"], bold=True)
        b_sig.bind(on_release=self.siguiente_turno)
        b_dado = BotonGrad(text=t("dado"), font_size=sp(11))
        b_dado.bind(on_release=self.lanzar_dado)
        b_moneda = BotonGrad(text=t("moneda"), font_size=sp(11))
        b_moneda.bind(on_release=self.lanzar_moneda)
        for w in (self.lbl_turno, b_sig, b_dado, b_moneda):
            barra.add_widget(w)
        self.raiz.add_widget(barra)

        self.raiz.add_widget(self.j2)

        fin = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(4))
        b_datos = BotonGrad(text=t("datos"), font_size=sp(12))
        b_datos.bind(on_release=self.abrir_datos)
        b_contacto = BotonGrad(text=t("contacto"), font_size=sp(12))
        b_contacto.bind(on_release=self.abrir_contacto)
        b_reset = Button(text=t("reiniciar"), size_hint_x=1.2, background_normal="",
                         background_color=pal["ROJO"], color=(1, 1, 1, 1), bold=True,
                         font_size=sp(11), halign="center")
        b_reset.bind(on_release=self.confirmar_reset)
        for w in (b_datos, b_contacto, b_reset):
            fin.add_widget(w)
        self.raiz.add_widget(fin)

        self.j1.build_ui()
        self.j2.build_ui()

    @blindado
    def alternar_idioma(self, *a):
        self.lang = "en" if self.lang == "es" else "es"
        self.armar_ui()

    @blindado
    def alternar_tema(self, *a):
        self.modo_oscuro = not self.modo_oscuro
        self.pal = PALETAS["oscuro" if self.modo_oscuro else "claro"]
        Window.clearcolor = self.pal["VENTANA"]
        self.armar_ui()

    # ----- Historial -----
    def log(self, tipo, **datos):
        self.historial.append({"ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               "tipo": tipo, "d": datos})

    def texto_modo(self, modo):
        return self.t("modo_1" if modo == 1 else "modo_3")

    def texto_evento(self, h, con_hora=True):
        """Convierte un evento guardado en texto, en el idioma actual."""
        t, d, tp = self.t, h["d"], h["tipo"]
        if tp == "lp":
            cuerpo = (f"{self.nombre_en(d['jug'], d['nom'])}: {d['ant']} ➔ {d['nuevo']} "
                      f"({d['cambio']:+} LP) [{t('desc_' + d['desc'])}]")
        elif tp == "turno":
            cuerpo = t("ev_turno", n=d["n"])
        elif tp == "dado":
            cuerpo = t("ev_dado", r=d["r"])
        elif tp == "moneda":
            cuerpo = t("ev_moneda", r=t("cara" if d["cara"] else "cruz"))
        elif tp == "win":
            cuerpo = t("ev_win", nom=self.nombre_en(d["jug"], d["nom"]), w=d["w"])
        elif tp == "campeon":
            cuerpo = t("ev_campeon", nom=self.nombre_en(d["jug"], d["nom"]), w=d["w"])
        elif tp == "nombres":
            cuerpo = t("ev_nombres", a=self.nombre_en(1, d["n1"]), b=self.nombre_en(2, d["n2"]),
                       modo=self.texto_modo(d["modo"]))
        elif tp == "inicio":
            cuerpo = t("ev_inicio", modo=self.texto_modo(d.get("modo", 3)))
        else:  # nuevo
            cuerpo = t("ev_" + tp)
        return f"[{h['ts'][11:]}] {cuerpo}" if con_hora else cuerpo

    # ----- Turnos, dado, moneda -----
    @blindado
    def siguiente_turno(self, *a):
        self.turno += 1
        self.lbl_turno.text = f"{self.t('turno')}: {self.turno}"
        self.log("turno", n=self.turno)

    @blindado
    def lanzar_dado(self, *a):
        res = random.randint(1, 6)
        self.log("dado", r=res)
        self.popup_resultado(self.t("dado"), f"🎲 {res}")

    @blindado
    def lanzar_moneda(self, *a):
        cara = random.choice([True, False])
        self.log("moneda", cara=cara)
        self.popup_resultado(self.t("moneda"), f"🪙 {self.t('cara' if cara else 'cruz')}")

    def popup_resultado(self, titulo, texto):
        cont = BoxLayout(orientation="vertical", padding=dp(20))
        cont.add_widget(Label(text=texto, font_size=sp(36), bold=True, color=self.pal["AZUL"]))
        p = Popup(title=titulo, content=cont, size_hint=(0.7, 0.3), background="",
                  background_color=self.pal["VENTANA"], title_color=self.pal["AZUL"])
        Clock.schedule_once(lambda *_: p.dismiss(), 1.5)
        p.open()

    # ----- Configuración del duelo (nombres + modalidad) -----
    @blindado
    def pedir_nombres(self, *a):
        if self._popup_nombres is not None:  # evita abrirlo dos veces
            return
        pal, t = self.pal, self.t
        cont = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(6))
        entradas = {}
        for i in (1, 2):
            lb = Label(text=t(f"j{i}"), color=pal["TEXTO"], size_hint_y=None, height=dp(20),
                       halign="left", valign="middle")
            lb.bind(size=lambda inst, s: setattr(inst, "text_size", s))
            cont.add_widget(lb)
            ti = TextInput(text=self.nombres[i] or "", hint_text=t(f"j{i}"), multiline=False,
                           write_tab=False, font_size=sp(16), size_hint_y=None, height=dp(38))
            entradas[i] = ti
            cont.add_widget(ti)

        lb_modo = Label(text=t("modo_label"), color=pal["TEXTO"], size_hint_y=None, height=dp(20),
                        halign="left", valign="middle")
        lb_modo.bind(size=lambda inst, s: setattr(inst, "text_size", s))
        cont.add_widget(lb_modo)

        opciones = {t("modo_3"): 3, t("modo_1"): 1}
        sp_modo = Spinner(text=self.texto_modo(self.match_modo), values=list(opciones.keys()),
                          size_hint_y=None, height=dp(38), background_normal="",
                          background_color=pal["AZUL"], color=(1, 1, 1, 1))
        cont.add_widget(sp_modo)

        nota = Label(text=t("nombres_nota"), color=pal["GRIS"], font_size=sp(10),
                     halign="center", valign="middle")
        nota.bind(size=lambda inst, s: setattr(inst, "text_size", s))
        cont.add_widget(nota)

        fila_btn = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(6))
        b_ok = BotonGrad(text=t("nombres_ok"))
        b_saltar = Button(text=t("nombres_saltar"), background_normal="",
                          background_color=pal["GRIS_CLARO"], color=pal["TEXTO"],
                          bold=True, font_size=sp(11))
        fila_btn.add_widget(b_ok)
        fila_btn.add_widget(b_saltar)
        cont.add_widget(fila_btn)

        p = Popup(title=t("nombres_titulo"), content=cont, size_hint=(0.9, 0.78),
                  background="", background_color=pal["VENTANA"], title_color=pal["AZUL"],
                  separator_color=pal["MORADO"], auto_dismiss=False)
        self._popup_nombres = p
        p.bind(on_dismiss=lambda *_: setattr(self, "_popup_nombres", None))

        def aplicar(saltar):
            try:
                if saltar:
                    nuevos = {1: None, 2: None}
                else:
                    nuevos = {i: (entradas[i].text.strip()[:MAX_NOMBRE] or None) for i in (1, 2)}
                self.match_modo = opciones.get(sp_modo.text, 3)
                if nuevos != self.nombres:
                    self.j1.wins = 0
                    self.j2.wins = 0
                self.nombres = nuevos
                self.j1.refrescar_nombre()
                self.j2.refrescar_nombre()
                self.log("nombres", n1=nuevos[1], n2=nuevos[2], modo=self.match_modo)
            except Exception:
                traceback.print_exc()
            finally:
                p.dismiss()

        b_ok.bind(on_release=lambda *_: aplicar(False))
        b_saltar.bind(on_release=lambda *_: aplicar(True))
        p.open()

    # ----- Reinicios -----
    def reiniciar_duelo_serie(self):
        self.j1.reiniciar_lp()
        self.j2.reiniciar_lp()
        self.turno = 1
        self.lbl_turno.text = f"{self.t('turno')}: 1"
        self.log("nuevo")

    def reiniciar_match_completo(self):
        self.j1.wins = 0
        self.j2.wins = 0
        self.j1.refrescar_nombre()
        self.j2.refrescar_nombre()
        self.reiniciar_duelo_serie()
        Clock.schedule_once(self.pedir_nombres, 0.25)

    @blindado
    def confirmar_reset(self, *a):
        pal, t = self.pal, self.t
        cont = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        lb = Label(text=t("confirmar_reset"), color=pal["TEXTO"], halign="center", valign="middle")
        lb.bind(size=lambda i, s: setattr(i, "text_size", s))
        cont.add_widget(lb)

        fila = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(6))
        b_si = Button(text=t("si"), background_normal="", background_color=pal["ROJO"],
                      color=(1, 1, 1, 1), bold=True)
        b_no = Button(text=t("no"), background_normal="", background_color=pal["GRIS_CLARO"],
                      color=pal["TEXTO"])
        fila.add_widget(b_si)
        fila.add_widget(b_no)
        cont.add_widget(fila)

        p = Popup(title=t("reiniciar"), content=cont, size_hint=(0.8, 0.3), background="",
                  background_color=pal["VENTANA"], title_color=pal["AZUL"])

        def do_reset(*_):
            p.dismiss()
            self.reiniciar_duelo_serie()

        b_si.bind(on_release=do_reset)
        b_no.bind(on_release=p.dismiss)
        p.open()

    # ----- Datos, archivos y avisos -----
    @blindado
    def abrir_datos(self, *a):
        if self._popup_datos is not None:
            return
        p = CentroDatos(self)
        self._popup_datos = p
        p.bind(on_dismiss=lambda *_: setattr(self, "_popup_datos", None))
        p.open()

    def guardar_archivo(self, nombre, contenido, bom=False):
        """Guarda en Descargas (Android) o, si no se puede, en la carpeta de la app."""
        carpetas = [c for c in ("/storage/emulated/0/Download", "/sdcard/Download") if os.path.isdir(c)]
        try:
            carpetas.append(self.user_data_dir)
        except Exception:
            pass
        carpetas.append(QUIEN)

        base, ext = os.path.splitext(nombre)
        sello = datetime.now().strftime("%Y%m%d_%H%M%S")
        for carpeta in carpetas:
            try:
                os.makedirs(carpeta, exist_ok=True)
                ruta = os.path.join(carpeta, f"{base}_{sello}{ext}")
                with open(ruta, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
                    f.write(contenido)
                return ruta
            except Exception:
                continue
        return None

    def abrir(self, url):
        try:
            import webbrowser
            if not webbrowser.open(url):
                raise RuntimeError("sin navegador")
        except Exception:
            Clipboard.copy(url)
            self.aviso(self.t("enlace_copiado"), url)

    def aviso(self, titulo, texto):
        pal = self.pal
        cont = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        lb = Label(text=texto or "", color=pal["TEXTO"], halign="center", valign="middle")
        lb.bind(size=lambda i, s: setattr(i, "text_size", s))
        b = BotonGrad(text=self.t("entendido"), size_hint_y=None, height=dp(44))
        cont.add_widget(lb)
        cont.add_widget(b)
        p = Popup(title=titulo, content=cont, size_hint=(0.9, 0.4), background="",
                  background_color=pal["VENTANA"], title_color=pal["AZUL"])
        b.bind(on_release=p.dismiss)
        p.open()

    @blindado
    def abrir_contacto(self, *a):
        pal, t = self.pal, self.t
        cont = ScrollView(size_hint=(1, 1))
        caja = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10), size_hint_y=None)
        caja.bind(minimum_height=caja.setter("height"))

        if os.path.exists(LOGO2):
            caja.add_widget(Image(source=LOGO2, size_hint_y=None, height=dp(100)))

        caja.add_widget(etiqueta(t("info_servicios"), markup=True, color=pal["TEXTO"]))

        for texto, url in ((t("btn_telegram") + "t.me/CipherlosAltos", TELEGRAM),
                           (t("btn_blog"), BLOG),
                           (t("btn_github"), GITHUB)):
            b = BotonGrad(text=texto, size_hint_y=None, height=dp(44))
            b.bind(on_release=lambda *_, u=url: self.abrir(u))
            caja.add_widget(b)

        caja.add_widget(Label(text=t("lbl_apoyo"), bold=True, color=pal["MORADO"],
                              size_hint_y=None, height=dp(30)))
        caja.add_widget(etiqueta(t("txt_apoyo"), color=pal["TEXTO"]))

        for texto, url in ((t("btn_paypal"), PAYPAL), (t("btn_kofi"), KOFI)):
            b = BotonGrad(text=texto, size_hint_y=None, height=dp(44))
            b.bind(on_release=lambda *_, u=url: self.abrir(u))
            caja.add_widget(b)

        cerrar = Button(text=t("cerrar"), size_hint_y=None, height=dp(40), background_normal="",
                        background_color=pal["GRIS_CLARO"], color=pal["TEXTO"])
        caja.add_widget(cerrar)
        caja.add_widget(Label(text=t("desarrollado"), color=pal["GRIS"], size_hint_y=None,
                              height=dp(30), font_size=sp(12)))

        cont.add_widget(caja)
        p = Popup(title=t("contacto_titulo"), content=cont, size_hint=(0.92, 0.9), background="",
                  background_color=pal["VENTANA"], title_color=pal["AZUL"],
                  separator_color=pal["MORADO"])
        cerrar.bind(on_release=p.dismiss)
        p.open()


if __name__ == "__main__":
    YugiohCounterApp().run()
