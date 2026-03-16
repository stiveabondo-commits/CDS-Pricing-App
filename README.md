# Credit Default Swap (CDS) - Pricing & Risk Analytics POC

 **Live Demo:** [Click here to access the interactive Streamlit Web App]([https://cds-pricing-emmanuel.streamlit.app])

This repository contains a Proof of Concept (POC) demonstrating the operational deployment of a Credit Default Swap (CDS) pricer. It bridges quantitative credit risk modeling with an interactive, production-ready web interface.

## Objective
Provide a real-time risk analytics dashboard that computes the Mark-to-Market (MtM) of a CDS contract and models the reference entity's implied survival curve using a reduced-form intensity model.

##  Key Features
- **Interactive Pricing Engine:** Real-time calculation of the Premium Leg and Protection Leg Present Values (PV) based on dynamic market inputs (Credit Spread, Recovery Rate, Risk-Free Rate).
- **Hazard Rate Modeling:** Extraction of implied hazard rates ($\lambda$) and generation of continuous survival and cumulative default probability curves.
- **Marginal Default Analytics:** Visualization of quarterly marginal default densities and detailed cashflow schedules.
- **Production Deployment:** Fully deployed via Streamlit Community Cloud, demonstrating capabilities in operationalizing mathematical models.

##  Technologies
`Python`, `Streamlit`, `NumPy`, `Pandas`, `Plotly`, `Quantitative Finance`
