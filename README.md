# Decision-making under uncertainty

This repository emerges out of teaching data science to students of various backgrounds and my practice in the industry. I aspire to contribute to the understanding of this complex landscape and teach people how to navigate it, how to develop valuable skills, and become more effective at problem-solving.

That's it, whatever will be published here can't be the be-all-end-all bootcamp or course. But here are a few of my beliefs, which may persuade you to take the long road to your own development in AI instead of searching for "the tutorial":

- There is no shortcut to a deep understanding of a domain, especially an interconnected network of fields and communities being in an evolving dialogue
- There is no shortcut to being skillful at something
- The journey from novice to expert is not linear, however, the "interest compounds"
- The journey need not be painful, but it can be seriously playful,a source of wonder and meaning
- Without skin in the game, we can't claim we truly get something
- Without a vision which is flexible enough, but at the same time long-lived:
    - In the case of rigidity - there is a risk of being stuck, rigid, or pursue obsessively, counterproductively, and getting fooled
    - In the case of everything goes - there is a risk of wandering aimlessly and not finding a home
- Fixating on beliefs and propositional knowing (the facts!) is counterproductive. Which should put into question all written above
- Fixating on skills makes you lose the grasp of the big picture

## Recent highlights

The repository will go through many changes as we go through the journey together, but you can get a sneak-peek of what it's about in the `/playground` directory. Of course it's unstable.

| ![Influence DAG](docs/img/output.svg)| ![LLN](docs/img/llln.png)|
|:--:|:--:|
| **(Fig.1) - How many people will show up to safari?** [notebook here](https://github.com/Bizovi/decision-making/blob/main/playground/01_tourism.ipynb)| **(Fig.2) - The greatest theorem never told** adapted and refactored [from CamDavidson](https://nbviewer.org/github/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/blob/master/Chapter4_TheGreatestTheoremNeverTold/Ch4_LawOfLargeNumbers_PyMC3.ipynb) (upcoming!)

### Week 3: Practice and readings

First, you have to be confident and comfortable with your local development tooling. Invest an hour to understand conda and type in the commands -- benefit a decade ahead!

- Walk through this tutorial: ["Introduction to conda for (data) scientists"](https://carpentries-incubator.github.io/introduction-to-conda-for-data-scientists/). It will serve you well for exploration and experimentation. 
    - For projects more focused on building data-driven applications, we will use `pip` and `poetry`.
    - We can use `conda` just for virtual environments and not for package management and dependency resolution / tracking.
    - Therefore, one has to pick an optimal approach for each project. Not great, but could be worse (as in `npm`)
- Read this old, but still relevant blog post about ["Conda: Myths and Misconceptions"](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/)



## Getting Started

If you have `conda` installed on Linux, MacOS or WSL2 on Windows, the easiest way to play around with the notebook is to recreate the environment from the yml file. Then, you can either create a kernel or connect from VSCode notebooks to the environment and start hacking.

```bash
git clone https://github.com/bizovi/decision-making.git

cd playground
conda env create --file conda-env.yml
conda activate gpa-prob

# if using a jupyter lab
python -m ipykernel install --user \
    --name="gpa-kernel" \
    --display-name="Kernel for Simulations"

# run the test suite and see if everything works as expected
python -m pytest 
```
