# Some notes:

1. Notebooks are fantastic for iteratively exploring and running experiments quickly. For larger scale projects Python scripts more reproducible and easier to run. We will combine notebooks and Python scripts together
2. I usually start machine learning projects in Jupyter/Google Colab notebooks for quick experimentation and visualization, and then when I've got something working, I move the most useful pieces of code to Python scripts
3. There are many possible workflows for writing machine learning code. Some prefer to start with scripts, others (like me) prefer to start with notebooks and go to scripts later on.


## Three highlights in this paper:

- Judd-Ofelt theory based, DFT-assisted numerical calculation of transition intensity of lanthanides in solids.
- Markov chain Monte Carlo model for many-ion collective interactions in $\mathrm{NaYF_4}$.
- Neural network model
- Computational tool box for experimentalists.

Since we have already comprehensively investigated the effects of crystal fields and electromagnetic fields on single $\mathrm{Ln}^{3+}$ in crystal $\mathrm{NaYF_4}$, now we will treat the spectroscopic properties of single particle emission spectrum as collective phenomena, induced by cooperactive actions and exchange interactions of many lanthanides in solid. There is no strict distinction between radiative and non-radiative emission. As a result, we calculate the transition rate with Judd-Ofelt theory and the actual distance between ions in Euclidean space, and then convert it to transition probability, which will be further compared with generated random number. Therefore, all transitions are treated equally based on a probabilistic perspective.


### Monte Carlo Simulation

Recall that this research endeavors to advance the understanding of energy transfer dynamics within UCNPs by developing and refining a Monte-Carlo model. Grounded in an extensive theoretical framework and calculated transition rates so far, the various mechanisms involved in energy redistribution are examined, including resonant energy transfer process(RET), phonon-assisted energy transfer process(PET)(up-conversion, cross-relaxation), electric dipole (ED) and magnetic dipole (MD) radiative emissions, and multi-phonon relaxation. 



The Monte Carlo model, which is currently in the refinement stage to ensure its predictions accurately mirror experimental findings. It integrates several critical components and reasonable assumption to simulate the complex transition behaviors of UCNPs with high fidelity:

- Ion spatial distribution


The model conceptualizes nanoparticles as hexagonal crystal structures($\beta$-phase), where $\mathrm{Yb^{3+}}$ or $\mathrm{Tm^{3+}$} ions are randomly distributed. This approach not only captures the inherent spatial relationships characteristic of hexagonal crystallinity but also facilitates a realistic representation of ion dispersion within the nanoparticle matrix.


- Critical interacting distance $R_0$


Acknowledging the inverse sixth power dependence of the energy transfer rate on the inter-ionic distance ($R$), the model introduces a critical interaction distance $R_0=1 ~\mathrm{nm}$. This pragmatic adjustment allows for the efficient simulation of ion interactions by limiting the consideration of effective neighbors to those within this defined radius, thus optimizing computational resources without compromising the model's integrity.



- High energy levels truncation 


Our simulations reveal that very few population inhabit in higher energy levels that have negligible contribution to the desired emission, and we have decided to truncate higher energy levels so that computational complexity can be also reduced. Meanwhile manually restricting the transition options for different ions at different levels.


- Probabilistic process modeling


The simulation timescale operates over $T=1~ \mathrm{s}$, segmented into nanosecond increments $\Delta t=1 ~\mathrm{us}$ yielding a comprehensive resolution of $1 \times 10^6$ steps. Each step assesses the state of excited sensitizer $\mathrm{Yb^{3+}}$ and emitter $\mathrm{Tm^{3+}}$ and their immediate neighbors within $R_0$, determining the subsequent mutual competitive energy transfer events, through a probabilistic comparison between a generated random number \textbf{$p_i$}, and established all transition rates $W=\{\mathrm{ED+MD}, \mathrm{Up}-\mathrm{conversion}, \mathrm{Cross}-\mathrm{relaxation}, \mathrm{Stay}\}$.


- Emission transition selection


A pivotal aspect of the simulation involves tracking and quantifying transition events over time: $10^6$ steps with $\Delta t= 1~\mathrm{us}, T=1~ \mathrm{s}$, and across specific wavelength bands, i.e. Blue ($\lambda \leq 510 ~\mathrm{nm}$), Green ($510 \leq \lambda \leq 705 ~\mathrm{nm}$), and near-infrared (NIR) ($705 \leq \lambda \leq 850 ~\mathrm{nm}$). The objective is to calculate the emission intensity in photons per second ($\mathrm{pps}$), which serves as a standard for model validation against experimental observations.

### Neural network model
