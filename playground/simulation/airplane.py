import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compute_nr_passengers(
        p_showup: float,
        p_couple: float,
        *,
        nr_samples: int = 5000,
        seed : int = 1317,
) -> pd.DataFrame:
    """Simulate the outcomes of the airplane problem ... """
    rng = np.random.default_rng(seed=seed)
    p_couple_reservation = (1 - (1 - p_couple)**2)
    df = pd.DataFrame({
        "third_wheel": rng.binomial(1, p_couple_reservation, size=nr_samples), 
        "y_individuals": rng.binomial(n=3, p=p_showup, size=nr_samples), 
        "y_mix": (
            rng.binomial(1, p_couple_reservation, size=nr_samples) + 
            2 * rng.binomial(1, p_showup**2, size=nr_samples)
        )
    })

    # either this or use .assign(lambda df_: ...) method chaining
    df["nr_show_up"] = (
        df.third_wheel * df.y_mix + (1 - df.third_wheel) * df.y_individuals
    )

    return df


def plot_passengers(df: pd.DataFrame, p_showup=0.85) -> None:
       rng = np.random.default_rng(seed=1317)
       nr_samples = len(df)
       show_up_pmf: pd.Series = df.nr_show_up.value_counts() / nr_samples
       
       y_individuals = rng.binomial(n=3, p=p_showup, size=nr_samples)
       show_up_ind, show_up_ind_counts = np.unique(y_individuals, return_counts=True)
       show_up_ind_pmf = show_up_ind_counts / show_up_ind_counts.sum()

       fig, ax = plt.subplots(figsize = (8, 5), layout="constrained")
       _ = ax.set_title("Distribution of nr. passengers who arrive to fly")

       offset, width = 0.2, 0.4
       color_array = ["darkred" if i == 2 else "lightgrey" for i in show_up_pmf.index]
       ax.bar(x=show_up_pmf.index - offset , height=show_up_pmf, 
              color=color_array, width = width, label = "Probably Mixed")
       ax.bar(x=show_up_ind + offset, height=show_up_ind_pmf, 
              width = width, color="lightskyblue", label = "If only singles")

       ax.annotate("low risk!", xytext=(-0.33, 0.05), xy = (0, 0.02))
       ax.annotate("call couples \nthe day before", xytext=(1.4, 0.16), xy = (1.5, 0.15))

       ax.tick_params(bottom='on', labelbottom='on')

       ax.xaxis.tick_bottom()
       ax.set_xticks(range(0, 4))
       ax.yaxis.grid(True, color="lightgrey", linestyle="--")

       ax.set_ylabel("Probability of outcome (PMF)")
       fig.set_facecolor("white")
       ax.legend(loc='best', frameon=False) #, ncol = 1, bbox_to_anchor=(1.3, 0.6), )

       ax.set_facecolor("white")