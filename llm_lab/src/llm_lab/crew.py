import yaml
from crewai import Agent, Crew, Process, Task

from tools.wiki_search_tool import WikipediaSummaryTool

from llms import ollama_1b, ollama_270m

class LlmLab():
    """LlmLab crew"""


    def __init__(self, agents_config_path: str = './config/agents.yaml', tasks_config_path: str = './config/tasks.yaml'):
        # Load YAML configs
        with open(agents_config_path) as f:
            self.agents_config = yaml.safe_load(f)

        with open(tasks_config_path) as f:
            self.tasks_config = yaml.safe_load(f)


        print(self.agents_config)
        print(self.tasks_config)

        print(type(self.agents_config))
        print(type(self.tasks_config))

        print(type(self.agents_config['primary_author']))

        self.wiki_tool= WikipediaSummaryTool()


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
            llm=ollama_1b
        )

        editor = Agent(
            role=self.agents_config['editor']['role'],
            goal=self.agents_config['editor']['goal'],
            backstory=self.agents_config['editor']['backstory'],
            verbose=True,
            llm=ollama_1b
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

        tasks = [write_report, extract_claims, verify_claims, skeptic_review, edit_report]

        # create crew
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
