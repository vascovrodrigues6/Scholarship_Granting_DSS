class Criterion:

    def __init__(self, id, name, weight, isBenefit):
        self.id = id
        self.name = name
        self.weight = weight
        self.isBenefit = isBenefit

    def getName(self):
        return self.name

    def getWeight(self):
        return self.weight

    def getIsBenefit(self):
        return self.isBenefit    

    def changeWeight(self, weight):
        self.weight = weight

