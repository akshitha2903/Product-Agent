from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
import yaml
@CrewBase
class ProductTaggingCrew:
    def __init__(self):
        base_path = os.path.dirname(__file__)  # This will point to src/crewai_prod

        with open(os.path.join(base_path, "config", "agents.yaml"), "r") as f:
            self.agents_config = yaml.safe_load(f)

        with open(os.path.join(base_path, "config", "tasks.yaml"), "r") as f:
            self.tasks_config = yaml.safe_load(f)

        # Initialize Gemini LLM
        self.llm = LLM(
        provider="gemini",
        model="gemini/gemini-1.5-flash",  # ✅ force API-key usage
        api_key=os.getenv("GEMINI_API_KEY")
    )

    @agent
    def product_marketer(self) -> Agent:
        return Agent(
            config=self.agents_config["product_marketer"],
            verbose=True,
            llm=self.llm
        )

    @task
    def generate_description_and_tags(self) -> Task:
        return Task(
            config=self.tasks_config["generate_description_and_tags"],
            output_file="product_output.md",
            agent=self.product_marketer()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.product_marketer()],
            tasks=[self.generate_description_and_tags()],
            process=Process.sequential,
            verbose=True
        )
