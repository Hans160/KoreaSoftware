# pip install mcp   , py312 환경에서 깔림
import mcp
from mcp.server.fastmcp import FastMCP
from mcp import ClientSession

from importlib.metadata import version
import inspect


print(f"MCP version: {version('mcp')}")

print("\nMCP 문서\n------------")
print(inspect.getdoc(FastMCP))

print(inspect.getdoc(FastMCP.sse_app))

print("\nMCP 세션 관리 문서\n-------------")
print(inspect.getdoc(ClientSession))