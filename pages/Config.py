from __future__ import annotations

import streamlit as st

from config_module import render_dealer_config
from db import init_db, seed_dealers

init_db()
seed_dealers()

st.set_page_config(page_title="Config", layout="centered")
render_dealer_config()
