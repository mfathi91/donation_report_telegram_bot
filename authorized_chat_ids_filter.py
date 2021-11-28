from telegram.ext import UpdateFilter


class AuthorizedChatIdsFilter(UpdateFilter):

    def __init__(self, authorized_chat_ids):
        self.authorized_chat_ids = authorized_chat_ids

    def filter(self, update):
        return update.effective_chat.id in self.authorized_chat_ids


