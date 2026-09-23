import asyncio

import httpx


class CatalogClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=2.0
        )

    async def get_quote(
            self,
            catalog_url: str,
            quote_id: str
    ):
        try:

            for _ in range(3):

                response = await self.client.get(
                    f"{catalog_url}/quote/{quote_id}"
                )

                if response.status_code != 503:
                    return response

                retry_after = response.headers.get(
                    "Retry-After",
                    "1"
                )

                await asyncio.sleep(
                    int(retry_after)
                )

            return response

        except httpx.TimeoutException:
            return None

        except httpx.ConnectError:
            return None
        
        except Exception:
            return None