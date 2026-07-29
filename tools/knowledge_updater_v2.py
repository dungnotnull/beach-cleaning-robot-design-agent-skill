"""
knowledge_updater_v2.py — Enhanced Knowledge Pipeline
Skill 235: beach-cleaning-robot-design v2.0.0

Production-grade crawl pipeline with:
- Structured logging
- Better error handling and recovery
- Progress tracking and metrics
- Configurable rate limiting
- Deduplication and scoring
- Dry-run mode
- Multiple source support

Dependencies:
    pip install requests feedparser python-dateutil

Usage:
    python tools/knowledge_updater_v2.py [--dry-run] [--news-only] [--keywords ...]
"""

import argparse
import hashlib
import json
import logging
import math
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    from logger import StructuredLogger, LogLevel
    STRUCTURED_LOGGING = True
except ImportError:
    STRUCTURED_LOGGING = False
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

try:
    import requests
except ImportError:
    requests = None

try:
    import feedparser
except ImportError:
    feedparser = None


# ==================== CONFIGURATION ====================

KNOWLEDGE_CONFIG = {
    "domain": "Beach-Cleaning Robotics & Coastal Engineering",
    "keywords": [
        "beach cleaning robot",
        "coverage path planning robot",
        "robot sand locomotion",
        "robot debris sensing vision LiDAR",
        "robot battery autonomy beach",
        "coastal robot corrosion reliability"
    ],
    "arxiv_categories": [
        "cs.RO",  # Robotics
        "cs.CV",  # Computer Vision
        "eess.SP"  # Signal Processing
    ],
    "arxiv_base": "https://export.arxiv.org/api/query",
    "semantic_scholar_base": "https://api.semanticscholar.org/graph/v1/paper/search",
    "rss_feeds": [
        # Add relevant RSS feeds for coastal engineering and robotics
    ],
    "authoritative_docs": [
        "Journal of Field Robotics — Wiley",
        "IEEE Transactions on Robotics",
        "Ocean Engineering — Elsevier",
        "Marine Pollution Bulletin — Elsevier",
        "Robotics and Autonomous Systems — Elsevier",
        "Sensors (MDPI)"
    ],
    "scoring_weights": {
        "recency": 0.4,
        "keyword_relevance": 0.4,
        "citation_count": 0.2
    },
    "max_results_per_source": 10,
    "max_new_entries_per_run": 20,
    "rate_limit_delay": 1.0,  # seconds between requests
    "request_timeout": 30,  # seconds
    "max_retries": 3
}

BRAIN_PATH = Path(__file__).parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"
LOG_DIR = Path(__file__).parent.parent / "logs"


# ==================== DATA STRUCTURES ====================

class SourceType(Enum):
    """Types of knowledge sources."""
    ARXIV = "arxiv"
    SEMANTIC_SCHOLAR = "semantic_scholar"
    RSS = "rss"
    MANUAL = "manual"


@dataclass
class KnowledgeEntry:
    """A knowledge base entry."""
    title: str
    authors: List[str]
    year: int
    venue: str
    doi_or_url: str
    abstract: str
    published_date: Optional[datetime]
    citation_count: int
    source: SourceType
    relevance_score: float = 0.0
    tier: int = 4  # Default to Tier 4

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "venue": self.venue,
            "doi_or_url": self.doi_or_url,
            "abstract": self.abstract,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "citation_count": self.citation_count,
            "source": self.source.value,
            "relevance_score": self.relevance_score,
            "tier": self.tier
        }


@dataclass
class CrawlMetrics:
    """Metrics for crawl operations."""
    entries_fetched: int = 0
    entries_new: int = 0
    entries_skipped: int = 0
    entries_failed: int = 0
    sources_attempted: int = 0
    sources_succeeded: int = 0
    duration_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "entries_fetched": self.entries_fetched,
            "entries_new": self.entries_new,
            "entries_skipped": self.entries_skipped,
            "entries_failed": self.entries_failed,
            "sources_attempted": self.sources_attempted,
            "sources_succeeded": self.sources_succeeded,
            "duration_seconds": self.duration_seconds
        }


# ==================== LOGGER SETUP ====================

if STRUCTURED_LOGGING:
    logger = StructuredLogger("knowledge_updater", log_dir=LOG_DIR)
else:
    logger = logging.getLogger(__name__)


# ==================== CORE FUNCTIONS ====================

def fetch_with_retry(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    max_retries: int = None,
    base_delay: float = 2.0,
    timeout: int = None
) -> Optional[Any]:
    """
    Fetch URL with retry logic and exponential backoff.

    Returns:
        Response object or None if all retries fail
    """
    if requests is None:
        logger.error("requests library not available")
        return None

    max_retries = max_retries or KNOWLEDGE_CONFIG["max_retries"]
    timeout = timeout or KNOWLEDGE_CONFIG["request_timeout"]

    for attempt in range(max_retries):
        try:
            if attempt > 0:
                delay = base_delay * (2 ** attempt)
                logger.warning(f"Retry {attempt + 1}/{max_retries} after {delay}s delay")
                time.sleep(delay)

            resp = requests.get(
                url,
                params=params or {},
                timeout=timeout
            )

            # Handle rate limiting
            if resp.status_code == 429:
                wait_time = int(resp.headers.get("Retry-After", 60))
                logger.warning(f"Rate limited. Waiting {wait_time}s")
                time.sleep(wait_time)
                continue

            # Handle server errors
            if resp.status_code >= 500:
                if attempt < max_retries - 1:
                    logger.warning(f"Server error {resp.status_code}, retrying...")
                    continue
                return None

            resp.raise_for_status()
            return resp

        except requests.exceptions.Timeout:
            logger.error(f"Request timeout on attempt {attempt + 1}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed on attempt {attempt + 1}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")

    logger.error(f"All {max_retries} retries failed")
    return None


def compute_hash(identifier: str) -> str:
    """Compute SHA256 hash of identifier."""
    return hashlib.sha256(identifier.strip().lower().encode()).hexdigest()


def load_existing_hashes() -> Set[str]:
    """Load existing DOI/URL hashes from knowledge base."""
    if not BRAIN_PATH.exists():
        logger.warning(f"Knowledge base not found: {BRAIN_PATH}")
        return set()

    try:
        content = BRAIN_PATH.read_text(encoding="utf-8")
        hashes = set()
        for match in re.finditer(r"\*\*DOI/URL:\*\*\s*(\S+)", content):
            hashes.add(compute_hash(match.group(1)))
        logger.info(f"Loaded {len(hashes)} existing hashes")
        return hashes
    except Exception as e:
        logger.error(f"Failed to load existing hashes: {e}")
        return set()


def score_entry(entry: KnowledgeEntry, keywords: List[str], now: datetime) -> float:
    """
    Score a knowledge entry for relevance.

    Returns:
        Score from 0-10
    """
    try:
        # Recency score (0-1)
        recency = 0.0
        if entry.published_date:
            days_old = (now - entry.published_date).days
            recency = max(0.0, 1.0 - (days_old / 730.0))  # 2-year decay

        # Keyword relevance score (0-1)
        text = (
            (entry.title or "") + " " +
            (entry.abstract or "") + " " +
            (entry.venue or "")
        ).lower()

        keyword_hits = sum(1 for kw in keywords if kw.lower() in text)
        relevance = min(keyword_hits / max(len(keywords), 1), 1.0)

        # Citation score (0-1)
        cit_score = min(math.log1p(entry.citation_count) / math.log1p(1000), 1.0)

        # Weighted composite score
        weights = KNOWLEDGE_CONFIG["scoring_weights"]
        composite = (
            recency * weights["recency"] +
            relevance * weights["keyword_relevance"] +
            cit_score * weights["citation_count"]
        )

        return round(composite * 10.0, 2)

    except Exception as e:
        logger.error(f"Failed to score entry: {e}")
        return 0.0


def determine_tier(entry: KnowledgeEntry) -> int:
    """
    Determine evidence tier for an entry.

    Tier 1: Systematic review, meta-analysis, official standards
    Tier 2: Peer-reviewed academic paper
    Tier 3: Industry report, professional guideline
    Tier 4: News, blog, vendor material
    """
    venue_lower = (entry.venue or "").lower()

    # Tier 1 indicators
    tier1_keywords = ["systematic review", "meta-analysis", "standard", "guideline"]
    if any(kw in venue_lower for kw in tier1_keywords):
        return 1

    # Tier 2 indicators (peer-reviewed journals)
    tier2_venues = [
        "journal of field robotics",
        "ieee transactions",
        "ocean engineering",
        "marine pollution bulletin",
        "robotics and autonomous systems",
        "sensors",
        "arxiv"
    ]
    if any(venue in venue_lower for venue in tier2_venues):
        return 2

    # Tier 3 indicators (industry reports)
    if "report" in venue_lower or "industry" in venue_lower:
        return 3

    # Default Tier 4
    return 4


# ==================== SOURCE FETCHERS ====================

def fetch_arxiv(keywords: List[str], metrics: CrawlMetrics) -> List[KnowledgeEntry]:
    """Fetch entries from ArXiv."""
    if requests is None or not KNOWLEDGE_CONFIG["arxiv_categories"]:
        logger.warning("ArXiv fetcher not available")
        return []

    metrics.sources_attempted += 1
    logger.info("Fetching from ArXiv...")

    try:
        cats = KNOWLEDGE_CONFIG["arxiv_categories"]
        query = "(" + " OR ".join(f"cat:{c}" for c in cats) + ") AND (" + " OR ".join(f'"{k}"' for k in keywords[:5]) + ")"

        resp = fetch_with_retry(
            KNOWLEDGE_CONFIG["arxiv_base"],
            params={
                "search_query": query,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "max_results": KNOWLEDGE_CONFIG["max_results_per_source"]
            }
        )

        if resp is None:
            logger.warning("ArXiv fetch failed")
            return []

        import xml.etree.ElementTree as ET
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(resp.content)

        entries = []
        for entry_elem in root.findall("atom:entry", ns):
            try:
                title_elem = entry_elem.find("atom:title", ns)
                summary_elem = entry_elem.find("atom:summary", ns)
                id_elem = entry_elem.find("atom:id", ns)
                published_elem = entry_elem.find("atom:published", ns)

                if title_elem is None or id_elem is None:
                    continue

                title = (title_elem.text or "").strip().replace("\n", " ")
                url = (id_elem.text or "").strip()
                if not title or not url:
                    continue

                # Parse publication date
                pub_date = None
                if published_elem is not None and published_elem.text:
                    try:
                        from dateutil import parser as date_parser
                        pub_date = date_parser.parse(published_elem.text).replace(tzinfo=None)
                    except Exception:
                        pub_date = None

                # Extract authors
                authors = [
                    a.find("atom:name", ns).text
                    for a in entry_elem.findall("atom:author", ns)
                    if a.find("atom:name", ns) is not None
                ][:3]

                entry = KnowledgeEntry(
                    title=title,
                    authors=authors,
                    year=pub_date.year if pub_date else datetime.now().year,
                    venue="ArXiv",
                    doi_or_url=url,
                    abstract=(summary_elem.text or "")[:300] if summary_elem is not None else "",
                    published_date=pub_date,
                    citation_count=0,
                    source=SourceType.ARXIV
                )
                entry.tier = determine_tier(entry)
                entries.append(entry)

            except Exception as e:
                logger.debug(f"Failed to parse ArXiv entry: {e}")

        logger.info(f"ArXiv: fetched {len(entries)} entries")
        metrics.sources_succeeded += 1
        time.sleep(KNOWLEDGE_CONFIG["rate_limit_delay"])
        return entries

    except Exception as e:
        logger.error(f"ArXiv fetch error: {e}")
        return []


def fetch_semantic_scholar(keywords: List[str], metrics: CrawlMetrics) -> List[KnowledgeEntry]:
    """Fetch entries from Semantic Scholar."""
    if requests is None:
        logger.warning("Semantic Scholar fetcher not available")
        return []

    metrics.sources_attempted += 1
    logger.info("Fetching from Semantic Scholar...")

    try:
        resp = fetch_with_retry(
            KNOWLEDGE_CONFIG["semantic_scholar_base"],
            params={
                "query": " ".join(keywords[:4]),
                "fields": "title,authors,year,venue,externalIds,abstract,citationCount",
                "limit": KNOWLEDGE_CONFIG["max_results_per_source"]
            }
        )

        if resp is None:
            logger.warning("Semantic Scholar fetch failed")
            return []

        data = resp.json()
        entries = []

        for paper in data.get("data", []):
            try:
                title = paper.get("title", "")
                if not title:
                    continue

                year = paper.get("year") or datetime.now().year
                ext_ids = paper.get("externalIds", {})

                # Prioritize DOI
                doi = ext_ids.get("DOI", "")
                if not doi and ext_ids.get("ArXiv"):
                    doi = f"https://arxiv.org/abs/{ext_ids['ArXiv']}"
                if not doi:
                    doi = f"https://www.semanticscholar.org/paper/{paper.get('paperId', '')}"

                entry = KnowledgeEntry(
                    title=title,
                    authors=[a.get("name", "") for a in paper.get("authors", [])[:3]],
                    year=year,
                    venue=paper.get("venue") or "Unknown",
                    doi_or_url=doi,
                    abstract=(paper.get("abstract") or "")[:300],
                    published_date=datetime(year, 1, 1),
                    citation_count=paper.get("citationCount", 0),
                    source=SourceType.SEMANTIC_SCHOLAR
                )
                entry.tier = determine_tier(entry)
                entries.append(entry)

            except Exception as e:
                logger.debug(f"Failed to parse Semantic Scholar entry: {e}")

        logger.info(f"Semantic Scholar: fetched {len(entries)} entries")
        metrics.sources_succeeded += 1
        time.sleep(KNOWLEDGE_CONFIG["rate_limit_delay"])
        return entries

    except Exception as e:
        logger.error(f"Semantic Scholar fetch error: {e}")
        return []


def fetch_rss(metrics: CrawlMetrics) -> List[KnowledgeEntry]:
    """Fetch entries from RSS feeds."""
    if feedparser is None or not KNOWLEDGE_CONFIG["rss_feeds"]:
        logger.warning("RSS fetcher not available")
        return []

    metrics.sources_attempted += 1
    logger.info("Fetching from RSS feeds...")

    entries = []

    for feed_url in KNOWLEDGE_CONFIG["rss_feeds"]:
        try:
            logger.debug(f"Fetching RSS feed: {feed_url}")
            feed = feedparser.parse(feed_url)

            for item in feed.entries[:10]:
                try:
                    title = item.get("title", "")
                    link = item.get("link", "")
                    if not title or not link:
                        continue

                    # Parse publication date
                    pub_date = None
                    if hasattr(item, "published_parsed") and item.published_parsed:
                        pub_date = datetime(*item.published_parsed[:6])

                    entry = KnowledgeEntry(
                        title=title,
                        authors=["Editorial"],
                        year=pub_date.year if pub_date else datetime.now().year,
                        venue="RSS",
                        doi_or_url=link,
                        abstract=(item.get("summary", ""))[:200],
                        published_date=pub_date,
                        citation_count=0,
                        source=SourceType.RSS,
                        tier=4  # RSS is always Tier 4
                    )
                    entries.append(entry)

                except Exception as e:
                    logger.debug(f"Failed to parse RSS item: {e}")

        except Exception as e:
            logger.warning(f"Failed to fetch RSS feed {feed_url}: {e}")

    logger.info(f"RSS: fetched {len(entries)} entries")
    if entries:
        metrics.sources_succeeded += 1
    time.sleep(KNOWLEDGE_CONFIG["rate_limit_delay"])
    return entries


# ==================== MAIN PIPELINE ====================

def format_entry(entry: KnowledgeEntry) -> str:
    """Format entry for knowledge base."""
    tier_label = {1: "Tier 1", 2: "Tier 2", 3: "Tier 3", 4: "Tier 4"}
    date_str = datetime.now().strftime("%Y-%m-%d")
    authors = ", ".join(entry.authors) or "Unknown"

    return f"\n### {date_str} — {entry.title}\n" \
           f"- **Authors:** {authors}\n" \
           f"- **Year:** {entry.year}\n" \
           f"- **Venue:** {entry.venue}\n" \
           f"- **DOI/URL:** {entry.doi_or_url}\n" \
           f"- **Evidence Tier:** {tier_label.get(entry.tier, 'Tier 4')}\n" \
           f"- **Relevance Score:** {entry.relevance_score}/10\n" \
           f"- **Key Finding:** {entry.abstract}\n"


def append_to_brain(
    entries: List[KnowledgeEntry],
    existing_hashes: Set[str],
    metrics: CrawlMetrics,
    dry_run: bool = False
) -> int:
    """Append new entries to knowledge base."""
    new_entries = []

    for entry in entries:
        try:
            h = compute_hash(entry.doi_or_url)
            if h in existing_hashes:
                metrics.entries_skipped += 1
                continue

            existing_hashes.add(h)
            new_entries.append(entry)

        except Exception as e:
            logger.error(f"Failed to process entry: {e}")
            metrics.entries_failed += 1

    if not new_entries:
        logger.info("No new entries to add")
        return 0

    # Score and sort entries
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    for entry in new_entries:
        entry.relevance_score = score_entry(entry, KNOWLEDGE_CONFIG["keywords"], now)

    new_entries.sort(key=lambda x: x.relevance_score, reverse=True)
    new_entries = new_entries[:KNOWLEDGE_CONFIG["max_new_entries_per_run"]]

    if dry_run:
        logger.info(f"[DRY RUN] Would append {len(new_entries)} entries:")
        for entry in new_entries[:5]:  # Show first 5
            logger.info(f"  - {entry.title} (score: {entry.relevance_score})")
        return len(new_entries)

    # Append to knowledge base
    try:
        content = BRAIN_PATH.read_text(encoding="utf-8")

        # Ensure update log section exists
        if "## 7. Knowledge Update Log" not in content:
            content += "\n## 7. Knowledge Update Log\n"

        # Format and append entries
        text = "".join(format_entry(entry) for entry in new_entries)
        content += text

        BRAIN_PATH.write_text(content, encoding="utf-8")

        metrics.entries_new = len(new_entries)
        logger.info(f"Appended {len(new_entries)} entries to knowledge base")
        return len(new_entries)

    except Exception as e:
        logger.error(f"Failed to append to knowledge base: {e}")
        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Enhanced knowledge pipeline for beach-cleaning-robot-design"
    )
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing")
    parser.add_argument("--news-only", action="store_true", help="Fetch RSS news only")
    parser.add_argument("--keywords", nargs="+", help="Custom keywords to search")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    if args.verbose and STRUCTURED_LOGGING:
        # Adjust log level
        pass

    start_time = time.time()
    keywords = args.keywords or KNOWLEDGE_CONFIG["keywords"]

    logger.info("=" * 60)
    logger.info("KNOWLEDGE UPDATE PIPELINE STARTED")
    logger.info(f"Domain: {KNOWLEDGE_CONFIG['domain']}")
    logger.info(f"Keywords: {', '.join(keywords[:5])}")
    logger.info(f"Dry run: {args.dry_run}")
    logger.info(f"News only: {args.news_only}")
    logger.info("=" * 60)

    metrics = CrawlMetrics()
    all_entries = []

    # Fetch from sources
    if not args.news_only:
        all_entries.extend(fetch_arxiv(keywords, metrics))
        all_entries.extend(fetch_semantic_scholar(keywords, metrics))

    all_entries.extend(fetch_rss(metrics))

    metrics.entries_fetched = len(all_entries)
    logger.info(f"Total entries fetched: {metrics.entries_fetched}")

    # Load existing hashes
    existing_hashes = load_existing_hashes()

    # Append to knowledge base
    n_added = append_to_brain(all_entries, existing_hashes, metrics, args.dry_run)

    # Calculate metrics
    metrics.duration_seconds = time.time() - start_time

    # Report
    logger.info("=" * 60)
    logger.info("KNOWLEDGE UPDATE PIPELINE COMPLETE")
    logger.info(f"Duration: {metrics.duration_seconds:.2f}s")
    logger.info(f"Sources attempted: {metrics.sources_attempted}")
    logger.info(f"Sources succeeded: {metrics.sources_succeeded}")
    logger.info(f"Entries fetched: {metrics.entries_fetched}")
    logger.info(f"Entries added: {metrics.entries_new}")
    logger.info(f"Entries skipped (duplicate): {metrics.entries_skipped}")
    logger.info(f"Entries failed: {metrics.entries_failed}")
    logger.info("=" * 60)

    # Save metrics
    metrics_path = LOG_DIR / "knowledge_updater_metrics.json"
    try:
        with open(metrics_path, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics.to_dict(),
                "config": {
                    "domain": KNOWLEDGE_CONFIG["domain"],
                    "keywords": keywords,
                    "dry_run": args.dry_run
                }
            }, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save metrics: {e}")

    return 0 if n_added >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
