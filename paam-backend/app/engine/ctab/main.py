from typing import Union, List
import pandas as pd

from ..question import Single, Multiple, Number
from .sig_test import _sig_test
from ..config import CrossTabConfig
from .utils import round_df, fillna, make_index_col, take_desired_col

pd.options.mode.chained_assignment = None  # Tắt cảnh báo

class CrossTab:
    def __init__(self, 
                 base: Union[Single, Multiple], 
                 target: Union[Single, Multiple, Number], 
                 deep_by: List[Union[Single, Multiple]] = []
            ):
        self.base = base
        self.target = target
        self.deep_by = deep_by
        self.config = CrossTabConfig()
        self._check_valid()
        
    @property
    def questions(self):
        return [self.base] + [self.target] + self.deep_by
    
    @property
    def agg_func(self):
        if isinstance(self.target, Union[Single, Multiple]):
            return pd.Series.nunique
        else:
            return ['mean', 'std']
        
    def _check_valid(self):
        for question in self.questions:
            question._ctab_mode = True
        for deep in self.deep_by:
            if deep._id == self.base._id:
                raise KeyError(f"Deep question: {deep.code} is duplicated with base")
            
    @property 
    def merge_df(self):
        merged_df = None

        for question in self.questions:
            if merged_df is None:
                merged_df = question.df
            else:
                merged_df = merged_df.merge(question.df, how='outer', on='R_ID')

        return merged_df.dropna()
    
    def _ctab_sm(self) -> pd.DataFrame:
        deep_codes = [deep.code for deep in self.deep_by]
        
        pivot_table = pd.pivot_table(
            data=self.merge_df,
            values='R_ID',
            index=self.target.code,
            columns=deep_codes + [self.base.code],
            aggfunc=self.agg_func,
            margins=True,
            margins_name='TOTAL',
            dropna=False
        )
        
        col_total = pivot_table['TOTAL']
        row_total = pivot_table.loc['TOTAL']

        pivot_table.drop('TOTAL', axis=1, inplace=True)
        pivot_table.drop(index='TOTAL', inplace=True)
        
        desired_cols = take_desired_col(self.base, self.deep_by)
        missing_cols = set(desired_cols) - set(pivot_table.columns)

        for col in missing_cols:
            pivot_table[col] = 0
            row_total.loc[col] = 0
                    
        pivot_table = pivot_table[desired_cols]
        
        desired_indexes = [answer.text for answer in self.target.answers]
                                
        pivot_table = pivot_table.reindex(desired_indexes, fill_value=0)
            
        if self.config.alpha:
            test_df = _sig_test(pivot_table, row_total, self.config.alpha, self.config.adjust)
            if self.config.pct:
                pct_pivot_table = round_df(pivot_table, row_total, self.config.round_digit)
                df =  pct_pivot_table.astype(str) + ' ' + test_df.astype(str)
            else:
                df = pivot_table.astype(str) + ' ' + test_df.astype(str)
                
        else:
            if self.config.pct:
                df = round_df(pivot_table, row_total, self.config.round_digit)
            else:
                df = pivot_table
                                    
        df['TOTAL'] = col_total
        df.loc['TOTAL'] = row_total
        
        make_index_col(df)
        
        return fillna(df)
    
    def _ctab_num(self):
        deep_codes = [deep.code for deep in self.deep_by]
        
        pivot_table = pd.pivot_table(
            data=self.merge_df,
            values='R_ID',
            index=self.target.code,
            columns=deep_codes + [self.base.code],
            aggfunc=self.agg_func,
            dropna=False
        ).T

        desired_cols = take_desired_col(self.base, self.deep_by)
        missing_cols = set(desired_cols) - set(pivot_table.columns)

        for col in missing_cols:
            pivot_table[col] = 0

        return fillna(make_index_col(pivot_table))
            
    @property
    def df(self) -> pd.DataFrame:
        if isinstance(self.target, (Single, Multiple)):
            return self._ctab_sm()
        elif isinstance(self.target, (Number)):
            return self._ctab_num()
    
