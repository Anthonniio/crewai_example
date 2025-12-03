import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from docker_notion.tools.custom_tool import (
    NotionPostPage,
    NotionPatchBlockChildren,
    NotionQueryDatabase,
    NotionGetPage,
    NotionUpdatePage,
    NotionArchivePage,
)

# Load environment variables
load_dotenv()

# ===== VARIABLE DE CONTROL =====
# Cambia este valor para ejecutar una prueba diferente
# Opciones: "post_page", "query_database", "get_page", "update_page", "patch_block_children", "archive_page"
TEST_TO_RUN = "post_page"
# ==============================


def test_notion_post_page():
    """Test NotionPostPage tool"""
    print("\n" + "="*60)
    print("TEST: NotionPostPage")
    print("="*60)
    
    tool = NotionPostPage()
    
    # Test data
    
    properties = {
        "Name": {"title": [{"text": {"content": "Bar Manolo"}}]},
        "Rating": {"number": 4.3},
        "Location": {"url": "https://www.google.com/maps/search/?api=1&query=Toma+Cafe+La+Palma+49+Madrid"}
    }
    
    print(f"Input properties: {properties}")
    
    result = tool._run(properties=properties)
    print(f"\nResult: {result}\n")
    return result


def test_notion_query_database():
    """Test NotionQueryDatabase tool"""
    print("\n" + "="*60)
    print("TEST: NotionQueryDatabase")
    print("="*60)
    
    tool = NotionQueryDatabase()
    
    # Test data
    database_id = os.getenv("NOTION_DATABASE_ID", "test-db-id")
    
    print(f"Input database_id: {database_id}")
    
    result = tool._run(database_id=database_id)
    print(f"\nResult: {result}\n")
    return result


def test_notion_get_page():
    """Test NotionGetPage tool"""
    print("\n" + "="*60)
    print("TEST: NotionGetPage")
    print("="*60)
    
    tool = NotionGetPage()
    
    # Test data - you need a valid page ID
    page_id = os.getenv("NOTION_PAGE_ID", "test-page-id")
    
    print(f"Input page_id: {page_id}")
    
    result = tool._run(page_id=page_id)
    print(f"\nResult: {result}\n")
    return result


def test_notion_update_page():
    """Test NotionUpdatePage tool"""
    print("\n" + "="*60)
    print("TEST: NotionUpdatePage")
    print("="*60)
    
    tool = NotionUpdatePage()
    
    # Test data - you need a valid page ID
    page_id = os.getenv("NOTION_PAGE_ID", "test-page-id")
    properties = {
        "Rating": {"number": 2},
    }
    
    print(f"Input page_id: {page_id}")
    print(f"Input properties: {properties}")
    
    result = tool._run(page_id=page_id, properties=properties)
    print(f"\nResult: {result}\n")
    return result


def test_notion_patch_block_children():
    """Test NotionPatchBlockChildren tool"""
    print("\n" + "="*60)
    print("TEST: NotionPatchBlockChildren")
    print("="*60)
    
    tool = NotionPatchBlockChildren()
    
    # Test data - you need a valid page ID
    block_id = os.getenv("NOTION_PAGE_ID", "test-page-id")
    children = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Hey yo.",
                            "link": None
                        }
                    }
                ]
            }
        }
    ]
    
    print(f"Input block_id: {block_id}")
    print(f"Input children: {children}")
    
    result = tool._run(block_id=block_id, children=children)
    print(f"\nResult: {result}\n")
    return result

def test_notion_archive_page():
    """Test NotionArchivePage tool"""
    print("\n" + "="*60)
    print("TEST: NotionArchivePage")
    print("="*60)
    
    tool = NotionArchivePage()
    
    # Test data - you need a valid page ID
    page_id = os.getenv("NOTION_PAGE_ID", "test-page-id")
    
    print(f"Input page_id: {page_id}")
    
    result = tool._run(page_id=page_id)
    print(f"\nResult: {result}\n")
    return result


def main():
    """Main function - selecciona qué test ejecutar"""
    print("\n🔍 Notion Tools Debug Testing Suite")
    print(f"API Key configured: {'✅' if os.getenv('NOTION_API_KEY') else '❌'}")
    print(f"Database ID: {os.getenv('NOTION_DATABASE_ID', 'NOT SET')}")
    print(f"Page ID: {os.getenv('NOTION_PAGE_ID', 'NOT SET')}")
    print(f"\nEjecutando TEST: {TEST_TO_RUN}\n")
    
    tests = {
        "post_page": test_notion_post_page,
        "query_database": test_notion_query_database,
        "get_page": test_notion_get_page,
        "update_page": test_notion_update_page,
        "patch_block_children": test_notion_patch_block_children,
        "archive_page": test_notion_archive_page,
    }
    
    if TEST_TO_RUN not in tests:
        print(f"❌ TEST NO VÁLIDO: {TEST_TO_RUN}")
        print(f"Opciones disponibles: {list(tests.keys())}")
        return
    
    try:
        tests[TEST_TO_RUN]()
        print("✅ Test completado\n")
    except Exception as e:
        print(f"❌ Error durante el test: {str(e)}\n")
        raise


if __name__ == "__main__":
    main()