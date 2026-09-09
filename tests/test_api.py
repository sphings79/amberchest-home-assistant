"""Tests for the HTTP client, against a small server that plays AmberChest."""

from __future__ import annotations

from aiohttp import ClientSession, web
import pytest

TOKEN = "session-token"


@pytest.fixture
async def server(aiohttp_server):
    """Serve what an instance with a password would answer."""
    state = {"logins": 0, "accepted": TOKEN}

    async def login(request: web.Request) -> web.Response:
        body = await request.json()
        if body.get("password") != "secret":
            return web.json_response({"message": "Wrong password"}, status=401)
        state["logins"] += 1
        return web.json_response({"token": state["accepted"]})

    def authorised(request: web.Request) -> bool:
        return request.headers.get("Authorization") == f"Bearer {state['accepted']}"

    async def accounts(request: web.Request) -> web.Response:
        if not authorised(request):
            return web.json_response({"message": "Not authenticated"}, status=401)
        return web.json_response([{"account": {"id": "a1", "name": "Privat"}}])

    async def schedule(request: web.Request) -> web.Response:
        return web.json_response({"message": "Not found"}, status=404)

    async def state_route(request: web.Request) -> web.Response:
        return web.json_response({"initialized": True, "authMode": "password"})

    app = web.Application()
    app["state"] = state
    app.router.add_post("/api/login", login)
    app.router.add_get("/api/accounts", accounts)
    app.router.add_get("/api/schedule", schedule)
    app.router.add_get("/api/state", state_route)
    return await aiohttp_server(app)


async def client_for(api, server, password: str | None = "secret"):
    session = ClientSession()
    return api.AmberChestClient(session, str(server.make_url("")), password)


async def test_login_stores_the_token(api, server) -> None:
    client = await client_for(api, server)
    await client.login()
    assert await client.accounts() == [{"account": {"id": "a1", "name": "Privat"}}]


async def test_wrong_password_is_reported(api, server) -> None:
    client = await client_for(api, server, "nope")
    with pytest.raises(api.AmberChestAuthError):
        await client.login()


async def test_a_dropped_session_logs_in_again(api, server) -> None:
    client = await client_for(api, server)
    await client.login()
    assert server.app["state"]["logins"] == 1

    # The server restarted and no longer knows the old token.
    server.app["state"]["accepted"] = "a-new-token"
    await client.accounts()
    assert server.app["state"]["logins"] == 2


async def test_without_a_password_a_401_is_final(api, server) -> None:
    client = await client_for(api, server, None)
    with pytest.raises(api.AmberChestAuthError):
        await client.accounts()


async def test_an_old_server_without_the_schedule_route(api, server) -> None:
    client = await client_for(api, server)
    await client.login()
    assert await client.schedule() == {"expression": None, "nextRun": None}


async def test_a_server_that_is_not_there(api, unused_tcp_port) -> None:
    session = ClientSession()
    client = api.AmberChestClient(
        session, f"http://127.0.0.1:{unused_tcp_port}", None
    )
    with pytest.raises(api.AmberChestError):
        await client.state()
    await session.close()
