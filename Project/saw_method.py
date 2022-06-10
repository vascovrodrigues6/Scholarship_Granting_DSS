import pandas as pd
import mcdm

class SAW:

    def __init__(self):
        pass

    def saw_method(self, data, criteria_list):
        data_for_saw_method = pd.DataFrame(data)
        data_for_saw_method.drop(data_for_saw_method.columns[[0]], axis = 1, inplace = True)
        data_for_saw_method = data_for_saw_method.values.tolist()
        criteria_weights = list(criteria_list['Weight'])
        rank = mcdm.rank(data_for_saw_method,w_vector=criteria_weights,n_method="Linear1",s_method="SAW")
        return rank