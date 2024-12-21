import pandas as pd
from typing import List, Union
from itertools import product
from ..question import Single, Multiple


def round_df(df: pd.DataFrame, total: pd.Series, round_digit: int):
    return df.div(total.values, axis=1).map(lambda x: f'{round(x*100, round_digit)}%' if x != 0 and not pd.isna(x) else 0)

def fillna(df: pd.DataFrame) -> pd.DataFrame:
    return df.fillna(0).replace('nan ', 0)

def make_index_col(df: pd.DataFrame) -> pd.DataFrame:
    new_col_level = []
    for i, col in enumerate(df.columns):
        if 'TOTAL' not in col:
            new_col_level.append(f"({chr(65+i)})")
        else:
            new_col_level.append('')
        
    col_tuple = []
    for i, cols in enumerate(df.columns):
        if isinstance(cols, str):
            col_tuple.append((cols, ) + (new_col_level[i], ))
        else:
            col_tuple.append(tuple(cols) + (new_col_level[i], ))
    new_columns = pd.MultiIndex.from_tuples(col_tuple)
    
    df.columns = new_columns
    
def take_desired_col(base: Union[Single, Multiple], deep_by: List[Union[Single, Multiple]]) -> List[str]:
    if deep_by:
        base_questions = deep_by + [base]
        desired_cols = list(product(*[[col.text for col in question.answers] for question in base_questions]))
    else:
        desired_cols = [answer.text for answer in base.answers]
        
    return desired_cols
