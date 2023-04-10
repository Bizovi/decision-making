from simulation.airplane import compute_nr_passengers

def test_dimensions_correspond():
    # Setup
    p_showup, p_couple, nr_samples = 0.85, 0.6, 2000

    # Execute
    df = compute_nr_passengers(
        p_showup, 
        p_couple, 
        nr_samples=nr_samples
    )

    # Validate / Test
    assert df.shape[0] == nr_samples
