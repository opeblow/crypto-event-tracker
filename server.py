import asyncio
from fastmcp import FastMCP
from tools import CryptoSearchTool, SearchConfig
import json

# Initializing FastMCP server
mcp = FastMCP("crypto-event-tracker")

# Initializing search tool
search_config = SearchConfig()
search_tool = CryptoSearchTool(search_config)

@mcp.tool()
async def search_crypto_events(query: str, count: int = 10) -> str:
    """
    Search for cryptocurrency events worldwide. Returns upcoming events with dates and general crypto news.
    
    Args:
        query: Search query for crypto events (e.g., 'Bitcoin conference', 'Ethereum upgrade', 'crypto airdrop')
        count: Number of results to return (default: 10)
    """
    # Performing search
    results = await search_tool.search(query, count)
    
    # Parse events
    parsed_response = search_tool.parse_events(results, query)
    
    # Formating the  response
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
    """
    Search for events related to a specific cryptocurrency.
    
    Args:
        coin_name: Name of the cryptocurrency (e.g., 'Bitcoin', 'Ethereum', 'Solana')
        count: Number of results to return (default: 10)
    """
    # Create query for specific coin
    query = f"{coin_name} cryptocurrency events upcoming"
    
    # Performing the search
    results = await search_tool.search(query, count)
    
    # Parse events
    parsed_response = search_tool.parse_events(results, query)
    
    # Formating response
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

if __name__ == "__main__":
    
    mcp.run(transport="stdio")