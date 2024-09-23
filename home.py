import time
import random
import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

# must be the first streamlit call in the file, therefore put it above the st.title
st.set_page_config(layout="wide")
#------------------------------------------------------------------
# タイトルを作成する
st.subheader('Home',divider="rainbow")
st.logo("logo-light.png")
_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 😎
"""

def stream_data():
    
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.05)
    
    lorem_split = _LOREM_IPSUM.split(" ")
    for word in random.sample(lorem_split,len(lorem_split)):
        yield word + " "
        time.sleep(0.05)

    yield pd.DataFrame(
        np.random.randn(5, 8),
        columns=["a", "b", "c", "d", "e", "f", "g", "h",],
    )


st.write_stream(stream_data)
st.balloons()
