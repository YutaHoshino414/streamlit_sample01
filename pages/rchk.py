import streamlit as st
import time
import pandas as pd
import rich
import tkinter as tk
from tkinter import filedialog
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from streamlit_navigation_bar import st_navbar

import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

setting = os.environ.__getitem__('DISPLAY')
#------------------------------------ Set up tkinter ----------
root = tk.Tk(screenName = setting)
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
    //.block-container{padding:4rem 2rem 10rem !important;}
    
    *::-webkit-scrollbar:horizontal{
        height:8px !important;
    }
    *::-webkit-scrollbar-thumb {
        background: rgb(255,75,75,0.8) !important; 
    }
    *::-webkit-scrollbar-button{
        
    }
    div[data-testid="stExpander"] details{
        box-shadow: 10px 10px 15px -10px gray;
    }
    .stTabs div[data-testid="stDataFrame"]{
        box-shadow: 10px 10px 15px -10px gray;
    }
</style>
""")                      

def show_progress_bar():
    progress_text = "Operation in progress.."
    my_bar = st.progress(
        0, text=progress_text)
    
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

#---------------------------------------------------------------------------------
if 'rchk' not in st.session_state:
    st.session_state['rchk'] = ''
if 'member' not in st.session_state:
    st.session_state['member'] = ''

with st.sidebar:
    option = st.selectbox(
        "",
        ("location1", "location2", "location3"),
        index=None,
        placeholder="Choose a location..",
        disabled=True
    )
    
    clicked = st.button('📑select rchk.csv',type="primary")
    if clicked:
        dirname = filedialog.askopenfilename(
            master=root,
            filetypes=[('data files','*.csv')] #filetypes=[('data files','*.csv;*.txt')]
        )
        print(len(dirname))
        if len(dirname) > 0:
            #---------------------------------------------
            st.session_state['rchk'] = dirname
            #---------------------------------------------
            show_progress_bar()
            #---------------------------------------------
    
    st.caption(f"selected: {st.session_state.rchk}")
    st.divider()
    st.caption(f"member file: {st.session_state.member}")
#--------------------------------------------------------------
if 'rchk.csv' in st.session_state.rchk:
    #st.write('file: `%s`' % dirname)
    rchk_path  = st.session_state['rchk']
    df         = pd.read_csv(rchk_path,encoding="cp932",header=None)
    df         = df.fillna("0:00:00")
    df.columns = [f"col_{i}" for i in range(len(df.columns))]
    df.rename(
            columns={'col_0':'No','col_1':'Name','col_2':'Count'},
            inplace=True
        )
    if len(st.session_state.member) > 0:
        df_member         = pd.read_csv(st.session_state.member,encoding="cp932")
        df_member.columns = ["Tagid","No","Name","Age","Gender","Address","Start","Category","Div","Yomi"]
        df_merged         = pd.merge(df_member[["No","Category","Name"]],df,how="left",on=["No","Name"])
        print(df_merged)
    else:
        df_merged = pd.DataFrame() #空df
else:
    df        = pd.DataFrame() #空df
    df_lap    = pd.DataFrame() #空df
    df_merged = pd.DataFrame() #空df

print(len(df))

#----------------------------------------------------------------
gb = GridOptionsBuilder.from_dataframe(df_merged)
#https://streamlit-aggrid.readthedocs.io/en/docs/GridOptionsBuilder.html
gb.configure_pagination(
    paginationPageSize=40,
    paginationAutoPageSize=False
)

#^^^^^^
#Is there a way to autosize all columns by default (on rendering) with streamlit???
#https://discuss.streamlit.io/t/is-there-a-way-to-autosize-all-columns-by-default-on-rendering-with-streamlit-aggrid/31841/7

other_options = {'suppressColumnVirtualisation': True}
gb.configure_grid_options(**other_options)

#^^^^^^
#Is there a way to set the row height?
gb.configure_grid_options(rowHeight=25)
#gb.configure_columns(["No","Name","Count"], cellStyle={'color': 'blue'})
#^^^^^^^
#https://discuss.streamlit.io/t/ag-grid-component-with-input-support/8108/91?page=5
gridOptions = gb.build()

#------pinned by default---------
if len(df) > 0:
    # #https://discuss.streamlit.io/t/st-dataframe-columns-freeze/53781/2
    gridOptions["columnDefs"][0]["pinned"] = "left"
    gridOptions["columnDefs"][0]["width"] = "50"
    gridOptions["columnDefs"][1]["pinned"] = "left"
    gridOptions["columnDefs"][2]["pinned"] = "left"
    for i,colDef in enumerate(gridOptions["columnDefs"][6:22]):
        if i==0 or (i % 2 == 1):
            colDef["cellStyle"] =  {'background-color': 'rgba(0, 107, 36, 0.2)'}
        else:
            colDef["cellStyle"] =  {'background-color': 'rgba(0, 107, 36, 0.1)'}

    gridOptions["defaultColDef"]["width"]= "75"
    
    rich.print(gridOptions["columnDefs"])
    rich.print(gridOptions["defaultColDef"])
    #---------------------------------------------------------------------aggrid
    # #https://discuss.streamlit.io/t/how-to-use-custom-css-in-ag-grid-tables/26743/5
    custom_css = {
        ".ag-tabs-body":{"min-height":"120px","font-size":"14px"},
        ".ag-picker-field-wrapper":{"height":"30px",},
        ".ag-input-field-input":{"height":"40px"},
        ".ag-popup-child":{"font-size":"15px","padding":"5px"},
        ".ag-header-cell":{"background":"rgb(187,187,187,0.1)"},
        ".ag-paging-panel":{"border":"1px solid #FF4B4B","background":"rgb(255, 75, 75,0.1)"}
    }
    with st.expander("Ag-grid Table Filters",expanded=True):
        return_grid = AgGrid(
            df_merged,
            gridOptions=gridOptions,
            height=320,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
            custom_css=custom_css,
            
            )
else:
    with st.expander("Ag-grid Table Filters"):
        return_grid = AgGrid(df,height=100)
print("----returned--------------",return_grid)
#--------------------------------------------------------------------- make lap df
df_copy    = return_grid.data.copy()
df_lap     = df_copy[df_copy.columns[:4]]
previous   = ""
#td = datetime.timedelta()
#print(td)
for i, (col, series) in enumerate(df_copy.items()):
    print(col,"-----",i)
    
    if i >= 6:
        df_copy[col] = pd.to_datetime(series,format="%H:%M:%S")
        #print(df_copy[col])
#        #print(f"previous--------{previous}")
        if i > 6:
            col_name = f"lap{i-6}"
            lap      = df_copy[col] - previous
            lap.name = col_name
            lap_sec  = lap.dt.total_seconds()
            rich.print(lap_sec % 60)
            lap_s    = lap_sec.where(lap_sec>0, other=0)
            df_lap   = pd.concat([df_lap,lap_s],axis=1)
            
        previous = df_copy[col]

import seaborn as sns
cm    = sns.light_palette("seagreen", as_cmap=True)
c_map = sns.diverging_palette(220,25,l=45,as_cmap=True)

df_style = df_lap.style.background_gradient(
            axis=1,
            cmap=cm,
            subset=df_lap.columns[4:19],
        ).background_gradient(
            axis=1,
            cmap=c_map ,
            subset=df_lap.columns[19:],
        ).highlight_between(
            left=2000,
            right=10000,
            color='orange',
            axis=1,
            subset=df_lap.columns[4:19]
        ).highlight_between(
            left=0,
            right=1,
            color='#FFF',
            axis=1,
            subset=df_lap.columns[4:]
        ).set_properties(
            **{'background-color': 'rgb(187,187,187,0.15)', # 背景
                'color': '#b3b3b3', # 文字色
                'border-color': 'white', # 枠の色っぽいが、変わってない？
                'align':'left'},subset=["No","Name","Count"]
        ).format(precision=0)

#----------------------------------------------------------------------
from st_aggrid import JsCode
tab1, tab2, tab3, tab4 = st.tabs(["rchk.csv(Lap/seconds)", "🚩rchk.csv(+member)","🚩rchk.csv(original)", "other"])

with tab1:
    if len(df) > 0:
        st.dataframe(df_style,height=600)
        #---------------------------------------------------------
        #gbuilder = GridOptionsBuilder.from_dataframe(df_lap)
        #other_options = {'suppressColumnVirtualisation': True}
        #gbuilder.configure_grid_options(**other_options)
        #gOptions = gbuilder.build()
        #
        #rich.print(gOptions["columnDefs"][4]) #[4]["tooltipValueGetter"]=
        #AgGrid(df_lap,gridOptions=gOptions)
        #---------------------------------------------------------


    else:
        st.write('select a file..')


with tab2:
    st.dataframe(return_grid.data.style.format(precision=0),height=500)



with tab3:
    st.dataframe(df.style.format(precision=0),height=500)