from saw_method import SAW
from topsis_method import TOPSIS
from wp_method import WP
import pandas as pd

class MixedMethods:

    def __init__(self):
        self.sawWeight = 0.45
        self.wpWeight = 0.35
        self.topsisWeight = 0.2

    def changeSAWWeight(self, newWeight):
        self.sawWeight = newWeight
    
    def changeWPWeight(self, newWeight):
        self.wpWeight = newWeight
    
    def changeTOPSISWeight(self, newWeight):
        self.topsisWeight = newWeight

    def mixed_approach(self, data, criteria_list):
        results_saw = pd.DataFrame(SAW().saw_method(data,criteria_list), columns=["id","result_value_saw"])
        results_topsis = pd.DataFrame(TOPSIS().topsis_method(data,criteria_list), columns=["id","result_value_topsis"])
        results_wp = pd.DataFrame(WP().wp_method(data,criteria_list), columns=["id","result_value_wp"])
        joint_rank = pd.merge(results_saw, results_topsis, how='left', on="id")
        joint_rank = pd.merge(joint_rank, results_wp, how='left', on="id")
        rank = pd.DataFrame(columns=['id', 'result_value'])
        for index,line in enumerate(joint_rank.values):
            weighted_result = ((line[1] * self.sawWeight) + (line[1] * self.topsisWeight) + (line[3] * self.wpWeight))
            rank.loc[index] = [line[0], round(weighted_result,3)]
        return rank