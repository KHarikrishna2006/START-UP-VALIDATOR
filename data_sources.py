from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
from urllib.parse import urlencode
from urllib.request import urlopen
import json


@dataclass
class WebSignals:
    trend_signal: float
    competition_signal: float
    market_signal: float
    sources: Dict[str, str]


def _safe_get_json(url: str, params: dict, timeout: int = 8) -> dict:
    full_url = f"{url}?{urlencode(params)}"
    with urlopen(full_url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_web_signals(query: str) -> WebSignals:
    q = query.strip()
    if not q:
        return WebSignals(0.0, 0.0, 0.0, {})

    sources: Dict[str, str] = {}

    try:
        hn_data = _safe_get_json(
            "https://hn.algolia.com/api/v1/search",
            {"query": q, "tags": "story", "hitsPerPage": 20},
        )
        hn_hits = float(hn_data.get("nbHits", 0))
        trend_signal = min(30.0, (hn_hits / 5000.0) * 30.0)
        sources["hackernews"] = f"{int(hn_hits)} related stories"
    except Exception:
        trend_signal = 0.0
        sources["hackernews"] = "unavailable"

    try:
        github_data = _safe_get_json(
            "https://api.github.com/search/repositories",
            {"q": q, "per_page": 1},
        )
        repo_count = float(github_data.get("total_count", 0))
        competition_signal = min(30.0, (repo_count / 100000.0) * 30.0)
        sources["github"] = f"{int(repo_count)} related repositories"
    except Exception:
        competition_signal = 0.0
        sources["github"] = "unavailable"

    try:
        ddg_data = _safe_get_json(
            "https://api.duckduckgo.com/",
            {"q": q, "format": "json", "no_redirect": 1, "no_html": 1},
        )
        related_topics = ddg_data.get("RelatedTopics", [])
        breadth = float(len(related_topics))
        market_signal = min(30.0, (breadth / 15.0) * 30.0)
        sources["duckduckgo"] = f"{int(breadth)} related topics"
    except Exception:
        market_signal = 0.0
        sources["duckduckgo"] = "unavailable"

    return WebSignals(
        trend_signal=round(trend_signal, 2),
        competition_signal=round(competition_signal, 2),
        market_signal=round(market_signal, 2),
        sources=sources,
    )
