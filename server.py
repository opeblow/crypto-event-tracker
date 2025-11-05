import asyncio
import json
from fastmcp import FastMCP


# Try importing tools safely
try:
    from tools import CryptoSearchTool, SearchConfig
    print("[INFO] Successfully imported tools ")
except Exception as e:
    print(f"ERROR: Failed to import tools: {e}")
    raise


    
# Initialize FastMCP server
print("INFO:Initializing FastMCP server...")
mcp = FastMCP("crypto-event-tracker")

# Initialize search tool with safety
try:
    search_config = SearchConfig()
    search_tool = CryptoSearchTool(search_config)
    print("INFO: Search tool initialized successfully ")
except Exception as e:
    print(f"ERROR:Failed to initialize search tool: {e}")
    raise

@mcp.tool()
async def search_crypto_events(query: str, count: int = 10) -> str:
    """Search for cryptocurrency events worldwide."""
    print(f"DEBUG: search_crypto_events called with query='{query}', count={count}")
    results = await search_tool.search(query, count)
    parsed_response = search_tool.parse_events(results, query)

    response = {
        "query": query,
        "total_results": parsed_response.total_results,
        "events_with_dates": [
            {
                "coin": event.coin_name,
                "title": event.event_title,
                "date": event.event_date.isoformat() if event.event_date else None,
                "location": event.location,
                "description": event.description,
                "category": event.category.value,
                "source": str(event.source_url)
            }
            for event in parsed_response.events_with_dates
        ],
        "events_without_dates": [
            {
                "coin": event.coin_name,
                "title": event.event_title,
                "description": event.description,
                "category": event.category.value,
                "source": str(event.source_url)
            }
            for event in parsed_response.events_without_dates
        ]
    }

    return json.dumps(response, indent=2)

@mcp.tool()
async def search_specific_coin(coin_name: str, count: int = 10) -> str:
    """Search for events related to a specific cryptocurrency."""
    print(f"sDEBUG:search_specific_coin called with coin='{coin_name}', count={count}")
    query = f"{coin_name} cryptocurrency events upcoming"
    results = await search_tool.search(query, count)
    parsed_response = search_tool.parse_events(results, query)

    response = {
        "coin": coin_name,
        "total_results": parsed_response.total_results,
        "events_with_dates": [
            {
                "coin": event.coin_name,
                "title": event.event_title,
                "date": event.event_date.isoformat() if event.event_date else None,
                "location": event.location,
                "description": event.description,
                "category": event.category.value,
                "source": str(event.source_url)
            }
            for event in parsed_response.events_with_dates
        ],
        "events_without_dates": [
            {
                "coin": event.coin_name,
                "title": event.event_title,
                "description": event.description,
                "category": event.category.value,
                "source": str(event.source_url)
            }
            for event in parsed_response.events_without_dates
        ]
    }

    return json.dumps(response, indent=2)


if __name__=="__main__":
    print("INFO:Starting MCP server on stdio")
    try:
        mcp.run(transport="stdio")
    
    except Exception as e :
        print(f"ERROR:MCP server crashed:{e}")