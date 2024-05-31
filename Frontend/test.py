import requests
class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def send_message(self, chat_id, text, additionals = None):
        if additionals:
            params = additionals.copy()
            params['chat_id'] = chat_id
            params['text'] = text
        else:
            params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp


# token = "6552666858:AAG7IuO8j1RbEbcbpDoBUQDP17qZZnBZGNE"
# chat_id = "@Fintech_TV"
# bot = BotHandler(token)
# print(bot.send_message(chat_id, "hello world!").text)

print(' '.join(['1', '2', '3']))