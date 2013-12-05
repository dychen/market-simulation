import random

class Environment:
    def __init__(self):
        self.people = []
        self.commodities = []
        self.history = {}
        self.num_bids = {}
        self.t = 0
        self.update_period = 100
        self.first_names = []
        self.last_names = []
        self.commodity_names = []
        self.load_names()

    def step(self):
        #random.shuffle(self.people)
        self.num_bids = {}
        self.global_sell()
        self.global_buy()
        self.update_prices()
        if self.t % self.update_period:
            for person in self.people:
                person.update_valuations()
        self.update_history()
        self.t += 1
        self.print_env()

    def global_sell(self):
        for commodity in self.commodities:
            for person in self.people:
                if person.sell(commodity):
                    if commodity not in self.num_bids:
                        self.num_bids[commodity] = 0
                    self.num_bids[commodity] -= 1

    def global_buy(self):
        for commodity in self.commodities:
            for person in self.people:
                if person.buy(commodity):
                    if commodity not in self.num_bids:
                        self.num_bids[commodity] = 0
                    self.num_bids[commodity] += 1

    def update_prices(self):
        for commodity in self.num_bids:
            commodity.update_price(self.num_bids[commodity])

    def update_history(self):
        for commodity in self.commodities:
            if commodity not in self.history:
                self.history[commodity] = []
            self.history[commodity].append(commodity.price_per_share)

    def add_person(self):
        name = self.generate_person_name()
        p = Person(self, name)
        self.people.append(p)

    def add_commodity(self):
        name = self.generate_commodity_name()
        c = Commodity(name)
        for person in self.people:
            person.add_commodity(c)
        self.commodities.append(c)

    def generate_person_name(self):
        random.shuffle(self.first_names)
        first = self.first_names[0]
        random.shuffle(self.last_names)
        last = self.last_names[0]
        return first + " " + last

    def generate_commodity_name(self):
        random.shuffle(self.commodity_names)
        return self.commodity_names[0]

    def load_names(self):
        f_first = open('first_names.csv', 'r')
        for line in f_first:
            self.first_names.append(line.strip())
        f_first.close()
        f_last = open('last_names.csv', 'r')
        for line in f_last:
            self.last_names.append(line.strip())
        f_last.close()
        f_commodities = open('commodities.csv', 'r')
        for line in f_commodities:
            self.commodity_names.append(line.strip())
        f_commodities.close()

    def print_history(self):
        for commodity in self.history:
            print "Commodity: " + commodity.name
            print ">> " + str(self.history[commodity])

    def print_env(self):
        for person in self.people:
            person.print_info()
        for commodity in self.commodities:
            commodity.print_info()

class Person:
    def __init__(self, env, name):
        self.name = name
        self.account = 1000 + random.randint(0, 1000)
        #self.buff = random.randint(0, 5)
        self.buff = 0
        self.shares = {}
        self.valuations = {}
        self.initialize_commodities(env)

    def initialize_commodities(self, env):
        for commodity in env.commodities:
            self.add_commodity(commodity)

    def add_commodity(self, commodity):
        self.shares[commodity] = 0
        self.initialize_valuation(commodity)

    def initialize_valuation(self, commodity):
        self.valuations[commodity] = commodity.value + random.randint(0, 20) - 10

    def update_valuations(self):
        for commodity in self.valuations:
            self.initialize_valuation(commodity)

    def buy(self, commodity):
        if self.valuations[commodity] > commodity.price_per_share + self.buff:
            if commodity.num_shares > 0 and (self.account - commodity.price_per_share) > 0:
                self.account -= commodity.price_per_share
                commodity.num_shares -= 1
                self.shares[commodity] += 1
                return True
        return False

    def sell(self, commodity):
        if self.valuations[commodity] < commodity.price_per_share - self.buff:
            if self.shares[commodity] > 0:
                self.account += commodity.price_per_share
                commodity.num_shares += 1
                self.shares[commodity] -= 1
                return True
        return False

    def print_transaction(self, env):
        return

    def print_info(self):
        print "Name: " + self.name
        print "> Account balance: " + str(self.account)
        print "> Shares: "
        for share in self.shares:
            print "> >> " + share.name + ": " + str(self.shares[share])

class Commodity:
    def __init__(self, name):
        self.name = name
        self.value = 10 + random.randint(0, 10)
        self.volatility = random.randint(0, 10)
        self.num_shares = 100 + random.randint(0, 100)
        self.target_shares = int(random.randint(0, 50) * 0.01 * self.num_shares)
        self.price_per_share = max(0, self.value + random.randint(0, 10) - 5)

    def update_price(self, delta):
        self.price_per_share = max(0, self.price_per_share + delta * 0.5 + (self.target_shares - self.num_shares) * 0.05)

    def update_value(self):
        self.value = max(0, self.value + random.randint(-self.volatility, self.volatility))

    def print_info(self):
        print "Commodity: " + self.name
        print "Shares in market: " + str(self.num_shares)
        print " > Target: " + str(self.target_shares)
        print "Price per share: " + str(self.price_per_share)

if __name__ == '__main__':
    num_people = 10
    num_commodities = 1
    e = Environment()
    for _ in range(num_people):
        e.add_person()
    for _ in range(num_commodities):
        e.add_commodity()
    while True:
        e.step()
        r = raw_input("q to quit, h for history: ")
        if r == 'q':
            break
        elif r == 'h':
            e.print_history()
