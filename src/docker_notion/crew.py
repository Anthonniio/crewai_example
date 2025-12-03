from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.mcp import MCPServerHTTP
from crewai.mcp.filters import create_static_tool_filter
from docker_notion.tools.custom_tool import NOTION_TOOLS
from typing import List, Tuple
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

GOOGLE_TOOL_NAMES: Tuple[str, ...] = (
    "search_web",
    "search_images",
)

@CrewBase
class DockerNotion():
    """DockerNotion crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        """Initialize the crew with MCP server configurations"""
        
        # Configure Google Search MCP (via HTTP)
        self.google_mcp = MCPServerHTTP(
            url=os.getenv("GOOGLE_SEARCH_URL"),
            headers={"Authorization": os.getenv("GOOGLE_SEARCH_KEY")},
            streamable=True,
            tool_filter=create_static_tool_filter(
                allowed_tool_names=list(GOOGLE_TOOL_NAMES)
            ),
            cache_tools_list=True,
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],  # type: ignore[index]
            mcps=[self.google_mcp],
            verbose=True,
            max_interations=3
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],  # type: ignore[index]
            tools=NOTION_TOOLS,
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )
    
    @task
    def deduplicate_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['deduplicate_research_task'], # type: ignore[index]
        )

    @task
    def create_database_entries_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_database_entries_task'], # type: ignore[index]
        )
    
    @task
    def add_simple_descriptions_task(self) -> Task:
        return Task(
            config=self.tasks_config['add_simple_descriptions_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DockerNotion crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )