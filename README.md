# Coffee Shop Research & Notion Database Manager

An AI-powered crew that researches coffee shops in any location and automatically creates organized entries in your Notion database.

## What It Does

This CrewAI-powered system:
- 🔍 **Researches** coffee shops in your specified location
- 📊 **Gathers** ratings, Google Maps URLs, and detailed descriptions
- 🗃️ **Creates** structured entries in your Notion database
- 🧹 **Deduplicates** results to avoid duplicates
- ✍️ **Adds** rich descriptions to each database entry

## Quick Start

### Prerequisites
- Python ≥3.10 <3.14
- OpenAI API key
- Notion integration token and database ID

### Installation

1. Install UV package manager:
```bash
pip install uv
```

2. Install dependencies:
```bash
crewai install
```

3. Configure environment:
```bash
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

4. Update your Notion database ID in `src/docker_notion/main.py`

### Run

```bash
crewai run
```

## Configuration

### Location & Settings
Edit `src/docker_notion/main.py` to customize:
```python
inputs = {
    'location': 'Madrid',           # Target city
    'number_of_shops': 3,          # Number of shops to find
    'database_id': 'your-db-id'    # Your Notion database ID
}
```

### Agents & Tasks
- **Agents**: `src/docker_notion/config/agents.yaml`
- **Tasks**: `src/docker_notion/config/tasks.yaml`

## Output Files

The crew generates several output files:
- `research_output.md` - Raw research results
- `deduplicated_research.md` - Cleaned, unique entries
- `created_entries.md` - Notion database creation log
- `descriptions_added.md` - Description addition log

## Project Structure

```
docker_notion/
├── src/docker_notion/
│   ├── config/
│   │   ├── agents.yaml      # Agent definitions
│   │   └── tasks.yaml       # Task workflows
│   ├── tools/               # Custom tools
│   ├── crew.py             # Main crew logic
│   └── main.py             # Entry point
├── knowledge/              # Reference data
└── tests/                 # Test files
```

## Commands

- `crewai run` - Execute the full workflow
- `crewai train` - Train the crew
- `crewai replay` - Replay specific tasks
- `crewai test` - Test crew performance

## Support

- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [Join Discord](https://discord.com/invite/X4JWnZnxPb)