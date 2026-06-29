"""
royalty_logic.py

Core logic for calculating music royalty splits (PRO-style).

In the music industry, royalties from a song are typically split into two
main "shares":
  - Writer's Share (50%): paid directly to the songwriter(s)/composer(s)
  - Publisher's Share (50%): paid to whoever owns/administers the publishing
    rights (often the writer themselves if self-published, or a publishing
    company they've signed with)

Within each share, the percentage is divided among contributors based on
their agreed-upon split (often negotiated based on creative contribution).

This module contains pure functions (no web/UI code) so the math can be
tested and reused independently of how it's presented to the user.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Contributor:
    """A single contributor to a song (a writer or a publisher entity)."""
    name: str
    percentage: float  # percentage of THEIR share (writer's or publisher's), 0-100

    def __post_init__(self):
        if self.percentage < 0 or self.percentage > 100:
            raise ValueError(
                f"Percentage for {self.name} must be between 0 and 100, got {self.percentage}"
            )


@dataclass
class SplitResult:
    """The calculated dollar/percentage result for one contributor."""
    name: str
    share_type: str  # "Writer's Share" or "Publisher's Share"
    percentage_of_share: float
    percentage_of_total: float
    dollar_amount: float


def validate_percentages(contributors: List[Contributor], label: str) -> None:
    """Raise an error if a group of contributors' percentages don't sum to 100."""
    total = sum(c.percentage for c in contributors)
    # Allow tiny floating point drift
    if abs(total - 100.0) > 0.01:
        raise ValueError(
            f"{label} percentages must add up to 100%. Currently: {total:.2f}%"
        )


def calculate_splits(
    total_royalty_amount: float,
    writers: List[Contributor],
    publishers: List[Contributor],
    writer_share_percent: float = 50.0,
    publisher_share_percent: float = 50.0,
) -> List[SplitResult]:
    """
    Calculate the full royalty split breakdown.

    Args:
        total_royalty_amount: Total dollar amount being split (e.g. $1000)
        writers: List of Contributor objects for the writer's share.
                 Their .percentage values should sum to 100.
        publishers: List of Contributor objects for the publisher's share.
                     Their .percentage values should sum to 100.
        writer_share_percent: What % of the TOTAL goes to writers overall
                               (industry standard default is 50%)
        publisher_share_percent: What % of the TOTAL goes to publishers overall
                                  (industry standard default is 50%)

    Returns:
        A list of SplitResult objects, one per contributor, showing exactly
        how much money and what overall percentage they receive.
    """
    if abs((writer_share_percent + publisher_share_percent) - 100.0) > 0.01:
        raise ValueError("Writer's share + Publisher's share must equal 100%")

    validate_percentages(writers, "Writer's share")
    validate_percentages(publishers, "Publisher's share")

    results: List[SplitResult] = []

    writer_pool = total_royalty_amount * (writer_share_percent / 100.0)
    for w in writers:
        dollar_amount = writer_pool * (w.percentage / 100.0)
        percentage_of_total = (writer_share_percent / 100.0) * w.percentage
        results.append(
            SplitResult(
                name=w.name,
                share_type="Writer's Share",
                percentage_of_share=w.percentage,
                percentage_of_total=percentage_of_total,
                dollar_amount=dollar_amount,
            )
        )

    publisher_pool = total_royalty_amount * (publisher_share_percent / 100.0)
    for p in publishers:
        dollar_amount = publisher_pool * (p.percentage / 100.0)
        percentage_of_total = (publisher_share_percent / 100.0) * p.percentage
        results.append(
            SplitResult(
                name=p.name,
                share_type="Publisher's Share",
                percentage_of_share=p.percentage,
                percentage_of_total=percentage_of_total,
                dollar_amount=dollar_amount,
            )
        )

    return results


if __name__ == "__main__":
    # Quick manual test when running this file directly:
    # python royalty_logic.py
    writers = [
        Contributor(name="Lorie B", percentage=70),
        Contributor(name="Co-Writer Jay", percentage=30),
    ]
    publishers = [
        Contributor(name="AI Girl LLC (Self-Published)", percentage=100),
    ]

    splits = calculate_splits(
        total_royalty_amount=1000.00,
        writers=writers,
        publishers=publishers,
    )

    print(f"{'Name':<30}{'Share Type':<20}{'% of Share':<12}{'% of Total':<12}{'Amount'}")
    print("-" * 90)
    for r in splits:
        print(
            f"{r.name:<30}{r.share_type:<20}{r.percentage_of_share:<12.2f}"
            f"{r.percentage_of_total:<12.2f}${r.dollar_amount:,.2f}"
        )
