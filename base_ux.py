from __future__ import annotations

import json

import streamlit as st

from config_module import render_dealer_config
from mini_ux_dealer import render_dealer_mini_ux
from mini_ux_transaction import render_transaction_mini_ux


def render_base_ux() -> None:
    st.title("Base UX")
    render_dealer_config()
    st.divider()

    dealer_name, dealer_code, selected_dealer = render_dealer_mini_ux()
    currency, amount = render_transaction_mini_ux()

    validation_message = ""
    limit_crossed = False

    if selected_dealer is None:
        validation_message = "Select a dealer from the list."
    elif not currency.strip() or amount <= 0:
        validation_message = "Fill Currency and Amount to enable submit."
    else:
        single_limit = float(selected_dealer["single_transaction_limit"])
        if amount > single_limit:
            limit_crossed = True
            validation_message = "Single transaction limit crossed."
        else:
            validation_message = "Single transaction limit check passed."

    if limit_crossed:
        st.error(validation_message)
    elif validation_message and "passed" not in validation_message:
        st.warning(validation_message)
    elif validation_message:
        st.success(validation_message)

    submit_disabled = (
        selected_dealer is None
        or not dealer_name.strip()
        or not dealer_code.strip()
        or not currency.strip()
        or amount <= 0
        or limit_crossed
    )

    if st.button("Submit", disabled=submit_disabled):
        submitted_payload = {
            "dealer_name": dealer_name.strip(),
            "dealer_code": dealer_code.strip(),
            "currency": currency.strip().upper(),
            "amount": amount,
            "single_transaction_limit": float(selected_dealer["single_transaction_limit"]),
        }
        print("Submitted Base UX payload:")
        print(json.dumps(submitted_payload, indent=2))
        st.success("Submitted. Values printed to terminal.")
