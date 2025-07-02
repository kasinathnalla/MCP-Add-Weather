import logging
logging.getLogger().setLevel(logging.ERROR)

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """ _summary_
    Get the weather for a location
    """
    print(f"Getting weather for {location}")
    return f"The weather in {location} is rainy all the time"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")