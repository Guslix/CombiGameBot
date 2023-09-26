import telebot
import time
from telebot import types
from Game import Game

bot = telebot.TeleBot('6429777300:AAFHTUyXrKZRaElGopWkOMVumLQLGx1tvhk')
game = Game(3, 12)
enters_k = 0

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Этот бот разыгрывает один раунд игры. '
                              'Во время раунда игроки по очереди бьют карту ведущего. '
                              'Чтобы набрать хорошую комбинацию, вам нужно выиграть как можно больше карт '
                              'и набрать большую сумму битых карт ведущего.\n'
                              'Как побить карту ведущего:\n'
                              ' - Картой той же масти, которая больше весит.\n'
                              ' - Туз - единица, то есть самая слабая карта, но может побить только короля.\n'
                              ' - Если закончилась эта масть, можно выложить любую карту. Карта другой масти всё время '
                              'проигрывает карте ведущего, если это не козырь.\n'
                              ' - В этой игре есть козыри. У каждого игрока своя козырная масть. Козырь может бить любую карту другой масти.\n'
                              ' - Нельзя выкладывать карту другой масти, если у вас остались карты масти как у ведущего.\n\n'
                              'Есть 4 уровня комбинаций:\n'
                              '1. Идеал - Выиграно от 8 карт, сумма битых карт не меньше 56, первая и последняя карты выиграны\n'
                              '2. Кандидат - Тоже от 8 карт и сумма не меньше 56, но проиграна первая или последняя карта\n'
                              '3. Норма - Выиграно от 7 карт, сумма битых карт не меньше 49, выиграна последняя карта\n'
                              '4. Плохая комбинация - комбинация, которая не достигла первых трёх уровней\n'
                              'Все правила можете узнать с помощью команды /help')
    bot.send_message(message.chat.id, 'Начать игру: команда /new\n'
                              'Вы можете в любой момент начать новую игру с помощью этой команды')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Этот бот разыгрывает один раунд игры. '
                              'Во время раунда игроки по очереди бьют карту ведущего. '
                              'Чтобы набрать хорошую комбинацию, вам нужно выиграть как можно больше карт '
                              'и набрать большую сумму битых карт ведущего.\n'
                              'Есть 4 уровня комбинаций:\n'
                              '1. Идеал - Выиграно от 8 карт, сумма битых карт не меньше 56, первая и последняя карты выиграны\n'
                              '2. Кандидат - Тоже от 8 карт и сумма не меньше 56, но проиграна первая или последняя карта\n'
                              '3. Норма - Выиграно от 7 карт, сумма битых карт не меньше 49, выиграна последняя карта\n'
                              '4. Плохая комбинация - комбинация, которая не достигла первых трёх уровней\n')

@bot.message_handler(commands=['new'])
def newGame(message):
    bot.send_message(message.chat.id, 'Поехали!')
    game.start()
    game_lap(message)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global enters_k
    enters_k += 1
    card_id = int(callback.data)
    if game.playable(card_id):
        pick_card(callback.message, card_id)
    else:
        bot.send_message(callback.message.chat.id, f'У вас ещё остались карты масти {game.dealer.to_string()[0]}')

def pick_card(message, card_id):
    play_log = game.play(card_id)
    print(play_log)
    bot.send_message(message.chat.id, play_log)
    global enters_k
    for i in range(enters_k):
        bot.delete_message(message.chat.id, message.message_id + i)
    enters_k = 0
    time.sleep(2)
    game_lap(message)

def game_lap(message):
    if game.is_over:
        bot.send_message(message.chat.id, game.result())
        bot.send_message(message.chat.id, 'Начать новую игру: /new')
    else:
        if game.cur == 0:
            bot.send_message(message.chat.id, game.lap_info())
        bot.send_message(message.chat.id, game.lap_player(), reply_markup=markup_hand())

def markup_hand():
    cards = game.hand()
    markup = types.InlineKeyboardMarkup()
    for i in range(4):
        if len(cards[i]) > 0:
            buttons = [types.InlineKeyboardButton(c.to_string(), callback_data=str(c.id)) for c in cards[i]]
            markup.row(*buttons)
    return markup

bot.infinity_polling()