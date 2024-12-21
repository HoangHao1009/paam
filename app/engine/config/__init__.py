from typing import Literal, List

class DataFrameConfig:
    scale_encode: bool = False
    
    def __str__(self):
        return f"Question DataFrame Config: scale_encode: {self.scale_encode}"
    
    def __repr__(self):
        return f"Question DataFrame Config: scale_encode: {self.scale_encode}"

class CrossTabConfig:
    def __init__(self, alpha: float=0, pct: bool=False, round_digit: int=0, adjust: Literal['none', 'bonferroni'] = 'none'):
        self.alpha = alpha
        self.pct = pct
        self.round_digit = round_digit
        self.adjust = adjust
        
    def __str__(self):
        return f"CrossTab Config: alpha={self.alpha}, pct={self.pct}, round_digit={self.round_digit}, adjust={self.adjust}"
    
    def __repr__(self):
        return f"CrossTab Config: alpha={self.alpha}, pct={self.pct}, round_digit={self.round_digit}, adjust={self.adjust}"
    
class SPSSConfig:
    def __init__(self, std: bool=False, pct: bool=True, compare_tests: List[str] = ['MEAN', 'PROP'], alpha: float=0.1):
        self.std = std
        self.pct = pct
        self.compare_tests = compare_tests
        self.alpha = alpha
        
    def __str__(self):
        return f"SPSS Config: std={self.std}, pct={self.pct}, compare_tests={self.compare_tests}, alpha={self.alpha}"
    
    def __str__(self):
        return f"SPSS Config: std={self.std}, pct={self.pct}, compare_tests={self.compare_tests}, alpha={self.alpha}"


