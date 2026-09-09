"""Thin asynchronous client for the AmberChest HTTP API."""

from __future__ import annotations

from typing import Any

from aiohttp import ClientError, ClientSession, ClientTimeout

from .const import ACCOUNTS_PATH, LOGIN_PATH, SCHEDULE_PATH, STATE_PATH

TIMEOUT = ClientTimeout(total=20)


class AmberChestError(Exception):
    """The server could not be reached or answered with an error."""


class AmberChestAuthError(AmberChestError):
    """The password was refused."""


class AmberChestLockedError(AmberChestError):
    """The configuration is still locked, so there is nothing to read."""


class AmberChestClient:
    """Talks to one AmberChest instance.

    Authentication has two shapes. An instance without a password lets
    everything through; one with a password hands out a session token in
    exchange for it. Those tokens do not survive a restart of the server, so
    every request retries once after logging in again.
    """

    def __init__(
        self,
        session: ClientSession,
        base_url: str,
        password: str | None,
        verify_ssl: bool = True,
    ) -> None:
        """Store the connection details; nothing is contacted yet."""
        self._session = session
        self._base_url = base_url.rstrip("/")
        self._password = password
        self._verify_ssl = verify_ssl
        self._token: str | None = None

    @property
    def base_url(self) -> str:
        """Return where this client points, for the device information."""
        return self._base_url

    async def _request(
        self, method: str, path: str, *, retry: bool = True, **kwargs: Any
    ) -> Any:
        headers = {"Authorization": f"Bearer {self._token}"} if self._token else {}
        try:
            response = await self._session.request(
                method,
                f"{self._base_url}{path}",
                headers=headers,
                ssl=self._verify_ssl,
                timeout=TIMEOUT,
                **kwargs,
            )
        except (ClientError, TimeoutError) as error:
            raise AmberChestError(str(error)) from error

        if response.status == 401:
            # Either the token expired or we never had one.
            if retry and self._password:
                await self.login()
                return await self._request(method, path, retry=False, **kwargs)
            raise AmberChestAuthError("Not authenticated")

        if response.status == 423:
            raise AmberChestLockedError("The configuration is locked")

        if response.status >= 400:
            raise AmberChestError(f"HTTP {response.status} for {path}")

        return await response.json()

    async def login(self) -> None:
        """Exchange the interface password for a session token."""
        if not self._password:
            return
        try:
            response = await self._session.post(
                f"{self._base_url}{LOGIN_PATH}",
                json={"password": self._password},
                ssl=self._verify_ssl,
                timeout=TIMEOUT,
            )
        except (ClientError, TimeoutError) as error:
            raise AmberChestError(str(error)) from error

        if response.status == 401:
            raise AmberChestAuthError("Wrong password")
        if response.status >= 400:
            raise AmberChestError(f"HTTP {response.status} while logging in")

        payload = await response.json()
        self._token = payload.get("token")

    async def state(self) -> dict[str, Any]:
        """Read whether the instance is set up, unlocked and how it authenticates."""
        return await self._request("GET", STATE_PATH)

    async def accounts(self) -> list[dict[str, Any]]:
        """Read one entry per mailbox, with the counters the sensors show."""
        return await self._request("GET", ACCOUNTS_PATH)

    async def schedule(self) -> dict[str, Any]:
        """Read the cron expression and the next run; empty outside the container."""
        try:
            return await self._request("GET", SCHEDULE_PATH)
        except AmberChestError:
            # Older servers do not know this endpoint yet.
            return {"expression": None, "nextRun": None}

    async def start_backup(self, account_id: str) -> None:
        """Start a backup; the server answers before it has finished."""
        # An empty JSON document, because the server insists on a body it can
        # parse and answers 415 without one.
        await self._request("POST", f"{ACCOUNTS_PATH}/{account_id}/sync", json={})

    async def cancel_backup(self, account_id: str) -> None:
        """Stop a running backup."""
        await self._request(
            "POST", f"{ACCOUNTS_PATH}/{account_id}/sync/cancel", json={}
        )
