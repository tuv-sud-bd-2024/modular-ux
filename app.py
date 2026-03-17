from __future__ import annotations

import streamlit as st

from base_ux import render_base_ux
from db import init_db, seed_dealers

init_db()
seed_dealers()

st.set_page_config(page_title="Base UX", layout="centered")
render_base_ux()
