from pathlib import Path

from ara_math.erdos_status import (
    parse_arxiv_solution_feed,
    parse_official_status_page,
    refresh_erdos_problem_record,
)
from ara_math.models import ProblemRecord


def test_parse_official_status_page_detects_proved() -> None:
    html = """
    <html><body>
    <div>PROVED This has been solved in the affirmative. - $25</div>
    <div>This page was last edited 01 February 2026.</div>
    </body></html>
    """

    payload = parse_official_status_page(html)

    assert payload["status"] == "proved"
    assert payload["last_edited"] == "01 February 2026"


def test_parse_official_status_page_detects_open_without_comment_leakage() -> None:
    html = """
    <html><body>
    <div>Random Solved Random Open OPEN This is open, and cannot be resolved with a finite computation. - $25</div>
    <div>Later comment: this has been solved for a special subcase.</div>
    <div>This page was last edited 18 April 2026.</div>
    </body></html>
    """

    payload = parse_official_status_page(html)

    assert payload["status"] == "open"
    assert payload["headline"] == "OPEN"


def test_parse_arxiv_solution_feed_detects_strong_signal() -> None:
    feed = """<?xml version='1.0' encoding='UTF-8'?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <id>http://arxiv.org/abs/2604.03609v1</id>
        <title>Solution of Erdős Problem 633</title>
        <summary>We classify triangles that can be tiled only into a square number of congruent triangles, settling Erdős Problem 633.</summary>
        <published>2026-04-04T06:48:14Z</published>
      </entry>
    </feed>
    """

    candidates = parse_arxiv_solution_feed(feed, problem_id="633")

    assert len(candidates) == 1
    assert candidates[0]["confidence"] == "strong_solution_signal"


def test_refresh_erdos_problem_record_marks_recent_solution_preprint() -> None:
    problem = ProblemRecord(
        problem_id="633",
        title="Erdős Problem #633",
        source="Erdős Problems",
        statement="placeholder",
        domain="geometry",
        references=["https://www.erdosproblems.com/633"],
        metadata={"source_catalog": "erdosproblems", "status_state": "open"},
    )

    official_html = """
    <html><body>
    <div>OPEN This is open, and cannot be resolved with a finite computation.</div>
    <div>This page was last edited 21 March 2026.</div>
    </body></html>
    """
    arxiv_feed = """<?xml version='1.0' encoding='UTF-8'?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <id>http://arxiv.org/abs/2604.03609v1</id>
        <title>Solution of Erdős Problem 633</title>
        <summary>We classify triangles that can be tiled only into a square number of congruent triangles, settling Erdős Problem 633.</summary>
        <published>2026-04-04T06:48:14Z</published>
      </entry>
    </feed>
    """

    def fetcher(url: str) -> str:
        if "erdosproblems.com" in url:
            return official_html
        if "export.arxiv.org" in url:
            return arxiv_feed
        raise AssertionError(url)

    refreshed = refresh_erdos_problem_record(problem, fetcher=fetcher)

    assert refreshed.open_problem is False
    assert refreshed.metadata["status_state"] == "likely_solved_preprint"
    assert refreshed.metadata["remote_solution_signal_count"] == 1
