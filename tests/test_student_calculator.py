import pytest

from calculator.commands import LastCommand
from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession


def test_adjust_with_offset_and_scale():
    calculation = CalculationFactory.create(
        "adjust", 3, offset=2, scale=4
    )
    assert calculation.get_result() == 20


def test_span_with_negative_values():
    calculation = CalculationFactory.create(
        "span", -4, 3, 8
    )
    assert calculation.get_result() == 12


def test_span_requires_at_least_two_values():
    calculation = CalculationFactory.create("span", 5)

    with pytest.raises(ValueError):
        calculation.get_result()


def test_last_returns_latest_successful_result():
    session = CalculatorSession()

    calculation = CalculationFactory.create("add", 2, 3)
    session.calculate(calculation)

    result = LastCommand(session).execute()

    assert result == "add 2.0 3.0 = 5.0000"


def test_failed_calculation_not_added_to_history():
    session = CalculatorSession()

    calculation = CalculationFactory.create("divide", 1, 0)

    with pytest.raises(ZeroDivisionError):
        session.calculate(calculation)

    assert session.get_history() == []


def test_last_when_history_is_empty():
    session = CalculatorSession()

    assert LastCommand(session).execute() == "History is empty."