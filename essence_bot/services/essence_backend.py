from typing import List

import aiohttp
from schemas.channel import ChannelAddResponse, ChannelResponse
from schemas.digest import AggregatedPostModel
from schemas.user import User
from services.base_api_service import BaseService


class EssenceBackendAPI(BaseService):
    async def get_user(self, user_id: str) -> User | None:
        url = f"{self.base_url}/user/"
        params = {"user_id": user_id}

        try:
            response_json = await self.get(url, params=params)
            return User(**response_json)
        except aiohttp.ClientResponseError as e:
            if e.status == 404 and e.message == "User not found":
                return None
            else:
                print(f"HTTP Error: {e.status} - {e.message}")
                raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    async def add_user(self, user_id: str, username: str) -> None:
        url = f"{self.base_url}/user/add"
        data = {"user_id": user_id, "username": username}

        try:
            await self.post(url, data=data)
        except aiohttp.ClientResponseError as e:
            print(f"HTTP Error: {e.status} - {e.message}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    async def subscribe_user(self, payment_id: str, user_id: str, days_cnt: int) -> None:
        url = f"{self.base_url}/subscription/activate"
        data = {"payment_id": payment_id, "user_id": user_id, "duration_days": days_cnt}

        try:
            await self.post(url, data=data)
        except aiohttp.ClientResponseError as e:
            print(f"HTTP Error: {e.status} - {e.message}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    async def add_channels(self, user_id: str, channel_links: List[str]) -> List[ChannelAddResponse]:
        url = f"{self.base_url}/channels/add"
        data = {"user_id": user_id, "channel_links": channel_links}

        try:
            results = await self.post(url, data=data)
            channels = [ChannelAddResponse(**channel) for channel in results]
            return channels
        except aiohttp.ClientResponseError as e:
            print(f"HTTP Error: {e.status} - {e.message}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    async def get_user_channels(self, user_id: str) -> List[ChannelResponse]:
        url = f"{self.base_url}/channels/"
        params = {"user_id": user_id}

        try:
            response_json = await self.get(url, params=params)
            return [ChannelResponse(**resp) for resp in response_json]
        except aiohttp.ClientResponseError as e:
            print(f"HTTP Error: {e.status} - {e.message}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    async def remove_channels(self, user_id: str, channel_links: List[str]) -> None:
        url = f"{self.base_url}/channels/remove"
        data = {"user_id": user_id, "channel_links": channel_links}

        try:
            await self.post(url, data=data)
        except aiohttp.ClientResponseError as e:
            print(f"HTTP Error: {e.status} - {e.message}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    async def set_digest_params(self, user_id: str, frequency: str, hour: int) -> None:
        url = f"{self.base_url}/user/change_digest_params"
        data = {"user_id": user_id, "digest_freq": frequency, "digest_time": hour}

        try:
            await self.post(url, data=data)
        except aiohttp.ClientResponseError as e:
            print(f"HTTP Error: {e.status} - {e.message}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    async def get_expiring_subscriptions(self, shift_days: int) -> List[str]:
        url = f"{self.base_url}/subscription/expiring_subs/{shift_days}"

        try:
            response_json = await self.get(url)
            return [user["user_id"] for user in response_json]
        except aiohttp.ClientResponseError as e:
            print(f"HTTP Error: {e.status} - {e.message}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    async def deactivate_subscription(self, user_id: str) -> None:
        url = f"{self.base_url}/subscription/deactivate"
        data = {"user_id": user_id}

        try:
            await self.post(url, data=data)
            print(f"Deactivated subscription for user {user_id}.")
        except aiohttp.ClientResponseError as e:
            print(f"HTTP Error during deactivation for user {user_id}: {e.status} - {e.message}")
            raise
        except Exception as e:
            print(f"An error occurred while deactivating subscription for user {user_id}: {e}")
            raise

    async def get_digest(self, user_id: str) -> List[AggregatedPostModel] | None:
        url = f"{self.base_url}/digest/"
        params = {"user_id": user_id}

        try:
            response_json = await self.get(url, params=params)
            return [AggregatedPostModel(**post) for post in response_json]
        except aiohttp.ClientResponseError as e:
            if e.status == 404 and e.message == "User not found":
                return None
            else:
                print(f"HTTP Error: {e.status} - {e.message}")
                raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    async def ask_question(self, user_id: str, clusters: List[int], digest_text: str, query_history: List[str]) -> str:
        url = f"{self.base_url}/digest/ask"
        data = {"user_id": user_id, "clusters": clusters, "digest_text": digest_text, "query_history": query_history}

        try:
            response = await self.post(url, data=data)
            return response
        except aiohttp.ClientResponseError as e:
            print(f"HTTP Error: {e.status} - {e.message}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
