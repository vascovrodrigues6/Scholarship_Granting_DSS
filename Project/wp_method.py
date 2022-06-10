import pandas as pd
import mcdm

class WP:

    def __init__(self):
        pass

    def normalizeWeights(self,criteria_weights):
        #criteria_weights = list(criteria_list['Weight'])
        sum_weights = sum(criteria_weights)
        new_criteria_weights = [weight/sum_weights for weight in criteria_weights]
        return new_criteria_weights

    def wp_method(self, data, criteria_list):
        data_for_wp_method = pd.DataFrame(data)
        data_for_wp_method.drop(data_for_wp_method.columns[[0]], axis = 1, inplace = True)
        if sum(data_for_wp_method["C1"]) == 0:
            data_for_wp_method.drop(data_for_wp_method["C1"], axis = 1, inplace = True)
        if sum(data_for_wp_method["C5"]) == 0:
            data_for_wp_method.drop(data_for_wp_method["C5"], axis = 1, inplace = True)
        data_for_wp_method = data_for_wp_method.values.tolist()
        criteria_weights = list(criteria_list['Weight'])
        criteria_weights = self.normalizeWeights(criteria_weights)
        rank = mcdm.rank(data_for_wp_method,w_vector=criteria_weights,s_method="MEW")
        results_dataframe = pd.DataFrame(rank, columns=["id","result_value"])
        sum_results = sum(results_dataframe["result_value"])
        if sum_results != 0:
            results_dataframe["result_value"] = [result/sum_results for result in results_dataframe["result_value"]]
        return rank