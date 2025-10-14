# schemas/function_analysis.py

from pydantic import BaseModel, Field
from typing import List, Optional


class FunctionAnalysis(BaseModel):
    """
    A structured analysis of a single Python function. This is our data contract.
    """

    function_name: str = Field(description="The name of the function.")
    description: str = Field(
        description="A concise, one-sentence summary of what the function does."
    )
    args: List[str] = Field(
        description="A list of the function's argument names, e.g., ['arg1', 'arg2']."
    )
    return_type: Optional[str] = Field(
        description="The return type of the function, if specified."
    )
