# NP
Judd-Ofelt theory based, DFT-assisted computational model of NP


The Monte Carlo model, which is currently in the refinement stage to ensure its predictions accurately mirror experimental findings. It integrates several critical components and reasonable assumption to simulate the complex transition behaviors of UCNPs with high fidelity:

### Ion spatial distribution


The model conceptualizes nanoparticles as hexagonal crystal structures($\beta$-phase), where $\mathrm{Yb^{3+}}$ or $\mathrm{Tm^{3+}$} ions are randomly distributed. This approach not only captures the inherent spatial relationships characteristic of hexagonal crystallinity but also facilitates a realistic representation of ion dispersion within the nanoparticle matrix.


### Critical interacting distance $R_0$


Acknowledging the inverse sixth power dependence of the energy transfer rate on the inter-ionic distance ($R$), the model introduces a critical interaction distance $R_0=1 ~\mathrm{nm}$. This pragmatic adjustment allows for the efficient simulation of ion interactions by limiting the consideration of effective neighbors to those within this defined radius, thus optimizing computational resources without compromising the model's integrity.



### High energy levels truncation 


Our simulations reveal that very few population inhabit in higher energy levels that have negligible contribution to the desired emission, and we have decided to truncate higher energy levels so that computational complexity can be also reduced. Meanwhile manually restricting the transition options for different ions at different levels.


### Probabilistic process modeling


The simulation timescale operates over $T=1~ \mathrm{s}$, segmented into nanosecond increments $\Delta t=1 ~\mathrm{us}$ yielding a comprehensive resolution of $1 \times 10^6$ steps. Each step assesses the state of excited sensitizer $\mathrm{Yb^{3+}}$ and emitter $\mathrm{Tm^{3+}}$ and their immediate neighbors within $R_0$, determining the subsequent mutual competitive energy transfer events, through a probabilistic comparison between a generated random number \textbf{$p_i$}, and established all transition rates $W=\{\mathrm{ED+MD}, \mathrm{Up}-\mathrm{conversion}, \mathrm{Cross}-\mathrm{relaxation}, \mathrm{Stay}\}$.


### Emission transition selection


A pivotal aspect of the simulation involves tracking and quantifying transition events over time: $10^6$ steps with $\Delta t= 1~\mathrm{us}, T=1~ \mathrm{s}$, and across specific wavelength bands, i.e. Blue ($\lambda \leq 510 ~\mathrm{nm}$), Green ($510 \leq \lambda \leq 705 ~\mathrm{nm}$), and near-infrared (NIR) ($705 \leq \lambda \leq 850 ~\mathrm{nm}$). The objective is to calculate the emission intensity in photons per second ($\mathrm{pps}$), which serves as a standard for model validation against experimental observations.
