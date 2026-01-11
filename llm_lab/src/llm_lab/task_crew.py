import yaml
from crewai import Agent, Crew, Process, Task


from pathlib import Path

from llm_lab.tools.wiki_search_tool import WikipediaSummaryTool
from llm_lab.tools.calculator_tool import CalculatorTool
from llm_lab.tools.file_write_tool import FileWriterTool

from llm_lab.llms import ollama_1b, ollama_270m

class LlmLab():
    """LlmLab crew"""


    def __init__(self, agents_config_path: str = None, tasks_config_path: str = None):

        cwd = Path.cwd()

        print(cwd)

        if agents_config_path is None:
            agents_config_path = cwd / "config" / "agents.yaml"

        if tasks_config_path is None:
            tasks_config_path = cwd / "config" / "tasks.yaml"

        # Load YAML configs
        with open(agents_config_path) as f:
            self.agents_config = yaml.safe_load(f)

        with open(tasks_config_path) as f:
            self.tasks_config = yaml.safe_load(f)


        self.wiki_tool= WikipediaSummaryTool()
        self.calculator_tool = CalculatorTool()
        self.file_writer_tool = FileWriterTool()


    def crew(self) -> Crew:

        # create agents
        primary_author = Agent(
            role=self.agents_config['primary_author']['role'],
            goal=self.agents_config['primary_author']['goal'],
            backstory=self.agents_config['primary_author']['backstory'],
            verbose=True,
            llm=ollama_270m
        )

        claim_extractor = Agent(
            role=self.agents_config['claim_extractor']['role'],
            goal=self.agents_config['claim_extractor']['goal'],
            backstory=self.agents_config['claim_extractor']['backstory'],
            verbose=True,
            llm=ollama_1b
        )

        fact_checker = Agent(
            role=self.agents_config['fact_checker']['role'],
            goal=self.agents_config['fact_checker']['goal'],
            backstory=self.agents_config['fact_checker']['backstory'],
            verbose=True,
            llm=ollama_1b,
            tools=[self.wiki_tool]
        )

        skeptic = Agent(
            role=self.agents_config['skeptic']['role'],
            goal=self.agents_config['skeptic']['goal'],
            backstory=self.agents_config['skeptic']['backstory'],
            verbose=True,
            llm=ollama_1b,
            tools=[self.calculator_tool]
        )

        editor = Agent(
            role=self.agents_config['editor']['role'],
            goal=self.agents_config['editor']['goal'],
            backstory=self.agents_config['editor']['backstory'],
            verbose=True,
            llm=ollama_1b,
            tools=[self.file_writer_tool]
        )

        agents = [primary_author, claim_extractor, fact_checker, skeptic, editor]

        # create tasks
        write_report = Task(
            description=self.tasks_config['write_report']['description'],
            expected_output=self.tasks_config['write_report']['expected_output'],
            agent=primary_author
        )

        extract_claims = Task(
            description=self.tasks_config['extract_claims']['description'],
            expected_output=self.tasks_config['extract_claims']['expected_output'],
            agent=claim_extractor,
            context=[write_report]
        )

        verify_claims = Task(
            description=self.tasks_config['verify_claims']['description'],
            expected_output=self.tasks_config['verify_claims']['expected_output'],
            agent=fact_checker,
            context=[extract_claims]
        )

        skeptic_review = Task(
            description=self.tasks_config['skeptic_review']['description'],
            expected_output=self.tasks_config['skeptic_review']['expected_output'],
            agent=skeptic,
            context=[verify_claims, write_report]
        )

        edit_report = Task(
            description=self.tasks_config['edit_report']['description'],
            expected_output=self.tasks_config['edit_report']['expected_output'],
            agent=editor,
            context=[write_report, verify_claims, skeptic_review]
        )

        write_report_to_file = Task(
            description=self.tasks_config['write_report_to_file']['description'],
            expected_output=self.tasks_config['write_report_to_file']['expected_output'],
            agent=editor,
            context=[edit_report]
        )

        tasks = [write_report, extract_claims, verify_claims, skeptic_review, edit_report, write_report_to_file]

        # create crew
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
