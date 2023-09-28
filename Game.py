import random
from card import Card

class Game(object):
    def __init__(self):
        self.pn = 3
        self.n_rounds = 3
        self.nlaps = 12
        self.norm = 7
        self.is_over = 1
        self.round = 0
        self.lap = 0
        self.cur = 0
        self.enters_k = 0
        self.score = []
        self.p = [[]]
        self.dealer = [[]]
        self.trump = []
        self.trick = []
        self.balance = []
        self.head = []

    def start(self):
        self.is_over = 0
        self.round = 0
        self.score = [0] * self.pn

    def new_round(self):
        self.lap = 0
        self.cur = 0
        k_decks = (self.pn+2) // 3
        self.p = [[] for i in range(k_decks * 3)]
        self.dealer = [[] for i in range(k_decks)]
        self.trump = []
        self.trick = [0] * self.pn
        self.balance = [0] * self.pn
        self.head = [0] * self.pn

        for h in range(k_decks):
            s, deck = [i for i in range(52)], []
            n = 51
            while n >= 0:
                i = random.randint(0, n)
                deck.append(Card(s[i]))
                s[i], s[n] = s[n], s[i]
                n -= 1
            for i in range(self.nlaps * 4):
                if i%4 == 3:
                    self.dealer[h].append(deck[i])
                else:
                    self.p[h*3 + i%4].append(deck[i])

        self.trump = [pi[0] for pi in self.p]
        for i in range(self.pn):
            self.p[i].sort(key=lambda x: x.suit * 13 + (x.cost+11) % 13)

    def lap_info(self):
        text = f'Ход {self.lap + 1}\n'
        for d in self.dealer:
            text += f' {d[self.lap].to_string()} '
        return text
    def lap_player(self):
        self.enters_k = 0
        return (f'Ходит игрок {self.cur + 1} (козырь: {self.trump[self.cur].suit_emoji()})\n'
                f'Бейте эту карту: {self.dealer[self.cur // 3][self.lap].to_string()}')

    def hand(self):
        h = [[],[],[],[]]
        for c in self.p[self.cur]:
            h[c.suit].append(c)
        return h
    def playable(self, card_id):
        c = Card(card_id)
        d = self.dealer[self.cur // 3][self.lap]
        if c.suit == d.suit:
            return '-'
        b = '-'
        for pc in self.p[self.cur]:
            if pc.suit == d.suit:
                b = d.suit_emoji()
        return b

    def play(self, card_id):
        c = Card(card_id)
        print(c.to_string())
        d = self.dealer[self.cur // 3][self.lap]
        score = c.beat(d, self.trump[self.cur].suit)
        self.balance[self.cur] += score
        play_log = f'Игрок {self.cur + 1}: {c.to_string()} vs. {d.to_string()} = '
        if (score > 0):
            play_log += f'{score}'
            self.trick[self.cur] += 1
            if (self.lap == self.nlaps-1):
                self.head[self.cur] = 1
                play_log += ', голова выиграна!'
        else:
            if (self.lap == self.nlaps-1):
                play_log += 'голова '
            play_log += 'бита'
        play_log += (f'\nВыиграно: {self.trick[self.cur]}/{self.lap + 1}. '
                     f'Баланс: {self.balance[self.cur]}/{self.trick[self.cur] * 7}')
        i = 0
        while self.p[self.cur][i].id != card_id:
            i += 1
        del self.p[self.cur][i]
        self.cur += 1
        if self.cur == self.pn:
            self.cur = 0
            self.lap += 1
        return play_log

    def result(self):
        st = [min(self.trick[i] - self.norm, self.balance[i] // 7 - self.norm) for i in range(self.pn)]
        round_score = [0] * self.pn
        mhead = 0
        kw, kl = 0, 0
        for i in range(self.pn):
            if self.pn <= 3 and self.head[i] == 1:
                mhead = 1
            if st[i] == 0 and self.head[i] == 1:
                if self.pn <= 6:
                    mhead = 1
            elif st[i] > 0:
                round_score[i] = 1
                if self.head[i] == 1:
                    mhead = 1
            else:
                round_score[i] = -1
                kl += 1

        mst, sst = 1, 0
        for i in range(self.pn):
            if st[i] > 0:
                if self.head[i] == mhead:
                    mst = max(mst, st[i])
                    sst += st[i]
                    kw += 1
                else:
                    round_score[i] = -1
                    kl += 1

        bet = 180 * mst
        if kw > 0 and mhead == 0:
            bet //= 3
        cash = bet * max(kw + kl, kw*2)
        for i in range(self.pn):
            if round_score[i] > 0:
                round_score[i] = cash * st[i] // sst - bet
            elif round_score[i] < 0:
                round_score[i] = -bet

        for i in range(self.pn):
            self.score[i] += round_score[i]

        stat = ''
        for i in range(self.pn):
            stat += f'Игрок {i + 1}: {self.trick[i]} карт '
            if self.head[i] == 1:
                stat += 'с головой'
            else:
                stat += 'без головы'
            stat += f', баланс {self.balance[i]}'
            if (st[i] > 0):
                if (self.head[i] == 1):
                    stat += ' - Идеал!'
                    if (st[i] > 1):
                        stat += f' ({st[i]})'
                else:
                    stat += ' - Кандидат'
                    if (st[i] > 1):
                        stat += f' ({st[i]})'
            elif (round_score[i] == 0):
                stat += ' - Норма 🟰 0'
            if round_score[i] > 0:
                stat += f' ♥️ +{round_score[i]}'
            elif round_score[i] < 0:
                stat += f' ♠️ {round_score[i]}'
            stat += '\n'
        return 'Результаты игры:\n' + stat