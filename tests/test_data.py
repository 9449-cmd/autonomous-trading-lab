from autonomous_trading_lab.data import load_candles_csv


def test_load_csv_with_optional_values_and_z_timestamp(tmp_path):
    path = tmp_path / "candles.csv"
    path.write_text(
        "timestamp,open,high,low,close,volume,funding_rate\n"
        "2026-01-01T00:00:00Z,10,12,9,11,3,0.001\n"
        "2026-01-01T01:00:00+00:00,11,13,10,12,,\n",
        encoding="utf-8",
    )

    candles = load_candles_csv(path)
    assert len(candles) == 2
    assert candles[0].funding_rate == 0.001
    assert candles[1].volume == 0
    assert candles[1].funding_rate == 0


def test_load_csv_rejects_timezone_naive_timestamps(tmp_path):
    path = tmp_path / "naive.csv"
    path.write_text(
        "timestamp,open,high,low,close\n2026-01-01T00:00:00,10,11,9,10\n",
        encoding="utf-8",
    )

    try:
        load_candles_csv(path)
    except ValueError as exc:
        assert "timezone" in str(exc)
    else:
        raise AssertionError("Expected timezone validation error")


def test_load_csv_rejects_invalid_candle_and_order(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text(
        "timestamp,open,high,low,close\n"
        "2026-01-01T01:00:00Z,10,11,9,10\n"
        "2026-01-01T00:00:00Z,10,11,9,10\n",
        encoding="utf-8",
    )

    try:
        load_candles_csv(path)
    except ValueError as exc:
        assert "strictly increasing" in str(exc)
    else:
        raise AssertionError("Expected ordering validation error")
