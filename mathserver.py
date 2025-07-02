from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """ _summary_
    Add two numbers
    """
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """ _summary_
    Subtract two numbers
    """
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """ _summary_
    Multiply two numbers
    """
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
