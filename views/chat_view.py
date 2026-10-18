"""View: interface gráfica em PyQt5 (sem lógica de negócio)."""
import html

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QTextBrowser, QVBoxLayout, QWidget)

STYLE = """
QMainWindow { background: #1e1f29; }
QLabel#title { color: #e0e0ff; font-size: 18px; font-weight: bold; padding: 6px; }
QTextBrowser { background: #282a36; color: #f8f8f2; border-radius: 8px;
               padding: 8px; font-size: 14px; border: 1px solid #44475a; }
QLineEdit { background: #282a36; color: #f8f8f2; border: 1px solid #6272a4;
            border-radius: 8px; padding: 8px; font-size: 14px; }
QPushButton { background: #7c5cff; color: white; border: none; border-radius: 8px;
              padding: 8px 16px; font-weight: bold; }
QPushButton:hover { background: #9479ff; }
QPushButton#clear { background: #44475a; }
QLabel#status { color: #8be9fd; font-size: 11px; }
"""


class ChatView(QMainWindow):
    """Janela principal. Emite sinais; o Controller decide o que fazer."""

    send_requested = pyqtSignal(str)
    clear_requested = pyqtSignal()

    def __init__(self, bot_name: str = "PyBot"):
        super().__init__()
        self.setWindowTitle(f"{bot_name} - Chatbot com Scikit-learn")
        self.resize(560, 640)
        self.setStyleSheet(STYLE)
        self._build_ui(bot_name)

    def _build_ui(self, bot_name):
        central = QWidget()
        layout = QVBoxLayout(central)

        title = QLabel(f"🤖 {bot_name}")
        title.setObjectName("title")
        layout.addWidget(title)

        self.dialog = QTextBrowser()
        layout.addWidget(self.dialog)

        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Digite sua mensagem...")
        self.input.returnPressed.connect(self._on_send)
        self.send_btn = QPushButton("Enviar")
        self.send_btn.clicked.connect(self._on_send)
        self.clear_btn = QPushButton("Limpar")
        self.clear_btn.setObjectName("clear")
        self.clear_btn.clicked.connect(self.clear_requested.emit)
        row.addWidget(self.input)
        row.addWidget(self.send_btn)
        row.addWidget(self.clear_btn)
        layout.addLayout(row)

        self.status = QLabel("Pronto.")
        self.status.setObjectName("status")
        layout.addWidget(self.status)

        self.setCentralWidget(central)

    def _on_send(self):
        text = self.input.text().strip()
        if text:
            self.input.clear()
            self.send_requested.emit(text)

    # --- Métodos públicos usados pelo Controller ---
    def show_message(self, sender: str, text: str, time_str: str, is_user: bool):
        color = "#50fa7b" if is_user else "#bd93f9"
        align = "right" if is_user else "left"
        self.dialog.append(
            f'<p align="{align}"><span style="color:{color};"><b>{html.escape(sender)}</b></span> '
            f'<span style="color:#6272a4;font-size:10px;">{time_str}</span><br>'
            f'{html.escape(text)}</p>'
        )
        self.dialog.verticalScrollBar().setValue(self.dialog.verticalScrollBar().maximum())

    def set_status(self, text: str):
        self.status.setText(text)

    def clear_dialog(self):
        self.dialog.clear()
