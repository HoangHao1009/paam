from typing import Literal

class QuestionDfConfig:
    scale_encode: bool = False
    
    def __str__(self):
        return f"Question DataFrame Config: scale_encode: {self.scale_encode}"
    
    def __repr__(self):
        return f"Question DataFrame Config: scale_encode: {self.scale_encode}"
