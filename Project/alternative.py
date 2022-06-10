class Alternative:

    def __init__(self,id,c1_answer,c2_answer,c3_answer,c4_answer,c5_answer):
        self.id = id
        self.c1_answer = c1_answer
        self.c2_answer = c2_answer
        self.c3_answer = c3_answer
        self.c4_answer = c4_answer
        self.c5_answer = c5_answer

    def changeC1Answer(self, c1_answer):
        self.c1_answer = c1_answer
    
    def changeC2Answer(self, c2_answer):
        self.c2_answer = c2_answer

    def changeC3Answer(self, c3_answer):
        self.c3_answer = c3_answer

    def changeC4Answer(self, c4_answer):
        self.c4_answer = c4_answer

    def changeC5Answer(self, c5_answer):
        self.c5_answer = c5_answer

    def update(self, c1_answer,c2_answer,c3_answer,c4_answer,c5_answer):
        self.changeC1Answer(c1_answer)
        self.changeC2Answer(c2_answer)
        self.changeC3Answer(c3_answer)
        self.changeC4Answer(c4_answer)
        self.changeC5Answer(c5_answer)
    
    def toArray(self):
        return [self.id,self.c1_answer,self.c2_answer,self.c3_answer,self.c4_answer,self.c5_answer]

    def toDict(self):
        dic = {
            'id': self.id,
            'c1_answer': self.c1_answer,
            'c2_answer': self.c2_answer,
            'c3_answer': self.c3_answer,
            'c4_answer': self.c4_answer,
            'c5_answer': self.c5_answer   
        }
        return dic