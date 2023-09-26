class Card(object):
    def __init__(self, id):
        self.id = id
        self.suit = id // 13
        self.cost = id % 13 + 1

    def to_string(self):
        emoji = ['♠️', '♥️', '♣️', '♦️']
        s = emoji[self.suit]
        if(self.cost == 1):
            s += 'A'
        elif(self.cost == 11):
            s += 'J'
        elif(self.cost == 12):
            s += 'Q'
        elif(self.cost == 13):
            s += 'K'
        else:
            s += str(self.cost)
        return s

    def from_string(s):
        if s[0] < 'a' or s[0] > 'd' or len(s) < 2:
            return -1
        id = (ord(s[0]) - 97) * 13
        c = s[1:]
        if c == 'A':
            return id
        if(c == 'J'):
            return id + 10
        if(c == 'Q'):
            return id + 11
        if(c == 'K'):
            return id + 12
        if c.isnumeric() and int(c) >= 2 and int(c) <= 10:
            return id + int(c)-1
        return -1

    def beat(self, b, trump):
        if self.suit == b.suit and ((self.cost > b.cost and self.cost - b.cost < 12) or b.cost - self.cost == 12):
            return b.cost
        if self.suit != b.suit and self.suit == trump:
            return b.cost
        return 0