import pytest
from simulation.airplane import compute_nr_passengers


def test_dataframe_contract():
    # Setup
    p_showup, p_couple, nr_samples = 0.85, 0.6, 2000

    # Execute
    df = compute_nr_passengers(p_showup, p_couple, nr_samples=nr_samples)

    # Validate / Test
    assert df.shape[0] == nr_samples
    assert df.shape[1] == 4
    assert set(df.columns) == {"third_wheel", "y_individuals", "y_mix", "nr_show_up"}


def test_wrong_input_parameter_raises_value_error():
    p_showup, p_couple, nr_samples = 1.2, 0.6, 2000
    
    with pytest.raises(ValueError):
        _ = compute_nr_passengers(p_showup, p_couple, nr_samples=nr_samples)
