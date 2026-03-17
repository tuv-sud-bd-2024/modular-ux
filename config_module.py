from __future__ import annotations

import sqlite3

import streamlit as st

from db import add_dealer, delete_dealer, list_dealers, update_dealer


def _dealer_label(dealer: dict) -> str:
    return f"{dealer['dealer_name']} ({dealer['dealer_code']})"


def render_dealer_config() -> None:
    st.subheader("Config Module: Dealer Management")

    dealers = list_dealers()
    if dealers:
        st.dataframe(dealers, use_container_width=True, hide_index=True)
    else:
        st.info("No dealers configured yet.")

    add_tab, edit_tab, delete_tab = st.tabs(["Add", "Edit", "Delete"])

    with add_tab:
        with st.form("add_dealer_form", clear_on_submit=True):
            dealer_name = st.text_input("Dealer Name")
            dealer_code = st.text_input("Dealer Code")
            is_on_leave = st.checkbox("Is On Leave", value=False)
            single_transaction_limit = st.number_input("Single Transaction Limit", min_value=0.0, step=1.0)
            daily_limit = st.number_input("Daily Limit", min_value=0.0, step=1.0)
            yearly_limit = st.number_input("Yearly Limit", min_value=0.0, step=1.0)
            primary_user = st.checkbox("Primary User", value=True)
            submitted = st.form_submit_button("Add Dealer")

            if submitted:
                if not dealer_name.strip() or not dealer_code.strip():
                    st.error("Dealer Name and Dealer Code are required.")
                elif single_transaction_limit <= 0:
                    st.error("Single Transaction Limit must be greater than zero.")
                else:
                    try:
                        add_dealer(
                            dealer_name,
                            dealer_code,
                            is_on_leave,
                            single_transaction_limit,
                            daily_limit,
                            yearly_limit,
                            primary_user,
                        )
                        st.success("Dealer added.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Dealer Code must be unique.")

    with edit_tab:
        if not dealers:
            st.info("Add dealers first to edit.")
        else:
            index_map = {_dealer_label(dealer): dealer for dealer in dealers}
            selected_label = st.selectbox("Select Dealer", options=list(index_map.keys()), key="edit_dealer_select")
            selected_dealer = index_map[selected_label]

            with st.form("edit_dealer_form"):
                dealer_name = st.text_input("Dealer Name", value=str(selected_dealer["dealer_name"]))
                dealer_code = st.text_input("Dealer Code", value=str(selected_dealer["dealer_code"]))
                is_on_leave = st.checkbox("Is On Leave", value=bool(selected_dealer["is_on_leave"]))
                single_transaction_limit = st.number_input(
                    "Single Transaction Limit",
                    min_value=0.0,
                    step=1.0,
                    value=float(selected_dealer["single_transaction_limit"]),
                )
                daily_limit = st.number_input(
                    "Daily Limit",
                    min_value=0.0,
                    step=1.0,
                    value=float(selected_dealer["daily_limit"]),
                )
                yearly_limit = st.number_input(
                    "Yearly Limit",
                    min_value=0.0,
                    step=1.0,
                    value=float(selected_dealer["yearly_limit"]),
                )
                primary_user = st.checkbox("Primary User", value=bool(selected_dealer["primary_user"]))

                submitted = st.form_submit_button("Update Dealer")
                if submitted:
                    if not dealer_name.strip() or not dealer_code.strip():
                        st.error("Dealer Name and Dealer Code are required.")
                    elif single_transaction_limit <= 0:
                        st.error("Single Transaction Limit must be greater than zero.")
                    else:
                        try:
                            update_dealer(
                                int(selected_dealer["id"]),
                                dealer_name,
                                dealer_code,
                                is_on_leave,
                                single_transaction_limit,
                                daily_limit,
                                yearly_limit,
                                primary_user,
                            )
                            st.success("Dealer updated.")
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("Dealer Code must be unique.")

    with delete_tab:
        if not dealers:
            st.info("Add dealers first to delete.")
        else:
            index_map = {_dealer_label(dealer): dealer for dealer in dealers}
            selected_label = st.selectbox("Select Dealer", options=list(index_map.keys()), key="delete_dealer_select")
            selected_dealer = index_map[selected_label]
            if st.button("Delete Dealer", type="secondary"):
                delete_dealer(int(selected_dealer["id"]))
                st.success("Dealer deleted.")
                st.rerun()


def get_dealer_name_options() -> list[str]:
    return [str(item["dealer_name"]) for item in list_dealers()]


def get_dealer_by_name(dealer_name: str) -> dict | None:
    normalized_name = dealer_name.strip().lower()
    for dealer in list_dealers():
        if str(dealer["dealer_name"]).strip().lower() == normalized_name:
            return dealer
    return None
