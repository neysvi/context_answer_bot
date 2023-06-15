import openai
import telebot
import pandas as pd
from json import loads, dumps

from similar_post import search_docs, preprocessing_post

# df = pd.read_excel('upd_db.xlsx')
df = pd.read_json('temp.json', orient='records')


openai.api_key = "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"
bot = telebot.TeleBot("6178335762:AAFSVr3YL0rhA5asnHqfpdDno2AZkE-ahrM")
id_users = [1317209052]


# Функция с ответом от ChatGPT
def make_request(message, context):
    context = context['text'][0] + ' ' + context['text'][1]
    msg = [({"role": "user",
             "content": message.text + ' - это вопрос. ' + context + ' - это текст, в котором может содержаться ответ на вопрос.'
                        + ' Сформулируй ответ на вопрос, используя только информацию в тексте. Если ответа в тексте нет, '
                          'напиши "Нет ответа"'})]
    engine = "gpt-3.5-turbo-16k"
    completion = openai.ChatCompletion.create(
        model=engine,
        messages=msg,
        temperature=0.7
    )
    list_of_answers = completion.choices[0].message.content
    return list_of_answers


# Стартовая функция (ответ на прописывание в чате "/start")
@bot.message_handler(commands=["start"])
def send_start(message):
    text = """Hello! This is chatgpt Bot!"""
    bot.send_message(message.chat.id, text)


# Прием текстовых сообщений
@bot.message_handler(content_types=["text"])
def text_answer(message):
    # posts = preprocessing_post(df)
    res = search_docs(df, message.text, top_n=4)
    chatgpt = make_request(message, res)
    bot.send_message(message.chat.id, chatgpt)

    print(res)


if __name__ == "__main__":
    target = bot.infinity_polling()

    # if '@neysvi_bot' in message.text and message.from_user.id in id_users:
    #     chatgpt = make_request(message)  # Вызов функции с ChatGPT и отправка туда твоего сообщения
    # bot_mess_id = bot.reply_to(message, chatgpt).message_id   # ответ конкретному пользователю
    # bot_mess_id = bot.send_message(message.chat.id, chatgpt).message_id
    # bot.forward_message(message.from_user.id, message.chat.id, bot_mess_id)
    # bot.forward_message(message.from_user.id, message.chat.id, message.message_id)
    # bot.send_message(message.chat.id, chatgpt)  # отправка сообщения с ответом chatgpt в чат
    # print(message)

    # @bot.message_handler(content_types=["voice"])
    # def voice_answer(message):
    #     chatgpt = make_request(message)
    #     # print(message.text)
    #     bot.reply_to(message, chatgpt)
