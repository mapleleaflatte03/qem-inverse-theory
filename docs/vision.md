# Vision

Zero-noise extrapolation is the most widely deployed quantum error mitigation technique, yet its theoretical foundations remain surprisingly thin. The standard approach—fit a curve to noisy data, extrapolate to zero noise—is treated as a regression problem. But it is fundamentally an inverse problem: recovering an unobserved quantity (the noiseless expectation) from indirect, noisy measurements.

This project develops the mathematical framework to understand:

1. When this inverse problem is well-posed (identifiable)
2. When finite-shot constraints make mitigation harmful
3. What physical structure restores identifiability
4. How to quantify uncertainty in the zero-noise estimate

The long-term goal is a rigorous theory of "when to mitigate" that complements the existing engineering of "how to mitigate."
