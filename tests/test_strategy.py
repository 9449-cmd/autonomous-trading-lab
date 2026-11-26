def test_moving_average_flip():
    # Added in a follow-up test module to document deterministic signal behavior.
    from autonomous_trading_lab.models import Signal
    from autonomous_trading_lab.strategy import moving_average_signal

    assert moving_average_signal([10, 11, 12, 13], 2, 3) is Signal.LONG
