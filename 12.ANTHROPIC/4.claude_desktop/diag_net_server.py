from mcp.server.fastmcp import FastMCP

import asyncio, platform, socket, sys, logging

mcp = FastMCP("simple-net-diag-server")

logger = logging.getLogger("simple-net-diag-server")

@mcp.tool()
async def fetch_page(host: str, port: int=80, path:str="/", max_bytes: int=100_000) -> dict:
"""
    간단한 페이지 GET(HTTP)을 통해서 가져온 결과를 반환합니다.
    -path는 기본 '/'이며 원하는 경로를 추가할수도 있습니다.
    -max_ytes
"""
    from urllib.parse import 

async def ping_host(host: str, count: int=3, timeout_sec: int=3) -> str:
    """
    지정한 host 로 ping을 하여 결과를 반환합니다.
    - count: 1~5까지
    - timeout: 1~5초( 패킷 당 타임아웃)
    """

    host = (host or "").strip()
    if not host:
        raise ValueError("Host 를 입력하세요.")
    
    if platform.system() == "Windows":
        cmd = ['ping', '-n', str(count), '-w', str(timeout_sec*1000), host]
    else:
        cmd = ['ping', '-c', str(count), '-W', str(timeout_sec), host]
    
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    text = out or err

    if isinstance(text, bytes):
        text = out.decode("utf-8", "ignore")
        if platform.system() == "Windows":
            text = err.decode("utf-8", "ignore")

    logger.info(f"ping result: {text}")

    return text

if __name__ == "__main__":
    mcp.run(transport="stdio")