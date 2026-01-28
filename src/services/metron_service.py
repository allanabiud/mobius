import os
import datetime
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
                wait = e.retry_after or 60

                if "per day" in str(e).lower():
                    # Daily limit should usually abort
                    raise RuntimeError(
                        f"Daily Metron API limit reached. Retry in {wait} seconds."
                    ) from e

                time.sleep(wait)

            except ApiError:
                raise

    def get_weekly_releases_stats(self):
        """
        Calculates the current week's dates and returns counts for
        New Comics, Debut Issues (#1s), and Pull List matches.
        """
        target_date = datetime.date.today()
        sunday = target_date - datetime.timedelta(days=(target_date.weekday() + 1) % 7)
        saturday = sunday + datetime.timedelta(days=6)

        all_week_issues = self.fetch_with_retry(
            self.session.issues_list,
            params={
                "store_date_range_after": sunday.isoformat(),
                "store_date_range_before": saturday.isoformat(),
            },
        )

        if not all_week_issues:
            return {"total": 0, "debuts": 0, "pulls": 0}

        missing_series = self.session.collection_missing_series()
        missing_names = {s.name for s in missing_series}

        total_count = len(all_week_issues)
        debut_count = len([i for i in all_week_issues if i.number == "1"])
        pull_count = len([i for i in all_week_issues if i.series.name in missing_names])

        return {"total": total_count, "debuts": debut_count, "pulls": pull_count}

    def search_series(self, query_text: str):
        """Fetches series list and attempts to find a cover image for each."""
        raw_results = self.fetch_with_retry(
            self.session.series_list, params={"name": query_text}
        )

        processed_results = []
        for series in raw_results:
            first_issue = self.fetch_with_retry(
                self.session.issues_list, params={"series_id": series.id, "number": 1}
            )
            img = first_issue[0].image if first_issue else None
            processed_results.append({"series": series, "image": img})

        return processed_results

    def search_issues(self, query_text: str):
        """Fetches issues based on series name."""
        return self.fetch_with_retry(
            self.session.issues_list, params={"series_name": query_text}
        )

    def get_series_details(self, series_id: int):
        """
        Fetches full series metadata and all associated issues.
        Returns a tuple of (series_object, issues_list).
        """
        series = self.fetch_with_retry(self.session.series, series_id)
        issues = self.fetch_with_retry(
            self.session.issues_list, params={"series_id": series_id}
        )
        return series, (issues if issues else [])
