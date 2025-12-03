from crewai import Agent, Task, Crew
from crewai.mcp import MCPServerHTTP
import os
from typing import Tuple
from crewai.mcp.filters import create_static_tool_filter
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

GOOGLE_TOOL_NAMES: Tuple[str, ...] = (
    "search_web",
    "search_images",
)

# Verificar que las variables existen
google_url = os.getenv("GOOGLE_SEARCH_URL")
google_key = os.getenv("GOOGLE_SEARCH_KEY")

if not google_url or not google_key:
    raise ValueError(
        "Missing environment variables:\n"
        f"GOOGLE_SEARCH_URL: {'✓' if google_url else '✗'}\n"
        f"GOOGLE_SEARCH_KEY: {'✓' if google_key else '✗'}\n"
        "Please check your .env file"
    )

# Create your agent
researcher = Agent(
    role="Senior Coffee Shop Research Specialist for Madrid",
    goal="Find verified, real coffee shops in Madrid with accurate information.",
    backstory="You're an expert in discovering and evaluating coffee shops with 10+ years of experience. The current year is 2025.",
    mcps=[
        MCPServerHTTP(
            url=google_url,
            headers={"Authorization": google_key},
            streamable=True,
            tool_filter=create_static_tool_filter(
                allowed_tool_names=list(GOOGLE_TOOL_NAMES)
            ),
            cache_tools_list=True,
        )
    ],
    verbose=True,
    max_iter=1
)

# Parámetros para la tarea
location = "Madrid"
number_of_shops = 5
current_year = 2025

# Crear la tarea
research_task = Task(
    description=f"""
    Conduct a thorough research about coffee shops in Madrid.
    
    Use web search to find information about the best specialty coffee shops.
    For each coffee shop you find, gather:
    - Name of the coffee shop (must be a real, existing establishment)
    - Rating based on reviews and reputation (estimate a number between 1-5)
    - Google Maps location URL (search for "coffee shop name + Madrid google maps")
    - Detailed information (atmosphere, specialties, what makes it unique)
    
    IMPORTANT:
    - Always verify that search results contain actual information before processing
    - If a search returns no results, try a different query
    - If you can't find 3 coffee shops, find as many as you can (minimum 3)
    - Make sure each coffee shop name is unique
    - For Google Maps URLs, use the format: https://www.google.com/maps/search/?api=1&query=COFFEE_SHOP_NAME+Madrid
    
    Current year: 2025
    """,
    expected_output=f"""
    A structured list of coffee shops, each containing:
    - name (string)
    - rating (number between 1-5)
    - google_maps_url (valid URL)
    - description (detailed text about the coffee shop)
    
    If fewer than 3 were found, explain why and provide what you found.
    """,
    agent=researcher,
    output_file="research_output.md"
)

# Crear el crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True
)

# Ejecutar
print(f"🔍 Searching for 3 coffee shops in Madrid...\n")
result = crew.kickoff()
print("\n" + "="*50)
print("RESULT:")
print("="*50)
print(result.raw)