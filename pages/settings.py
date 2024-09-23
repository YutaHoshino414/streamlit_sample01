import os
import pandas as pd

import streamlit as st
import tkinter as tk
from tkinter import filedialog
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode

#------------------------------------ Set up tkinter ----------
root = tk.Tk()
root.withdraw()

# Make folder picker dialog appear on top of other windows
root.wm_attributes('-topmost', 1)
#--------------------------------------------------------------
st.html("""
<style>
    *{
        font-size:14px !important;
        }
    body{
        line-height:1.5;
    }
    header{
        height:10px !important;
    }
    .block-container{padding:4rem 4rem 10rem !important;}
    
    *::-webkit-scrollbar:horizontal{
        height:8px !important;
    }
    *::-webkit-scrollbar-thumb {
        background: rgb(255,75,75,0.8) !important; 
    }
    *::-webkit-scrollbar-button{
        
    }
    
    .stTabs .element-container > iframe{
        box-shadow: 10px 10px 15px -10px gray;
    }
</style>
""")   
#----------------------------------------------------------
def validate_file(file_path):
    print(file_path)
    basename = os.path.basename(file_path)
    if len(file_path) == 0:
        st.write("file not selected..")
    elif "member.csv" == basename or "member.txt"==basename:
        #---------------------------------------------
        st.session_state['member'] = file_path
        df = pd.read_csv(file_path,encoding="cp932")
        df.columns = ["Tagid","No","Name","Age","Gender","Address","Start","Category","Div","Yomi"]
        
        return df
#----------------------------------------------------------

df = pd.DataFrame()
if 'member' not in st.session_state:
    st.session_state['member'] = ''
    st.session_state['root_path'] = ''
else:
    if len(st.session_state.member) > 0:
        df = pd.read_csv(st.session_state.member,encoding="cp932")
        df.columns = ["Tagid","No","Name","Age","Gender","Address","Start","Category","Div","Yomi"]
        
        st.session_state['root_path'] = os.path.dirname(st.session_state.member)


with st.sidebar:
    #st.info(st.session_state.root_path)
    clicked = st.button('Choose a member file')
    if clicked:
        file_path = filedialog.askopenfilename(
                master=root,
                filetypes=[('data files','*.csv;*.txt')] #filetypes=[('data files','*.csv;*.txt')]
            )
        df = validate_file(file_path)


tab1, tab2, tab3, tab4 = st.tabs(["👥Member", "📍Locations", "👟Rchk", "Other"])
with tab1:
    #----------------------------------------------------------
    gb = GridOptionsBuilder.from_dataframe(df)
    other_options = {'suppressColumnVirtualisation': True}
    gb.configure_grid_options(**other_options)
    gb.configure_side_bar()
    gridOptions = gb.build()
    #gridOptions["defaultColDef"]["width"]= "100"
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True)
    #----------------------------------------------------------
    df_grid = AgGrid(
        df,
        gridOptions=gridOptions,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        #columns_state=columns_state,
        update_on=["stateUpdated"]
    )
    st.write(df_grid.columns_state)
    

#with tab2:
#    root_path = st.session_state.root_path
#    lacation_list = [dire for dire in os.listdir(root_path)if os.path.isdir(f"{root_path}/{dire}")]
#    st.write(lacation_list)
