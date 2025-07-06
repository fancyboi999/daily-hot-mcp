from fastmcp import FastMCP
from daily_hot_mcp.utils.logger import logger
from daily_hot_mcp.tools import all_tools

# 重命名变量，使其符合 mcp dev 命令的预期
server = FastMCP(name = "daily-hot-mcp")

for tool in all_tools:
    server.add_tool(tool)
    logger.info(f"Registered tool: {tool.name}")

def run_http(host: str, port: int, path: str, log_level: str):
    """Run Daily Hot MCP server in HTTP mode."""
    try:
        logger.info(f"Starting Daily Hot MCP server with HTTP transport (http://{host}:{port}{path})")
        server.run(
            transport="http",
            host=host,
            port=port,
            path=path,
            log_level=log_level
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")

def main():
    run_http("0.0.0.0", 8000, "/mcp", "INFO")

if __name__ == "__main__":
    main()