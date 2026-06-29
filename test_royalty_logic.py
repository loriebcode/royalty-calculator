"""
test_royalty_logic.py

Basic tests for the core royalty split math in royalty_logic.py.

Run with:
    python -m pytest test_royalty_logic.py -v

Or, without pytest installed:
    python test_royalty_logic.py
"""

from royalty_logic import Contributor, calculate_splits, validate_percentages


def test_basic_even_split():
    """Two writers splitting evenly, single publisher, standard 50/50 share."""
    writers = [
        Contributor(name="Writer A", percentage=50),
        Contributor(name="Writer B", percentage=50),
    ]
    publishers = [Contributor(name="Publisher A", percentage=100)]

    results = calculate_splits(1000.0, writers, publishers)

    by_name = {r.name: r for r in results}
    assert by_name["Writer A"].dollar_amount == 250.0
    assert by_name["Writer B"].dollar_amount == 250.0
    assert by_name["Publisher A"].dollar_amount == 500.0


def test_uneven_writer_split():
    """Writers with an uneven (70/30) split."""
    writers = [
        Contributor(name="Lorie B", percentage=70),
        Contributor(name="Co-Writer", percentage=30),
    ]
    publishers = [Contributor(name="AI Girl LLC", percentage=100)]

    results = calculate_splits(1000.0, writers, publishers)
    by_name = {r.name: r for r in results}

    assert by_name["Lorie B"].dollar_amount == 350.0
    assert by_name["Co-Writer"].dollar_amount == 150.0


def test_custom_share_percentages():
    """Writer/publisher overall share doesn't have to be 50/50."""
    writers = [Contributor(name="Solo Writer", percentage=100)]
    publishers = [Contributor(name="Self Published", percentage=100)]

    # Writer keeps 60% of total (instead of standard 50%)
    results = calculate_splits(
        1000.0, writers, publishers,
        writer_share_percent=60,
        publisher_share_percent=40,
    )
    by_name = {r.name: r for r in results}

    assert by_name["Solo Writer"].dollar_amount == 600.0
    assert by_name["Self Published"].dollar_amount == 400.0


def test_invalid_writer_percentages_raises():
    """Writer percentages that don't sum to 100 should raise an error."""
    writers = [Contributor(name="Writer A", percentage=60)]  # only 60, not 100
    publishers = [Contributor(name="Publisher A", percentage=100)]

    try:
        calculate_splits(1000.0, writers, publishers)
        assert False, "Expected a ValueError but none was raised"
    except ValueError as e:
        assert "100%" in str(e)


def test_invalid_share_split_raises():
    """Writer share % + Publisher share % must equal 100."""
    writers = [Contributor(name="Writer A", percentage=100)]
    publishers = [Contributor(name="Publisher A", percentage=100)]

    try:
        calculate_splits(
            1000.0, writers, publishers,
            writer_share_percent=60,
            publisher_share_percent=60,  # 60 + 60 = 120, invalid
        )
        assert False, "Expected a ValueError but none was raised"
    except ValueError:
        pass  # expected


def test_negative_percentage_rejected():
    """A Contributor can't have a negative percentage."""
    try:
        Contributor(name="Bad Writer", percentage=-10)
        assert False, "Expected a ValueError but none was raised"
    except ValueError:
        pass  # expected


if __name__ == "__main__":
    # Allow running this file directly without pytest installed.
    test_functions = [
        test_basic_even_split,
        test_uneven_writer_split,
        test_custom_share_percentages,
        test_invalid_writer_percentages_raises,
        test_invalid_share_split_raises,
        test_negative_percentage_rejected,
    ]

    passed = 0
    for test_func in test_functions:
        try:
            test_func()
            print(f"PASSED: {test_func.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAILED: {test_func.__name__} — {e}")

    print(f"\n{passed}/{len(test_functions)} tests passed")
