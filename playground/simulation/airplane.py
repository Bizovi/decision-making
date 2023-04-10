import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import graphviz as gr
plt.style.use("ggplot")


def plot_causal_graph() -> None:
    """A low-resolution influence graph, a story of how people show up"""
    g = gr.Digraph()

    with g.subgraph(name='cluster_1') as c:
        c.attr(label='1:nr_trips')
        c.edges([
            ("X2", "X3"),    ("X3", "Y mix"), ("X2", "Y mix"), 
            ("X1", "Y ind"), ("Y ind", "Y"),  ("Y mix", "Y" ),
        ])
        c.node("X3", color="lightblue", style='filled')
        c.node("X1", color="lightblue", style='filled')

    g.node("pr_showup", fillcolor="lightgrey", style="filled")
    g.edge("pr_showup", "Y ind")
    g.edge("pr_showup", "Y mix")

    g.node("share\ncouples", fillcolor="lightgrey", style="filled")
    g.edge("share\ncouples", "X2")
    return g


def compute_nr_passengers(
        p_showup: float,
        p_couple: float,
        *,
        nr_samples: int = 5000,
        seed : int = 1317,
) -> pd.DataFrame:
    """Simulates how many passengers will show up to a safari or flight, if there are 
    only 3 spots on the plane / car. Couples don't show up if any of them doesn't go.

    Arguments:
        * p_showup: probability that each individual will keep the promise
        * p_couple: probability that a person will bring a (+1) - attention,
            the narrative is that one reserves the spot and drags another,
            so p_couple in the population isn't what will end up on the plane
        * nr_samples: you could use something more realistic, of a few years 
            being in business -- there will be more uncertainty
        * seed: to ensure reproducibility

    Returns: pd.DataFrame with the following columns
        * third_wheel: whether there is a couple making a reservation  
        * y_individuals: number of individuals who show up if reserved independently
        * y_mix: number of individuals who show when a couple made reservation
        * nr_show_up: final number of individuals who show up
    """
    rng = np.random.default_rng(seed=seed)
    p_couple_reservation = (1 - (1 - p_couple)**2)
    df = pd.DataFrame({
        "third_wheel": rng.binomial(1, p_couple_reservation, size=nr_samples), 
        "y_individuals": rng.binomial(n=3, p=p_showup, size=nr_samples), 
        "y_mix": (
            rng.binomial(1, p_couple_reservation, size=nr_samples) + 
            2 * rng.binomial(1, p_showup**2, size=nr_samples)
        )
    }).assign(
        nr_show_up = (
            lambda df_: 
            df_.third_wheel*df_.y_mix + 
            (1 - df_.third_wheel) * df_.y_individuals
        )
    )   
    return df


def plot_passengers(df: pd.DataFrame, p_showup=0.85) -> None:
       """Visualize the distribution of people who show up, if there are only individuals,
       or couples + individuals in our statistical population
       
        Arguments:
            * df: pd.DataFrame with the following columns
                * third_wheel: whether there is a couple making a reservation  
                * y_individuals: number of individuals who show up if reserved independently
                * y_mix: number of individuals who show when a couple made reservation
                * nr_show_up: final number of individuals who show up
            * p_showup: the theoretical value of the parameter p (share ppl showing up)

       """
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