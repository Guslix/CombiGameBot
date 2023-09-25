import telebot
import time
from Game import Game

bot = telebot.TeleBot('6429777300:AAFHTUyXrKZRaElGopWkOMVumLQLGx1tvhk')
game = Game(3)
wrong_enters = 0

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Этот бот разыгрывает один раунд игры. '
                              'Во время раунда игроки по очереди бьют карту ведущего. '
                              'Чтобы набрать хорошую комбинацию, вам нужно выиграть как можно больше карт '
                              'и набрать большую сумму битых карт ведущего.\n'
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
    bot.send_message(message.chat.id, game.lap_info())
    bot.send_message(message.chat.id, game.lap_player())

@bot.message_handler()
def enter_card(message):
    card = game.pick(message.text)
    global wrong_enters
    wrong_enters += 1
    if(card >= 52):
        bot.send_message(message.chat.id, f'У вас ещё остались карты масти {chr(97 + card % 4)}')
    elif(card == -1):
        bot.send_message(message.chat.id, 'У вас нет такой карты')
    elif(card == -2):
        bot.send_message(message.chat.id, 'Масть карты - строчная буква a, b, c, d; '
                                          'номинал карты - число от 2 до 10 или большая буква A, J, Q, K')
    else:
        play_log = game.play(card)
        for i in range(wrong_enters * 2):
            bot.delete_message(message.chat.id, message.message_id - i)
        wrong_enters = 0
        bot.send_message(message.chat.id, play_log)
        time.sleep(5)
        if game.lap == 12:
            bot.send_message(message.chat.id, game.result())
            bot.send_message(message.chat.id, 'Начать новую игру: /new')
        else:
            if game.cur_pl == 0:
                bot.send_message(message.chat.id, game.lap_info())
            bot.send_message(message.chat.id, game.lap_player())

bot.infinity_polling()