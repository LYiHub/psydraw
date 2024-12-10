from pydantic import BaseModel
from typing import List, Optional

class MethodList(BaseModel):
    method: List[str]

class AnalysisOutput(BaseModel):
    feature: str
    analysis: str
    
class Usage(BaseModel):
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int

class HTPInput(BaseModel):
    image_path: str
    language: str = "zh"
    
class HTPOutput(BaseModel):
    overall: AnalysisOutput
    house: AnalysisOutput
    tree: AnalysisOutput
    person: AnalysisOutput
    merge: str
    final: str
    signal: str
    usage: Usage
    classification: Optional[bool]
    fix_signal: Optional[str] = None