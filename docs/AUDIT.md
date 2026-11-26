## Audit trail

A local JSONL audit helper is available for reproducible research records:

```python
from autonomous_trading_lab.audit import dataclass_record, write_jsonl

record = dataclass_record(result)
write_jsonl("artifacts/backtest.jsonl", record)
```

Audit files are derived from local simulated runs. Never write private exchange credentials or live order secrets into these records.
