from decouple import config
import requests
from telegram.ext import Updater, MessageHandler, Filters

token = config('TOKEN')
updater = Updater(token=token)
dispatcher = updater.dispatcher

def stalk(bot, update):
    api = requests.get("https://api.github.com/users/" + update.message.text)
    res = api.json()
    # print(api, res)
    profile = ""
    pic = res["avatar_url"] + "&s=128"
    for data in res:
        url = data.endswith('url')
        ids = data.endswith('id')
        hireable = data.endswith('hireable')
        admin = data.endswith('admin')
        updated = data.endswith('updated_at')
        if url or ids or hireable or admin or updated:
            pass
        else:
            copy = data
            copy_res = res[data]
            if copy == "created_at":
                copy = "Joined"
                copy_res = copy_res.split('T')[0]
            profile += str(copy.title().replace("_", " ")) + ": " + str(copy_res) + "\n"
    profile += pic
    update.message.reply_text(profile)

dispatcher.add_handler(MessageHandler(Filters.text, stalk))

updater.start_polling()
updater.idle()
