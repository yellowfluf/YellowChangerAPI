import asyncio
import httpx
from httpx import Timeout, HTTPError


class HTTPClient:

    def __init__(self):
        """
        Initialization of an HTTP client using httpx.AsyncClient.

        Creates an asynchronous session for executing HTTP requests.
        """
        self.timeout = Timeout(
            connect=30.0,  # Connection establishment timeout
            read=30.0,     # Response reading timeout
            write=30.0,    # Request sending timeout
            pool=30.0      # Timeout for obtaining a connection from the pool
        )
        self.session = httpx.AsyncClient(timeout=self.timeout)

    async def __aenter__(self):
        """
        Initialize session when entering context.
        """
        self.session = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Close session when exiting context.
        """
        await self.session.aclose()

    async def get(
        self,
        url: str,
        headers: dict = None,
        params: dict = None,
        retries: int = 3,
        base_delay: int = 5,
        timeout: Timeout = None
    ):
        """
        Execute a GET request with retry support.

        :param url: URL to execute the request.
        :param headers: Request headers.
        :param params: Parameters in JSON format for the query string.
        :param retries: Number of attempts.
        :param base_delay: Base delay between attempts.
        :param timeout: Custom timeouts for the request.
        :return: Response in JSON format.
        :raises httpx.HTTPStatusError: In case of an HTTP status error.
        :raises Exception: In case of unexpected errors.
        """
        for attempt in range(1, retries + 1):
            try:
                response = await self.session.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=timeout or self.timeout
                )
                if response.is_error:
                    error = HTTPError(response.request)
                    error.status_code = response.status_code
                    error.text = response.text
                    error.reason_phrase = response.reason_phrase
                    raise error
                return response.json()
            except httpx.HTTPStatusError:
                if attempt == retries:
                    raise
                await asyncio.sleep(base_delay * attempt)
            except Exception:
                if attempt == retries:
                    raise
                await asyncio.sleep(base_delay * attempt)

    async def get_json(
        self,
        url: str,
        headers: dict = None,
        json_body: dict = None,
        retries: int = 3,
        base_delay: int = 5,
        timeout: Timeout = None
    ) -> dict:
        """
        Execute a GET request with retry support, where the body is passed in JSON format.

        :param url: URL to execute the request.
        :param headers: Request headers.
        :param json_body: Request body in JSON format (not a query string).
        :param retries: Number of attempts for failed requests.
        :param base_delay: Base delay (in seconds) between retry attempts.
        :param timeout: Custom timeouts for the request.
        :return: Server response in JSON format (dict).
        :raises httpx.HTTPStatusError: If the server returned an unsuccessful HTTP status and retries are exhausted.
        :raises Exception: In case of unexpected errors.
        """
        for attempt in range(1, retries + 1):
            try:
                response = await self.session.request(
                    method="GET",
                    url=url,
                    headers=headers,
                    json=json_body,
                    timeout=timeout or self.timeout
                )
                if response.is_error:
                    error = HTTPError(response.request)
                    error.status_code = response.status_code
                    error.text = response.text
                    error.reason_phrase = response.reason_phrase
                    raise error
                response.raise_for_status()

                return response.json()

            except httpx.HTTPStatusError:
                if attempt == retries:
                    raise
                else:
                    await asyncio.sleep(base_delay * attempt)

            except Exception:
                if attempt == retries:
                    raise
                else:
                    await asyncio.sleep(base_delay * attempt)

    async def post(
        self,
        url: str,
        json: dict = None,
        headers: dict = None,
        retries: int = 3,
        base_delay: int = 5,
        timeout: Timeout = None
    ):
        """
        Execute a POST request with retry support.

        :param url: URL to execute the request.
        :param json: Data sent in the request body.
        :param headers: Request headers.
        :param retries: Number of attempts.
        :param base_delay: Base delay between attempts.
        :param timeout: Custom timeouts for the request.
        :return: Response in JSON format.
        :raises httpx.HTTPStatusError: In case of an HTTP status error.
        :raises Exception: In case of unexpected errors.
        """
        for attempt in range(1, retries + 1):
            try:
                response = await self.session.request(
                    method="POST",
                    url=url,
                    headers=headers,
                    json=json,
                    timeout=timeout or self.timeout
                )
                if response.is_error:
                    error = HTTPError(response.request)
                    error.status_code = response.status_code
                    error.text = response.text
                    error.reason_phrase = response.reason_phrase
                    raise error
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError:
                if attempt == retries:
                    raise
                await asyncio.sleep(base_delay * attempt)
            except Exception:
                if attempt == retries:
                    raise
                await asyncio.sleep(base_delay * attempt)

    async def close(self):
        """
        Close the HTTP session.

        Terminates the HTTP session and closes the connection.
        """
        await self.session.aclose()
