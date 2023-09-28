import telebot
import time
from telebot import types
from Game import Game

bot = telebot.TeleBot('6429777300:AAFHTUyXrKZRaElGopWkOMVumLQLGx1tvhk')
game = Game()

@bot.message_handler(commands=['start'])
def main(message):
    #rules_short = open('./Rules/rules_short.txt', 'r')
    #bot.send_message(message.chat.id, *rules_short)
    hall(message)

def hall(message):
    text = ('Начать игру - команда /new\n'
            'Прервать игру - команда /quit\n'
            'Подробнее о правилах игры - команда /help\n'
            'Изменить настройки - команда /settings')
    markup = types.ReplyKeyboardMarkup()
    button_row = [types.KeyboardButton('/new'), types.KeyboardButton('/help'), types.KeyboardButton('/settings')]
    markup.row(*button_row)
    bot.send_message(message.chat.id, text, reply_markup=markup)

def gameover_exception(message):
    if not game.is_over:
        game.enters_k += 2
        bot.send_message(message.chat.id, "Сначала доиграйте игру или прервите с помощью команды /quit")
        return 1
    return 0

@bot.message_handler(commands=['help'])
def help(message):
    if gameover_exception(message):
        return
    rules = open('./Rules/rules_short.txt', 'r')
    bot.send_message(message.chat.id, *rules)
    hall(message)

@bot.message_handler(commands=['settings'])
def settings(message):
    if gameover_exception(message):
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f'Количество игроков: {game.pn}', callback_data='set_pn'))
    markup.add(types.InlineKeyboardButton(f'Количество раундов игры: {game.n_rounds}', callback_data='set_nr'))
    markup.add(types.InlineKeyboardButton(f'Назад', callback_data='to_hall'))
    bot.send_message(message.chat.id, 'Изменить настройки игры', reply_markup=markup)

@bot.message_handler(commands=['quit'])
def quit(message):
    game.is_over = 1
    hall(message)

@bot.message_handler(commands=['new'])
def newGame(message):
    if gameover_exception(message):
        return
    game.start()
    new_round(message)

def new_round(message):
    game.new_round()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Поехали!', callback_data='newround'))
    bot.send_message(message.chat.id, f'♠️♥️♣️♦️ Раунд {game.round+1} ♠️♥️♣️♦️', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'set_pn':
        set_pn(callback.message)
    elif callback.data == 'set_nr':
        set_nrounds(callback.message)
    elif callback.data == 'to_hall':
        hall(callback.message)
    elif callback.data == 'newround':
        game_lap(callback.message)
    else:
        game.enters_k += 1
        card_id = int(callback.data)
        dealer = game.playable(card_id)
        if dealer == '-':
            pick_card(callback.message, card_id)
        else:
            bot.send_message(callback.message.chat.id, f'У вас ещё остались карты масти {dealer}')

def pick_card(message, card_id):
    play_log = game.play(card_id)
    print(play_log)
    bot.send_message(message.chat.id, play_log)
    for i in range(game.enters_k):
        bot.delete_message(message.chat.id, message.message_id + i)
    time.sleep(2)
    game_lap(message)

def game_lap(message):
    if game.lap == game.nlaps:
        bot.send_message(message.chat.id, game.result())
        game.round += 1
        if game.round == game.n_rounds:
            end_game(message)
        else:
            new_round(message)
    else:
        if game.cur == 0:
            bot.send_message(message.chat.id, game.lap_info())
        bot.send_message(message.chat.id, game.lap_player(), reply_markup=markup_hand())

def end_game(message):
    game.is_over = 1
    text = 'Результаты:\n'
    rating = [(i+1, game.score[i]) for i in range(game.pn)]
    rating.sort(key=lambda x: -x[1])
    for i in range(len(rating)):
        text += f'{i+1}. Игрок {rating[i][0]} ({rating[i][1]} баллов)\n'
    bot.send_message(message.chat.id, text)
    hall(message)

def markup_hand():
    cards = game.hand()
    markup = types.InlineKeyboardMarkup()
    for i in range(4):
        if len(cards[i]) > 0:
            buttons = [types.InlineKeyboardButton(c.to_string(), callback_data=str(c.id)) for c in cards[i]]
            markup.row(*buttons)
    return markup

def set_pn(message):
    bot.send_message(message.chat.id, 'Введите количество игроков - целое число от 2 до 9')
    bot.register_next_step_handler(message, check_pn)
def check_pn(message):
    if not message.text.isnumeric():
        set_pn(message)
        return
    pn = int(message.text)
    if 2 <= pn <= 9:
        game.pn = pn
        settings(message)
    else:
        set_pn(message)

def set_nrounds(message):
    bot.send_message(message.chat.id, 'Введите количество раундов - целое число от 1 до 14')
    bot.register_next_step_handler(message, check_nrounds)
def check_nrounds(message):
    if not message.text.isnumeric():
        set_nrounds(message)
        return
    n_rounds = int(message.text)
    if 1 <= n_rounds <= 14:
        game.n_rounds = n_rounds
        settings(message)
    else:
        set_nrounds(message)

bot.infinity_polling()