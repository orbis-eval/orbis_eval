class GoldFileHandler(object):
    def __init__(self, rucksack, gold_path):
        self.rucksack = rucksack
        self.gold_path = gold_path
        self.lense = self.rucksack.open['data']['lense']
        self.mapping = self.rucksack.open['data']['mapping']
        self.filter = self.rucksack.open['data']['filter']
        self.corpus = self.rucksack.open['data']['corpus']

    def run(self):
        raise NotImplementedError
