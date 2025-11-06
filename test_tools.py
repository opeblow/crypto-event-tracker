import asyncio
from tools import CryptoSearchTool,SearchConfig

async def test():
    print('Creating search config.')
    config=SearchConfig()
    print(f"API KEY loaded:{config.api_key[:10]}")

    print("Creating Search Tool")
    tool=CryptoSearchTool(config)
    print("Testing Search")

    results=await tool.search("Bitcoin events",5)

    print(f"Got {len(results)}results!")

    for i,result in enumerate (results,1):
        print(f"\n{i}.{result.title}")
        print(f"{result.url}")

    print("\n Parsing events")
    parsed=tool.parse_events(results,"Bitcoin events")

    print(f"Events with dates :{len(parsed.events_with_dates)}")
    print(f"Events without dates:{len(parsed.events_without_date)}")

if __name__=="__main__":
    asyncio.run(test())