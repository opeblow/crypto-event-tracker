import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params=StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    print("Connecting to server ")

    async with stdio_client(server_params) as (read,write):
        print("Server subprocess started")

        session=ClientSession(read,write)
        print("Initializing session")

        await session.initialize()
        print("Session initialized!")

        tools=await session.list_tools()
        print(f"Tools:{[t.name for t in tools.tools]}")

        print("\n Testing search_ctypto_events")
        result=await session.call_tool(
            "search_crypto_events",
            {"query":"Bitcoin events","count":3}
        )

        print(f"\n Result:\n {result.content[0].text[:500]}")
        print("\n ALL TESTS PASSED!")

if __name__=="__main__":
    asyncio.run(main())