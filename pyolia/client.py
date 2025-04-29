""" Python wrapper for the Veolia unofficial API """
import asyncio
import logging
from typing import Optional, List

import aiohttp
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://mywater.veolia.us"
LOGIN_URL = f"{BASE_URL}/user/login"


class BadCredentialsException(Exception):
    pass


class VeoliaClient:
    def __init__(self, username: str, password: str, session: Optional[aiohttp.ClientSession] = None):
        self.username = username
        self.password = password
        self.session = session or aiohttp.ClientSession()
        self.logged_in = False

    async def login(self):
        _LOGGER.debug("Fetching login page to retrieve form_build_id...")

        async with self.session.get(LOGIN_URL) as resp:
            if resp.status != 200:
                raise Exception("Failed to load login page")
            html = await resp.text()

        soup = BeautifulSoup(html, "html.parser")
        form_build_id_element = soup.find("input", {"name": "form_build_id"})
        if not form_build_id_element:
            raise Exception("form_build_id not found in login page")

        form_build_id = form_build_id_element.get("value")

        payload = {
            "name": self.username,
            "pass": self.password,
            "form_build_id": form_build_id,
            "form_id": "user_login_form",
            "op": "Log in"
        }

        _LOGGER.debug("Posting login form with credentials and form_build_id...")

        async with self.session.post(LOGIN_URL, data=payload) as post_resp:
            if post_resp.status != 200:
                raise Exception("Failed to POST login form")
            post_html = await post_resp.text()

        if "logout" not in post_html.lower():
            raise BadCredentialsException("Failed to login. Please check your credentials.")

        _LOGGER.info("Login successful!")
        self.logged_in = True

    async def get_consumption(self, month: int, year: int, day: Optional[int] = None) -> List[float]:
        if not self.logged_in:
            await self.login()

        # Adjust endpoint for actual US API if different
        if day is not None:
            # Example: hourly consumption endpoint
            url = f"{BASE_URL}/api/consumption/hourly?day={day}&month={month}&year={year}"
        else:
            # Example: daily/monthly consumption endpoint
            url = f"{BASE_URL}/api/consumption/monthly?month={month}&year={year}"

        _LOGGER.debug(f"Fetching consumption data from {url}")

        async with self.session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to fetch consumption data: HTTP {resp.status}")
            data = await resp.json()

        # Parse and normalize data here if needed
        consumption = data.get("consumption", [])
        _LOGGER.debug(f"Consumption data received: {consumption}")
        return consumption

    async def close(self):
        if not self.session.closed:
            await self.session.close()
