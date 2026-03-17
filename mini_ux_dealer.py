from __future__ import annotations

import streamlit as st

from config_module import get_dealer_by_name, get_dealer_name_options


def render_dealer_mini_ux() -> tuple[str, str, dict | None]:
    st.subheader("Mini UX: Dealer Input")

    options = get_dealer_name_options()
    if not options:
        st.warning("No dealers found. Add dealer entries in the Config Module.")
        return "", "", None

    selected_name = st.selectbox("Dealer Name", options=options)
    selected_dealer = get_dealer_by_name(selected_name)

    dealer_code = ""
    if selected_dealer is not None:
        dealer_code = str(selected_dealer["dealer_code"])

    st.text_input("Dealer Code", value=dealer_code, disabled=True)
    return selected_name, dealer_code, selected_dealer
