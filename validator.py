from __future__ import annotations

from dataclasses import dataclass

from data_sources import fetch_web_signals


@dataclass
class ScoreWeights:
    market: float = 0.35
    competition: float = 0.30
    trend: float = 0.35


HIGH_VALUE_KEYWORDS = {
    "ai",
    "automation",
    "saas",
    "health",
    "fintech",
    "edtech",
    "platform",
    "b2b",
    "analytics",
    "cloud",
}
TREND_KEYWORDS = {
    "ai",
    "sustainable",
    "green",
    "creator",
    "remote",
    "cybersecurity",
    "personalization",
    "no-code",
}
COMPETITIVE_KEYWORDS = {"ecommerce", "food delivery", "social media", "rideshare", "marketplace"}


def _normalize(score: float) -> float:
    return max(0.0, min(100.0, round(score, 2)))


def validate_idea(title: str, description: str) -> dict:
    text = f"{title} {description}".lower()
    words = set(text.replace(",", " ").replace(".", " ").split())

    market_signal = len(words & HIGH_VALUE_KEYWORDS)
    trend_signal = len(words & TREND_KEYWORDS)
    competition_signal = len(words & COMPETITIVE_KEYWORDS)

    heuristic_market = _normalize(45 + market_signal * 10)
    heuristic_trend = _normalize(40 + trend_signal * 12)
    heuristic_competition = _normalize(70 - competition_signal * 12)

    web_signals = fetch_web_signals(f"{title} {description[:140]}")

    market_score = _normalize(heuristic_market * 0.75 + web_signals.market_signal * 0.83)
    trend_score = _normalize(heuristic_trend * 0.75 + web_signals.trend_signal * 0.83)
    competition_score = _normalize(heuristic_competition * 0.75 + (30 - web_signals.competition_signal) * 0.83)

    weights = ScoreWeights()
    feasibility_score = _normalize(
        (market_score * weights.market)
        + (competition_score * weights.competition)
        + (trend_score * weights.trend)
    )

    swot = {
        "strengths": [
            "Idea shows clear value proposition for a target user segment.",
            f"Market attractiveness score is {market_score} / 100.",
        ],
        "weaknesses": [
            "Needs clearer go-to-market strategy and distribution channels.",
            "Revenue assumptions should be validated with customer interviews.",
        ],
        "opportunities": [
            f"Trend alignment score is {trend_score} / 100, indicating growth potential.",
            "Potential partnerships with incubators, colleges, and startup communities.",
        ],
        "threats": [
            f"Competition resilience score is {competition_score} / 100.",
            "Fast-moving competitors can replicate features quickly.",
        ],
    }

    improvement_tips = [
        "Run 10–15 customer interviews to validate the core pain point.",
        "Build a landing page and test demand with a waitlist campaign.",
        "Define one beachhead segment before scaling to adjacent markets.",
        "Track CAC, conversion rate, and retention for feasibility re-scoring.",
    ]

    return {
        "market_score": market_score,
        "competition_score": competition_score,
        "trend_score": trend_score,
        "swot": swot,
        "feasibility_score": feasibility_score,
        "improvement_tips": improvement_tips,
        "data_sources": web_signals.sources,
    }
