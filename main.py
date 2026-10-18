"""Ponto de entrada da aplicação (MVC)."""
import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from controllers.chat_controller import ChatController
from models.chatbot_model import ChatbotModel
from views.chat_view import ChatView


class App:
    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        base = Path(__file__).parent
        self.model = ChatbotModel(base / "data" / "intents.json")
        self.view = ChatView(self.model.bot_name)
        self.controller = ChatController(self.model, self.view)

    def run(self) -> int:
        self.view.show()
        return self.qt_app.exec_()


if __name__ == "__main__":
    sys.exit(App().run())
