import numpy as np
from numpy.typing import ArrayLike
from typing import Literal

import matplotlib.pyplot as plt
import arviz as az
import warnings

az.style.use("arviz-viridish")


def rmse_at_n(
    samples: ArrayLike, # n x k
    n: int, 
    true_rate: float,
) -> float:
    """This function approx. D_n, the average variance of using n samples."""
    if n > samples.shape[0]:
        warnings.warn("Attempting to compute with n greater than the nr_samples")
    
    if len(samples.shape) > 2:
        warnings.warn("Functionality wasn't tested on tensors (dim >= 3)")
    
    average_Z = samples[0:n].mean(axis=0)
    return np.sqrt(
        (np.square(average_Z - true_rate)).mean()
    )


def simulate_rv_convergence(
    dist: Literal["poisson", "binomial"],
    n: int, 
    parameters: dict[str, float|int],
    sample_every_n: int = 100,
    nr_repetitions: int = 3,
    rng_seed = 1377
) -> dict:
    """--"""    
    match [dist, parameters]:
        case ["poisson", {"lam": lam}] if lam > 0:
            parameter, variance = lam, lam
        case ["binomial", {"p": p, "n": n_trials}] if 0 <= p <= 1 and n_trials >=1:
            parameter = p * n_trials
            variance = n_trials * p * (1 - p)      
        case _:
            raise ValueError("only poisson|binomial are supported or no valid parameter supplied")        

    rng = np.random.default_rng(seed = rng_seed)
    sample_sizes = np.array(range(1, n, sample_every_n))

    if hasattr(rng, dist) and callable(dist_fn := getattr(rng, dist)):
        samples = dist_fn(**parameters, size=(n, nr_repetitions))
    else:
        raise ValueError("only poisson|binomial are supported or numpy API changed")
    
    partial_average = np.array([
        [samples[:i, k].mean() for i in sample_sizes]
        for k in range(nr_repetitions)
    ])
    distance_results = np.array(
        [rmse_at_n(samples, n, parameter) for n in sample_sizes]
    )

    return {
        "partial_average": partial_average,
        "sample_sizes": sample_sizes,
        "mse": distance_results,
        "variance": variance,
        "parameter": parameter
    }


def plot_rv_convergence(df) -> None:

    sample_sizes = df["sample_sizes"]
    partial_average = df["partial_average"]
    distance_results = df["mse"]
    param = df["parameter"]
    variance = df["variance"]
    nr_repetitions = partial_average.shape[0]

    fig, ax = plt.subplots(figsize=(8, 8), layout='constrained', nrows=2)
    ax[0].yaxis.grid(True, color="lightgrey", linestyle="--")
    ax[1].yaxis.grid(True, color="lightgrey", linestyle="--")
    fig.set_facecolor("white")
    ax[0].set_facecolor("white")
    ax[1].set_facecolor("white")



    for k in range(nr_repetitions):
        ax[0].plot(
             sample_sizes, partial_average[k], lw=1.5, label=f"seq {k}"
        )

    ax[0].axhline(param, color = "red", ls = "--", label = "$\lambda$")
    ax[0].set_ylim(param - param*0.04, param + param*0.04)

    ax[0].set_ylabel( "average of $n$ samples")
    ax[0].set_title(
        f"Convergence of the average of \n random variables to its expected value $\\theta = {param}$"
    )
    ax[0].legend(loc='center right', ncol = 1, bbox_to_anchor=(0.95, 0.7), frameon=False)


    ax[1].set_xlabel("# of samples, $n$")

    ax[1].set_ylabel( "expected squared-distance from true value" )
    ax[1].plot(sample_sizes, distance_results, lw = 3, 
                label="d($\\bar{x}$, $\lambda$)")
    ax[1].plot( sample_sizes, np.sqrt(variance)/np.sqrt(sample_sizes), lw = 2, ls = "--", 
            label = r"$\frac{\sqrt{\lambda}}{\sqrt{N}}$")
    ax[1].set_ylim(0, max(distance_results) * 0.05)
    ax[1].legend(loc='center right', ncol = 1, bbox_to_anchor=(0.95, 0.7), frameon=False)
    plt.show()