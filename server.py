import asyncio
import json
import platform
from fastmcp import FastMCP

mcp=FastMCP("crypto-event-tracker")

_search_tool=None

def get_search_tool():
    """Lazy initialization of search tool"""
    global _search_tool
    if _search_tool is None:
        from tools import CryptoSearchTool,SearchConfig
        search_config=SearchConfig()
        _search_tool=CryptoSearchTool(search_config)
    
    return _search_tool

@mcp.tool
async def search_crypto_events(query:str,count:int=10)->str:
    """Search for cryptocurrency events around the world"""
    tools=get_search_tool()
    results=await tools.search(query,count)
    parsed_response=tools.parse_events(results,query)

    response={
        "query":query,
        "total_results":parsed_response.total_results,
        "events_with_dates":[
            {
                "coin":event.coin_name,
                "title":event.event_title,
                "date":event.event_date.isoformat() if  event.event_date else None,
                "location":event.location,
                "description":event.description,
                "category":event.category.value,
                "source":str(event.source_url)
            }
            for event in parsed_response.events_with_dates
        ],
        "events_without_dates":[
            {
                "coin":event.coin_name,
                "title":event.event_title,
                "description":event.description,
                "category":event.category.value,
                "source":str(event.source_url)
            }
            for event in parsed_response.events_without_date
        ]
        
   }
    return json.dumps(response,indent=2)

if __name__=="__main__":
    if platform.system()=="windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    mcp.run(transport="http",host="127.0.0.1",port=5000)
            

        
    