from mcp.server.fastmcp import FastMCP
import requests, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("xiaozhi_mcp")

mcp = FastMCP("WebSearch")

@mcp.tool()
def web_search(query: str) -> dict:
    '''
    Tìm kiếm trên web (DuckDuckGo) và trả về tóm tắt + liên quan.
    '''
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
        res = requests.get(url, timeout=10).json()
        abstract = res.get("AbstractText") or "Không có tóm tắt rõ ràng."
        related = []
        for t in res.get("RelatedTopics", [])[:3]:
            if isinstance(t, dict) and t.get("Text"):
                related.append(t.get("Text"))
        return {"summary": abstract, "related": related}
    except Exception as e:
        logger.error("web_search error: %s", e)
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("MCP server chạy...")
    mcp.run(transport="stdio")
