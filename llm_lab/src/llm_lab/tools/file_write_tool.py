from typing import Type
from pathlib import Path

from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class FileWriterInput(BaseModel):
    filename: str = Field(..., description="The name of the file to write (with extension).")
    content: str = Field(..., description="The content of the file to write.")
    directory: str = Field(..., description="The directory to write the file to.")

class FileWriterTool(BaseTool):
    name: str = "File Writer"
    description: str = "Write text content to a file on disk."
    args_schema: Type[BaseModel] = FileWriterInput

    def _run(self, filename: str, content: str, directory: str = '.') -> str:

        Path(directory).mkdir(parents=True, exist_ok=True)

        file_path = Path(directory, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Report written to {file_path}"
