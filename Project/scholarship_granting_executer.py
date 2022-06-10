import json
from os import path
from criteria import Criteria
from alternative import Alternative
import normalizer
import pandas as pd
import json_manager as jm
from distutils.util import strtobool
from saw_method import SAW
from topsis_method import TOPSIS
from wp_method import WP
from mixed_approach import MixedMethods
import json_manager as jm

class ScholarshipGrantingExecuter:

    def __init__(self) -> None:
        self.criteriaList = Criteria()
        self.alternativeList = []
        self.decisionMatrix = pd.DataFrame(columns=['id', 'C1', 'C2', 'C3', 'C4', 'C5'])
        self.normalizedDecisionMatrix = pd.DataFrame(columns=['id', 'C1', 'C2', 'C3', 'C4', 'C5'])
        self.threshold = {"Type":"Value", "Value":0.50}
        self.resultsWithThreshold = pd.DataFrame(columns=['id', 'C1', 'C2', 'C3', 'C4', 'C5', 'ranking', 'elegibility'])
        self.resultsWithoutThreshold = pd.DataFrame(columns=['id', 'C1', 'C2', 'C3', 'C4', 'C5', 'ranking'])

    def setupCriteria(self):
        listCriteria = jm.readJson("criteria")
        for item in listCriteria["Criteria"]:
            self.criteriaList.addCriterion(item["name"],float(item["weight"]),bool(strtobool(item["isBenefit"])))

    def setupAlternatives(self,alternativeList):
        for item in alternativeList:
            newAlternative = Alternative(item.id,item.c1_answer,item.c2_answer,
            item.c3_answer,item.c4_answer,item.c5_answer)
            self.alternativeList.append(newAlternative)
    
    def setupAlternativesFromFile(self):
        alternativeList = jm.readJson("alternatives")
        for item in alternativeList["Alternatives"]:
            newAlternative = Alternative(item["id"],item["c1_answer"], float(item["c2_answer"]),
            int(item["c3_answer"]),int(item["c4_answer"]),item["c5_answer"])
            self.alternativeList.append(newAlternative)

    def editCriterionWeight(self,id,newCriterionWeight):
        self.criteriaList.editCriterionWeight(id,newCriterionWeight)

    def editAlternativeCriteriaAnswer(self,id,criterion,newAnswer):
        for alternative in self.decisionMatrix:
            if alternative.id == id:
                if criterion == "C1":
                    alternative.changeC1Answer(newAnswer)
                elif criterion == "C2":
                    alternative.changeC2Answer(newAnswer)
                elif criterion == "C3":
                    alternative.changeC3Answer(newAnswer)
                elif criterion == "C4":
                    alternative.changeC4Answer(newAnswer)
                elif criterion == "C5":
                    alternative.changeC5Answer(newAnswer)
        
    def obtainNormalizedDecisionMatrix(self):
        decisionMatrix = pd.DataFrame(map(Alternative.toArray, self.alternativeList), columns=['id', 'C1', 'C2', 'C3', 'C4', 'C5'])
        self.normalizedDecisionMatrix["id"] = decisionMatrix["id"]
        self.normalizedDecisionMatrix["C1"] = decisionMatrix["C1"].map(lambda a: normalizer.normalizeC1_C5(a))
        self.normalizedDecisionMatrix["C2"] = decisionMatrix["C2"].map(lambda a: normalizer.normalizeC2(a))
        self.normalizedDecisionMatrix["C3"] = decisionMatrix["C3"].map(lambda a: normalizer.normalizeC3(a))
        self.normalizedDecisionMatrix["C4"] = decisionMatrix["C4"].map(lambda a: normalizer.normalizeC4(a))
        self.normalizedDecisionMatrix["C5"] = decisionMatrix["C5"].map(lambda a: normalizer.normalizeC1_C5(a))

    def runSAWMethod(self):
        saw_method = SAW()
        criteria_list = self.criteriaList.criteria_list_to_dataframe()
        results = saw_method.saw_method(self.normalizedDecisionMatrix, criteria_list)
        if self.threshold["Type"] == "":
            self.mergeResultsWithInputNoThreshold(results)
        else:
            self.mergeResultsWithInputWithThreshold(results)

    def runTOPSISMethod(self):
        topsis_method = TOPSIS()
        criteria_list = self.criteriaList.criteria_list_to_dataframe()
        results = topsis_method.topsis_method(self.normalizedDecisionMatrix, criteria_list)
        if self.threshold["Type"] == "":
            self.mergeResultsWithInputNoThreshold(results)
        else:
            self.mergeResultsWithInputWithThreshold(results)

    def runWPMethod(self):
        wp_method = WP()
        criteria_list = self.criteriaList.criteria_list_to_dataframe()
        results = wp_method.wp_method(self.normalizedDecisionMatrix, criteria_list)
        if self.threshold["Type"] == "":
            self.mergeResultsWithInputNoThreshold(results)
        else:
            self.mergeResultsWithInputWithThreshold(results)

    def runMixedMethod(self):
        mixed_approach = MixedMethods()
        criteria_list = self.criteriaList.criteria_list_to_dataframe()
        results = mixed_approach.mixed_approach(self.normalizedDecisionMatrix, criteria_list)
        if self.threshold["Type"] == "":
            self.mergeResultsWithInputNoThreshold(results)
        else:
            self.mergeResultsWithInputWithThreshold(results)

    def mergeResultsWithInputNoThreshold(self, results):
        results_dataframe = pd.DataFrame(results, columns=["id","result_value"])
        results_dataframe["id"] = results_dataframe["id"].str.upper()
        self.resultsWithoutThreshold = pd.merge(self.normalizedDecisionMatrix, results_dataframe, how='left', on="id")
        return results_dataframe

    def mergeResultsWithInputWithThreshold(self, results):
        results_dataframe = self.mergeResultsWithInputNoThreshold(results)
        if self.threshold["Type"] == "Number":
            self.obtainEligibilityNumber(results_dataframe)
        if self.threshold["Type"] == "Value":
            self.obtainEligibilityValue(results_dataframe)

    def obtainEligibilityNumber(self,results):
        results_dataframe_ordered = results.sort_values("result_value", ascending=False)
        number_scholarships = self.threshold["Value"]
        eligibility = [True] * number_scholarships
        eligibility.extend([False] * (len(results_dataframe_ordered["id"]) - number_scholarships))
        results_dataframe_ordered.insert(len(results_dataframe_ordered.columns), 'eligibility', eligibility)
        self.resultsWithThreshold = pd.merge(self.normalizedDecisionMatrix, results_dataframe_ordered, how='left', on="id")

    def obtainEligibilityValue(self,results):
        results_dataframe = results
        eligibility = []
        minimum_value = self.threshold["Value"]
        for result in results["result_value"]:
            if float(result) >= float(minimum_value):
                eligibility.append(True)
            else:
                eligibility.append(False)
        results_dataframe.insert(len(results_dataframe.columns), 'eligibility', eligibility)
        self.resultsWithThreshold = pd.merge(self.normalizedDecisionMatrix, results_dataframe, how='left', on="id")

    def exportAlternatives(self,filename):
        exportAlternativeLines= [ob.toDict() for ob in self.alternativeList]
        exportLines = { "Alternatives": exportAlternativeLines }
        jm.writeJson(filename,exportLines)

    def exportResultsWithTreshold(self,filename):
        exportResult = self.resultsWithThreshold.to_dict(orient = "records")
        exportLines = { "Results": exportResult }
        jm.writeJson(filename,exportLines)

    def exportResultsWithoutTreshold(self,filename):
        exportResult = self.resultsWithoutThreshold.to_dict(orient = "records")
        exportLines = { "Results": exportResult }
        jm.writeJson(filename,exportLines)