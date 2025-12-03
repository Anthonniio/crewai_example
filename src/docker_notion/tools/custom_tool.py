from crewai.tools import BaseTool
import os, sys
import requests
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


class NotionPostPage(BaseTool):
    name: str = "post_page"
    description: str = """
        Create a new page in Notion.
        Args:
            properties: dict with page properties (Name, Rating, Location, etc.). Example:
                        properties = {
                            "Name": {"title": [{"text": {"content": "Bar Manolo"}}]},
                            "Rating": {"number": 4.3},
                            "Location": {"url": "https://www.google.com/maps/search/?api=1&query=Toma+Cafe+La+Palma+49+Madrid"}
                        }
        """
    
    def _run(self, properties: dict) -> str:
        api_key = os.getenv('NOTION_API_KEY')
        if not api_key:
            return "Error: NOTION_API_KEY not set"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        parent = {"database_id": os.getenv("NOTION_DATABASE_ID", "test-db-id")}
        payload = {
            "parent": parent,
            "properties": properties
        }
        
        try:
            response = requests.post(
                "https://api.notion.com/v1/pages",
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            page_id = result.get('id', 'unknown')
            return f"Successfully created page with ID: {page_id}"
        except requests.exceptions.HTTPError as e:
            return f"HTTP Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error creating page: {str(e)}"


class NotionPatchBlockChildren(BaseTool):
    name: str = "patch_block_children"
    description: str = """
        Add children blocks to a page.
        Args:
            block_id: The page UUID
            children: List of block objects to add. Example:
                children = [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": "This a description example to add.",
                                        "link": None
                                    }
                                }
                            ]
                        }
                    }
                ]
        """
        
    def _run(self, block_id: str, children: list) -> str:
        api_key = os.getenv('NOTION_API_KEY')
        if not api_key:
            return "Error: NOTION_API_KEY not set"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        payload = {
            "children": children
        }
        
        try:
            response = requests.patch(
                f"https://api.notion.com/v1/blocks/{block_id}/children",
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return f"Successfully added children blocks to {block_id}"
        except requests.exceptions.HTTPError as e:
            return f"HTTP Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error adding children blocks: {str(e)}"


class NotionQueryDatabase(BaseTool):
    name: str = "query_database"
    description: str = "Query a Notion database to check if entries already exist or retrieve existing entries."
    
    def _run(self, database_id: str, filter_obj: Optional[dict] = None) -> str:
        """
        Query a Notion database.
        Args:
            database_id: The database UUID
            filter_obj: Optional filter object
        """
        api_key = os.getenv('NOTION_API_KEY')
        if not api_key:
            return "Error: NOTION_API_KEY not set"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        payload = {}
        if filter_obj:
            payload["filter"] = filter_obj
        
        try:
            response = requests.post(
                f"https://api.notion.com/v1/databases/{database_id}/query",
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            results = result.get('results', [])
            return results
        except requests.exceptions.HTTPError as e:
            return f"HTTP Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error querying database: {str(e)}"


class NotionGetPage(BaseTool):
    name: str = "get_page"
    description: str = "Retrieve information about a specific Notion page by its ID."
    
    def _run(self, page_id: str) -> str:
        """
        Get page details.
        Args:
            page_id: The page UUID
        """
        api_key = os.getenv('NOTION_API_KEY')
        if not api_key:
            return "Error: NOTION_API_KEY not set"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28"
        }
        
        try:
            response = requests.get(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return str(response.json())
        except requests.exceptions.HTTPError as e:
            return f"HTTP Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error getting page: {str(e)}"


class NotionUpdatePage(BaseTool):
    name: str = "update_page"
    description: str = """
        Update page properties.
        Args:
            page_id: The page UUID
            properties: dict with properties to update. Example of properties to update:
                properties = {
                    "Rating": {"number": 2},
                } 
        """
        
    def _run(self, page_id: str, properties: dict) -> str:
        api_key = os.getenv('NOTION_API_KEY')
        if not api_key:
            return "Error: NOTION_API_KEY not set"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        payload = {
            "properties": properties
        }
        
        try:
            response = requests.patch(
                f"https://api.notion.com/v1/pages/{page_id}",
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return f"Successfully updated page {page_id}"
        except requests.exceptions.HTTPError as e:
            return f"HTTP Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error updating page: {str(e)}"

class NotionArchivePage(BaseTool):
    name: str = "archive_page"
    description: str = "Archive (delete) a Notion page by its ID."

    def _run(self, page_id: str) -> str:

        notion_token = os.environ.get("NOTION_API_KEY")
        if not notion_token:
            return "Error: NOTION_API_KEY not set."

        url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        payload = {
            "archived": True, 
            "properties": {}
        }

        response = requests.patch(url, headers=headers, json=payload)

        if response.status_code != 200:
            return f"HTTP Error {response.status_code}: {response.text}"

        return f"Page {page_id} archived successfully."


# Lista de todas las herramientas disponibles para los agentes
NOTION_TOOLS = [
    NotionPostPage(),
    NotionPatchBlockChildren(),
    NotionQueryDatabase(),
    NotionGetPage(),
    NotionUpdatePage(),
    NotionArchivePage(),
]