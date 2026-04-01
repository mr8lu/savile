import pytest
from pathlib import Path
from starlette.testclient import TestClient
from starlette.applications import Starlette
from starlette.routing import Route
from mcp.server.sse import SseServerTransport
from savile.mcp.server import create_mcp_server

@pytest.fixture
def mock_vault(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "personas").mkdir()
    (vault / "frameworks").mkdir()
    
    # Create a persona
    persona_file = vault / "personas" / "realist.md"
    persona_file.write_text("You are a realist.")
    
    return vault

def test_sse_endpoint_exists(mock_vault):
    """Test that the SSE and messages endpoints are correctly set up and reachable."""
    from starlette.responses import Response
    from starlette.routing import Mount

    server = create_mcp_server(mock_vault)
    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await server.run(
                streams[0], streams[1], server.create_initialization_options()
            )
        return Response()

    app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages", app=sse.handle_post_message),
        ],
    )

    client = TestClient(app)
    
    # 1. Test SSE endpoint (GET /sse)
    # Note: TestClient with SSE can be tricky, but we can verify it doesn't 404
    with client.stream("GET", "/sse") as response:
        assert response.status_code == 200
        # We don't need to read the whole stream in a simple unit test
    
    # 2. Test messages endpoint (POST /messages)
    # It should return 400 or something if the body is invalid, but not 404
    response = client.post("/messages", json={})
    # Since we haven't properly initialized the SSE session, it might return error,
    # but we just want to verify it's routed.
    assert response.status_code != 404
