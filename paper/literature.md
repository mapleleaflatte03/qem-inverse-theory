# Literature and Citations

## Citation Audit Status

**This file is a citation scaffold, not a final bibliography.**
Entries marked VERIFY must be checked against official sources (arXiv, DOI, publisher) before use in any submission.

---

Citation keys for use in `draft.md`. To be converted to BibTeX for final submission.

---

## Foundational ZNE

**[LiBenjamin2017]**
Y. Li, S. C. Benjamin. "Efficient Variational Quantum Simulator Incorporating Active Error Minimization." Physical Review X 7, 021050 (2017).
*Why:* Original proposal of extrapolation-based error mitigation.

**[Temme2017]**
K. Temme, S. Bravyi, J. M. Gambetta. "Error Mitigation for Short-Depth Quantum Circuits." Physical Review Letters 119, 180509 (2017).
*Why:* Introduces probabilistic error cancellation and quasi-probability extrapolation.

**[GiurgicaTiron2020]**
T. Giurgica-Tiron, Y. Hindy, R. LaRose, A. Mari, W. J. Zeng. "Digital Zero Noise Extrapolation for Quantum Error Mitigation." VERIFY: IEEE International Conference on Quantum Computing and Engineering (QCE), 2020. Exact proceedings details to be confirmed.
*Why:* Digital ZNE via unitary folding — the standard implementation method.

---

## Quantum Error Mitigation Reviews

**[Cai2023]**
Z. Cai, R. Babbush, S. C. Benjamin, S. Endo, W. J. Huggins, Y. Li, J. R. McClean, T. E. O'Brien. "Quantum Error Mitigation." VERIFY: Reviews of Modern Physics 95, 045005 (2023). Exact author list and volume to be confirmed.
*Why:* Comprehensive review covering ZNE, PEC, and their limitations.

**[Endo2021]**
S. Endo, Z. Cai, S. C. Benjamin, X. Yuan. "Hybrid Quantum-Classical Algorithms and Quantum Error Mitigation." VERIFY: Journal of the Physical Society of Japan 90, 032001 (2021). Exact venue/volume to be confirmed.
*Why:* Review connecting QEM to variational algorithms.

---

## QEM Lower Bounds / Sample Complexity

**[Takagi2022]**
R. Takagi, S. Endo, S. Minagawa, M. Gu. "Fundamental Limitations of Quantum Error Mitigation." npj Quantum Information 8, 114 (2022).
*Why:* Proves exponential sampling overhead for generic QEM. Key lower bound.

**[Quek2024]**
Y. Quek, D. S. França, S. Khatri, J. J. Meyer, J. Eisert. VERIFY: exact title, venue, and year. Believed to be published in Nature Physics 2024 but details unconfirmed.
*Why:* Tighter exponential bounds on QEM. Identifies assumptions under which bounds apply.

**[Tsubouchi2023]**
K. Tsubouchi, T. Sagawa, N. Yoshioka. "Universal Cost Bound of Quantum Error Mitigation Based on Quantum Estimation Theory." VERIFY: Physical Review Letters 131, 210601 (2023). Volume/page to be confirmed.
*Why:* Universal cost framework connecting QEM to estimation theory.

---

## Inverse Problems / Hadamard Well-Posedness

**[Hadamard1902]**
J. Hadamard. "Sur les problèmes aux dérivées partielles et leur signification physique." VERIFY: Princeton University Bulletin 13, 49–52 (1902). Exact publication details to be confirmed.
*Why:* Original definition of well-posedness (existence, uniqueness, stability).

**[Tikhonov1963]**
A. N. Tikhonov. "Solution of Incorrectly Formulated Problems and the Regularization Method." Soviet Mathematics Doklady 4, 1035–1038 (1963).
*Why:* Foundational regularization theory for ill-posed inverse problems.

**[Hansen1998]**
P. C. Hansen. "Rank-Deficient and Discrete Ill-Posed Problems." SIAM (1998).
*Why:* Numerical methods for discrete inverse problems. Relevant to polynomial extrapolation.

---

## Constrained Estimation / Projection

**[Miranskyy2026]**
A. Miranskyy, L. Zhang, J. Doliskani. "Physically Constrained Zero-Noise Extrapolation." VERIFY: arXiv:2604.24475 (April 2026). Exact author list and title to be confirmed.
*Why:* Bounded ZNE with model selection on 180K circuits. Direct predecessor.

**[Boyd2004]**
S. Boyd, L. Vandenberghe. "Convex Optimization." Cambridge University Press (2004).
*Why:* Theory of constrained optimization, projection onto convex sets.

**[Duchi2008]**
J. Duchi, S. Shalev-Shwartz, Y. Singer, T. Chandra. "Efficient Projections onto the ℓ1-Ball for Learning in High Dimensions." ICML (2008).
*Why:* Simplex projection algorithm used in probability constraints.

---

## Bayesian Inverse Problems / Uncertainty

**[Stuart2010]**
A. M. Stuart. "Inverse Problems: A Bayesian Perspective." Acta Numerica 19, 451–559 (2010).
*Why:* Foundational framework for Bayesian treatment of inverse problems.

**[Ferrie2014]**
C. Ferrie. "Self-Guided Quantum Tomography." VERIFY: Physical Review Letters 113, 190404 (2014). Volume/page to be confirmed.
*Why:* Bayesian approach to quantum state estimation.

**[Rasmussen2006]**
C. E. Rasmussen, C. K. I. Williams. "Gaussian Processes for Machine Learning." MIT Press (2006).
*Why:* GP regression theory underlying Bayesian ZNE prototype.

---

## Model Selection

**[Akaike1974]**
H. Akaike. "A New Look at the Statistical Model Identification." IEEE Transactions on Automatic Control 19, 716–723 (1974).
*Why:* Original AIC.

**[HurvichTsai1989]**
C. M. Hurvich, C.-L. Tsai. "Regression and Time Series Model Selection in Small Samples." Biometrika 76, 297–307 (1989).
*Why:* AICc correction for small samples — critical for ZNE with n ≤ 7.

**[BurnhamAnderson2002]**
K. P. Burnham, D. R. Anderson. "Model Selection and Multimodel Inference." Springer (2002).
*Why:* Comprehensive treatment of information-theoretic model selection.
