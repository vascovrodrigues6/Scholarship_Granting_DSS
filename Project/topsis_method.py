import pandas as pd
import mcdm

class TOPSIS:

    def __init__(self):
        pass

    def topsis_method(self, data, criteria_list):
        data_for_topsis_method = pd.DataFrame(data)
        data_for_topsis_method.drop(data_for_topsis_method.columns[[0]], axis = 1, inplace = True)
        data_for_topsis_method = data_for_topsis_method.values.tolist()
        criteria_weights = list(criteria_list['Weight'])
        criteria_IsBenefit = list(criteria_list['IsBenefit'])
        rank = mcdm.rank(data_for_topsis_method,w_vector=criteria_weights,n_method="Vector",is_benefit_x=criteria_IsBenefit,s_method="TOPSIS")
        return rank