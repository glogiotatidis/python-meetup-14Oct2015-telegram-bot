import telegram


token = 'YOUR TOKEN HERE'
webhook = 'https://pacific-taiga-2595.herokuapp.com/hook'

class BBot(telegram.Bot):
    def __init__(self):
        super(BBot, self).__init__(token=token)

    def process(self, update):
        return self.sendMessage(chat_id=update.message.chat.id, text=update.message.text)


def main():
    import json
    import os
    from bottle import request, route, run
    from urlparse import urlparse


    bot = BBot()
    bot.setWebhook(webhook)

    @route(urlparse(webhook).path or '/', method='POST')
    def handle_message():
        data = json.load(request.body)
        update = telegram.Update.de_json(data)
        bot.process(update)
        return 'OK'

    @route('/', method='GET')
    def home():
        return 'Hi :)'


    port = os.getenv('PORT')

    try:
        run(host='0.0.0.0', port=port, reloader=False)
    finally:
        bot.db.close()


if __name__ == '__main__':
    main()
