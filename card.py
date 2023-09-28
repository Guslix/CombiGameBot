class Card(object):
    def __init__(self, id):
        self.id = id
        self.suit = id // 13
        self.cost = (id+12) % 13 + 2

    def suit_emoji(self):
        return ['♠️', '♥️', '♣️', '♦️'][self.suit]
    def to_string(self):
        s = ''
        if(self.cost == 14):
            s += 'Т'
        elif(self.cost == 11):
            s += 'В'
        elif(self.cost == 12):
            s += 'Д'
        elif(self.cost == 13):
            s += 'K'
        else:
            s += str(self.cost)
        s += self.suit_emoji()
        return s

    def beat(self, b, trump):
        if self.suit == b.suit and self.cost > b.cost:
            return b.cost
        if self.suit == trump and b.suit != trump:
            return b.cost
        return 0
