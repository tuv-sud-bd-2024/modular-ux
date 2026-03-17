from __future__ import annotations

import streamlit as st


def render_transaction_mini_ux() -> tuple[str, float]:
    st.subheader("Mini UX: Transaction Input")
    currency = st.text_input("Currency")
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    return currency, amount
