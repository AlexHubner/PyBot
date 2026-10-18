"""Controller: liga a View ao Model."""
from models.chatbot_model import ChatbotModel, Message
from views.chat_view import ChatView


class ChatController:
    USER_NAME = "Você"

    def __init__(self, model: ChatbotModel, view: ChatView):
        self.model = model
        self.view = view
        self.view.send_requested.connect(self.handle_user_message)
        self.view.clear_requested.connect(self.handle_clear)
        self._bot_say("Olá! Eu sou o PyBot. Digite 'ajuda' para ver o que sei fazer.")

    def _display(self, msg: Message):
        self.view.show_message(msg.sender, msg.text,
                               msg.timestamp.strftime("%H:%M:%S"),
                               is_user=(msg.sender == self.USER_NAME))

    def _bot_say(self, text: str):
        self._display(self.model.add_message(self.model.bot_name, text))

    def handle_user_message(self, text: str):
        self._display(self.model.add_message(self.USER_NAME, text))
        reply, tag, conf = self.model.get_response(text)
        self._bot_say(reply)
        self.view.set_status(f"Intenção: {tag or 'desconhecida'} | confiança: {conf:.0%}")

    def handle_clear(self):
        self.model.clear_history()
        self.view.clear_dialog()
        self.view.set_status("Histórico limpo.")
