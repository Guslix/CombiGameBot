import random
from card import Card

class Game(object):
    def __init__(self, pn, nlaps):
        self.pn = pn
        self.nlaps = nlaps
        self.norm = 7
        self.lap = 0
        self.cur = 0
        self.p = [[]]
        self.trump = []
        self.trick = []
        self.balance = []
        self.head = []
        self.dealer = 0
        self.is_over = 1

    def start(self):
        s, deck = [i for i in range(52)], []
        n = 51
        while (n >= 0):
            i = random.randint(0, n)
            deck.append(Card(s[i]))
            s[i], s[n] = s[n], s[i]
            n -= 1

        self.is_over = 0
        self.lap = 0
        self.cur = 0
        self.p = [[] for i in range(4)]
        self.trick = [0 for i in range(self.pn)]
        self.balance = [0 for i in range(self.pn)]
        self.head = [0 for i in range(self.pn)]
        for i in range(self.nlaps * 4):
            self.p[i % 4].append(deck[i])
        self.trump = [self.p[i][0] for i in range(self.pn)]
        for i in range(self.pn):
            self.p[i].sort(key=lambda x: x.id)

    def lap_info(self):
        self.dealer = self.p[3][self.lap]
        return (f'Ход {self.lap + 1}\nКарта ведущего: {self.dealer.to_string()}\n')
    def lap_player(self):
        return (f'Ходит игрок {self.cur + 1} (козырь: {self.trump[self.cur].to_string()[0]})\n'
                f'Бейте эту карту: {self.dealer.to_string()}')

    def hand(self):
        h = [[],[],[],[]]
        for c in self.p[self.cur]:
            h[c.suit].append(c)
        return h
    def playable(self, card_id):
        c = Card(card_id)
        if c.suit == self.dealer.suit:
            return True
        b = True
        for pc in self.p[self.cur]:
            if pc.suit == self.dealer.suit:
                b = False
        return b

    def play(self, card_id):
        c = Card(card_id)
        print(c.to_string())
        score = c.beat(self.dealer, self.trump[self.cur].suit)
        self.balance[self.cur] += score
        play_log = f'Игрок {self.cur + 1}: {c.to_string()} vs. {self.dealer.to_string()} = '
        if (score > 0):
            play_log += f'{score}'
            self.trick[self.cur] += 1
            if (self.lap == 0):
                self.head[self.cur] += 1
            if (self.lap == self.nlaps-1):
                self.head[self.cur] += 2
        else:
            play_log += 'бита'
        play_log += (f'\nВыиграно: {self.trick[self.cur]}/{self.lap + 1}. '
                     f'Баланс: {self.balance[self.cur]}/{self.trick[self.cur] * 7}. '
                     f'Голова: {self.head[self.cur]}/2')
        i = 0
        while self.p[self.cur][i].id != card_id:
            i += 1
        del self.p[self.cur][i]
        self.cur += 1
        if self.cur == self.pn:
            self.cur = 0
            self.lap += 1
        if self.lap == self.nlaps:
            self.is_over = 1
        return play_log

    def result(self):
        stat = ''
        for i in range(self.pn):
            stat += f'Игрок {i + 1}: выиграно {self.trick[i]} карт, баланс {self.balance[i]}, голова {self.head[i]}'
            st = min(self.trick[i] - self.norm, self.balance[i] // 7 - self.norm)
            if (st > 0):
                if (self.head[i] == 3):
                    stat += ' - Идеал!'
                    if (st > 1):
                        stat += f' ({st})'
                elif (self.head[i] == 2):
                    stat += ' - Норм. кандидат'
                    if (st > 1):
                        stat += f' ({st})'
                elif (self.head[i] == 1):
                    stat += ' - Кандидат'
                    if (st > 1):
                        stat += f' ({st})'
                elif (self.head[i] == 0):
                    stat += ' - голый кандидат'
                    if (st > 1):
                        stat += f' ({st})'
            elif (st == 0 and self.head[i] >= 2):
                stat += ' - Норма'
            stat += '\n'
        return 'Результаты игры:\n' + stat