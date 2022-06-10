from criterion import Criterion
import pandas as pd

class Criteria:

    def __init__(self):
        self.criteriaList = []
        self.criteriaIndex = 1

    def addCriterion(self,criterionName,criterionWeight,criterionIsBenefit):
        self.criteriaList.append(Criterion("C"+ str(self.criteriaIndex),criterionName,criterionWeight,criterionIsBenefit))
        self.criteriaIndex = self.criteriaIndex+1

    def editCriterionWeight(self,id, newCriterionWeight):
        for criterion in self.criteriaList:
            if criterion.id == id:
                criterion.changeWeight(newCriterionWeight)

    def criteria_list_to_dataframe(self):
        criteria_list = pd.DataFrame(columns=['id', 'Name', 'Weight', 'IsBenefit'])
        for index,criterion in enumerate(self.criteriaList):
            criteria_list.loc[index] = [criterion.id,criterion.name,criterion.weight,criterion.isBenefit]
        return criteria_list
