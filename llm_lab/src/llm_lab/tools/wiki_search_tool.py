from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from llm_lab.src.llm_lab.service.wiki_search import wiki_summary


class WikipediaSummaryToolInput(BaseModel):
    """Input schema for Wikipedia Summary Tool."""
    topic: str = Field(..., description="The topic for which the tool will get a summary of using Wikipedia.")

class WikipediaSummaryTool(BaseTool):
    name = "Wikipedia Summary"
    description = "Fetch a clean summary of a topic from Wikipedia (handles disambiguation)."
    args_schema: Type[BaseModel] = WikipediaSummaryToolInput

    def _run(self, topic: str) -> str:
        return wiki_summary(topic)

