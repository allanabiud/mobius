import os
import time
from dotenv import load_dotenv

from mokkari.session import Session
from mokkari.sqlite_cache import SqliteCache
from mokkari.exceptions import RateLimitError, ApiError

load_dotenv()


class MetronService:
    def __init__(self, cache_path="metron_cache.db"):
        username = os.getenv("METRON_USERNAME")
        password = os.getenv("METRON_PASSWORD")

        if not username or not password:
            raise RuntimeError(
                "METRON_USERNAME and METRON_PASSWORD must be set in the environment."
            )

        cache = SqliteCache(cache_path)

        self.session = Session(
            username=username,
            passwd=password,
            cache=cache,
            user_agent="Mobius/1.0",
        )

    def fetch_with_retry(self, func, *args, **kwargs):
        """
        Generic wrapper for all Metron API calls.
        Handles rate limits and retries safely.
        """
        while True:
            try:
                return func(*args, **kwargs)

            except RateLimitError as e:
                # Mokkari tells you exactly how long to wait
                wait = e.retry_after or 60

                if "per day" in str(e).lower():
                    # Daily limit should usually abort
                    raise RuntimeError(
                        f"Daily Metron API limit reached. Retry in {wait} seconds."
                    ) from e

                # Minute limit: sleep and retry
                time.sleep(wait)

            except ApiError:
                raise
