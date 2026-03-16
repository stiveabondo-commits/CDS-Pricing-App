import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="CDS Pricing POC", page_icon="📈", layout="wide")

st.title("Credit Default Swap (CDS) - Pricing & Risk Analytics")
st.markdown("""
**Auteur:** Emmanuel Abondo Owona | Ce tableau de bord interactif calcule la valorisation simplifiée d'un CDS et modélise la courbe de survie implicite de l'entité de référence en temps réel.
""")

# --- BARRE LATÉRALE : PARAMÈTRES DU MARCHÉ ---
st.sidebar.header("Paramètres de Marché & Contrat")

notional = st.sidebar.number_input("Notionnel (EUR)", min_value=1_000_000, max_value=100_000_000, value=10_000_000, step=1_000_000)
spread_bps = st.sidebar.slider("Spread de Crédit (bps)", min_value=10, max_value=1000, value=150, step=10)
recovery_rate = st.sidebar.slider("Taux de Recouvrement (Recovery Rate %)", min_value=0, max_value=100, value=40, step=5) / 100.0
r = st.sidebar.slider("Taux Sans Risque Continu (%)", min_value=-1.0, max_value=10.0, value=2.0, step=0.1) / 100.0
maturity = st.sidebar.slider("Maturité (Années)", min_value=1, max_value=10, value=5, step=1)

# --- CALCULS MATHÉMATIQUES (Modèle Réduit d'Intensité) ---
spread = spread_bps / 10000.0
# Approximation standard du marché : Taux de Hasard (Lambda) = Spread / (1 - Recovery)
hazard_rate = spread / (1 - recovery_rate) if recovery_rate < 1.0 else 0.0

# Génération de la grille de temps (paiements trimestriels)
dt = 0.25
times = np.arange(dt, maturity + dt, dt)

# Calcul des probabilités et facteurs d'actualisation
survival_probs = np.exp(-hazard_rate * times)
default_probs = 1 - survival_probs
discount_factors = np.exp(-r * times)

# --- CALCUL DES JAMBES DU CDS (Legs) ---
# Premium Leg (Ce que paie l'acheteur de protection)
premium_leg_pv = np.sum(spread * dt * notional * survival_probs * discount_factors)

# Protection Leg (Ce que paie le vendeur en cas de défaut)
# Probabilité marginale de défaut sur chaque trimestre
marginal_default_probs = np.zeros_like(survival_probs)
marginal_default_probs[0] = 1 - survival_probs[0]
for i in range(1, len(survival_probs)):
    marginal_default_probs[i] = survival_probs[i-1] - survival_probs[i]

protection_leg_pv = np.sum((1 - recovery_rate) * notional * marginal_default_probs * discount_factors)

# Mark-to-Market (MtM) pour l'Acheteur de Protection
mtm_buyer = protection_leg_pv - premium_leg_pv

# --- AFFICHAGE DES RÉSULTATS (METRICS) ---
st.markdown("###  Résultats de Valorisation (Mark-to-Market)")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Taux de Hasard implicite (λ)", f"{hazard_rate*100:.2f}%")
col2.metric("Premium Leg PV", f"{premium_leg_pv:,.0f} €")
col3.metric("Protection Leg PV", f"{protection_leg_pv:,.0f} €")
col4.metric("MtM (Acheteur de Protection)", f"{mtm_buyer:,.0f} €", 
            delta="En l'état, le contrat est à parité" if abs(mtm_buyer) < 100 else None)

# --- GRAPHIQUES INTERACTIFS ---
st.markdown("###  Analyse des Probabilités")
colA, colB = st.columns(2)

# Graphique 1 : Courbe de survie vs Courbe de défaut
fig_probs = go.Figure()
fig_probs.add_trace(go.Scatter(x=times, y=survival_probs, mode='lines+markers', name='Probabilité de Survie', line=dict(color='green')))
fig_probs.add_trace(go.Scatter(x=times, y=default_probs, mode='lines+markers', name='Probabilité de Défaut cumulée', line=dict(color='red')))
fig_probs.update_layout(title="Courbes de Survie et de Défaut Implicites", xaxis_title="Années", yaxis_title="Probabilité", yaxis=dict(range=[0,1]))
colA.plotly_chart(fig_probs, use_container_width=True)

# Graphique 2 : Densité de défaut marginale
fig_marginal = go.Figure()
fig_marginal.add_trace(go.Bar(x=times, y=marginal_default_probs, name='Défaut Marginal', marker_color='orange'))
fig_marginal.update_layout(title="Probabilité de défaut par trimestre", xaxis_title="Années", yaxis_title="Probabilité Marginale")
colB.plotly_chart(fig_marginal, use_container_width=True)

# --- TABLEAU DE FLUX ---
with st.expander("Voir l'échéancier détaillé (Cashflows)"):
    df_schedule = pd.DataFrame({
        "Maturité (Années)": times,
        "Facteur d'actualisation": discount_factors,
        "Prob. de Survie": survival_probs,
        "Prob. Marginale de Défaut": marginal_default_probs
    })
    st.dataframe(df_schedule.style.format({
        "Facteur d'actualisation": "{:.4f}",
        "Prob. de Survie": "{:.2%}",
        "Prob. Marginale de Défaut": "{:.2%}"
    }))