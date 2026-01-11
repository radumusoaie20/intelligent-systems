from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class CalculatorToolInput(BaseModel):
    """Input schema for Calculator Tool Input."""
    expression: str = Field(..., description="A mathematical expression to evaluate.")

class CalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = "Evaluate numeric expressions."
    args_schema: Type[BaseModel] = CalculatorToolInput

    def _run(self, expression: str) -> str:
        return str(eval(expression))