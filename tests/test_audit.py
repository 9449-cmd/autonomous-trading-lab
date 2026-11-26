from pathlib import Path

from autonomous_trading_lab.audit import dataclass_record, write_jsonl
from autonomous_trading_lab.engine import BacktestConfig, BacktestResult


def test_audit_record_round_trip(tmp_path: Path):
    result = BacktestResult(
        initial_equity=100.0,
        final_equity=101.0,
        total_return_pct=1.0,
        max_drawdown_pct=0.5,
        trades=1,
        equity_curve=(),
    )
    record = dataclass_record(result)
    path = tmp_path / "audit" / "backtest.jsonl"
    write_jsonl(path, record)

    assert path.read_text(encoding="utf-8").strip().startswith('{"equity_curve"')
