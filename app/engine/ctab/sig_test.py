from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.multitest import multipletests
import pandas as pd
from typing import Literal

def _sig_test(crosstab: pd.DataFrame, total_df: pd.Series, alpha: float, adjust: Literal['none', 'bonferroni']='none') -> pd.DataFrame:
    num_cols = crosstab.shape[1]
    test_df = pd.DataFrame('', index=crosstab.index, columns=crosstab.columns)
    letters = [chr(65 + i) for i in range(num_cols)]
    n = list(total_df.values)

    for i in range(num_cols):
        for j in range(i + 1, num_cols):
            col1_letter, col2_letter = letters[i], letters[j]
            count1, count2 = crosstab.iloc[:, i].values, crosstab.iloc[:, j].values
            total1, total2 = n[i], n[j]

            p_vals = []
            for row in range(len(count1)):
                current_col1, current_col2 = count1[row], count2[row]
                                
                if total1 == 0 or total2 == 0 or current_col1 == 0 or current_col2 == 0 or current_col1 == total1 or current_col2 == total2:
                    p_vals.append(pd.NA)
                    continue
                
                if current_col1 + current_col2 > 0:
                    z_stat, p_val = proportions_ztest([current_col1, current_col2], [total1, total2])
                    p_vals.append(p_val)
                else:
                    p_vals.append(pd.NA)

            if adjust != 'none':
                reject, p_adjusted, _, _ = multipletests(p_vals, method=adjust, alpha=alpha)
            else:
                reject = [p < alpha for p in p_vals]
                p_adjusted = p_vals
                
            for row in range(len(count1)):
                if pd.notna(reject[row]) and reject[row]:
                    if count1[row] / total1 > count2[row] / total2:
                        test_df.iloc[row, i] += f'{col2_letter}'
                    else:
                        test_df.iloc[row, j] += f'{col1_letter}'
                                                  
    return test_df