from telegram.ext import UpdateFilter


class ReliableUserFilter(UpdateFilter):

    def filter(self, update):
        return update.effective_chat.id == CHAT_ID


