from typing import Type

from crewai.tools import BaseTool

import requests
from bs4 import BeautifulSoup
from openpyxl.styles.builtins import output
from pydantic import BaseModel, Field


class DuckDuckGoInput(BaseModel):
    """Input schema for DuckDuckGoSearchTool"""
    query: str = Field(..., description="The search query the agent wants to look up.")


class DuckDuckGoSearchTool(BaseTool):

    name: str = "DuckDuckGo Search Tool"
    description: str = (
        "Searches the web for a topic using DuckDuckGo and returns the top results "
        "as structured data including title, URL, and content snippet. (JSON format)"
    )
    args_schema: Type[BaseModel] = DuckDuckGoInput

    def _run( self, query: str) -> str:


        url = "https://duckduckgo.com/html/"

        params = {"q": query}

        response = requests.post(
            url,
            data=params,
            timeout=10,
            headers={
                "User-Agent": 'Mozilla/5.0 (Homework Project CrewAI)'
            }
        )

        soup = BeautifulSoup(response.text, "html.parser") # Converts HTML text into DOM like structure


        results = []
        for r in soup.select('.result')[:5]: 
            title_tag = r.select_one('.result__a')
            snippet_tag = r.select_one('.result__snippet')
            if not title_tag:
                continue

            results.append({
                "title": title_tag.get_text(strip=True),
                "url": title_tag["href"],
                "content": snippet_tag.get_text(strip=True) if snippet_tag else ""
            })

        if not results:
            results.append({"title": "", "url": "", "content": "No results found."})

        return results
