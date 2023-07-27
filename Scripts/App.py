import pandas as pd

import streamlit as st
from streamlit_option_menu import option_menu

from VisualizeAssemblyLine import visualize
from Solver import solve


def main():
    st.title("Assembly line balancing")

    st.sidebar.subheader("File Upload")
    tasksFile = st.sidebar.file_uploader("Upload your excel file describing the tasks")

    st.sidebar.subheader("File Upload")
    assemblyLineFile = st.sidebar.file_uploader("Upload your excel file describing the assembly line")

    if tasksFile is not None and assemblyLineFile is not None:
        tasksDataFrame = applyModificationsToData(tasksFile)
        assemblyLineDataFrame = applyModificationsToData(assemblyLineFile)
        
        
        with st.container():
            selectedPage = option_menu(
                menu_title=None,
                options=["Home", "Unbalanced graph", "Solver", "Results"],
                icons=['house', 'bar-chart', 'gear', 'clipboard-check'],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
                styles={
                    "container": {"display": "flex", "flex-wrap": "wrap", "padding": "0", "margin": "0", "list-style-type": "none", "max-width": "100%"},
                    "nav-item": {"flex": "1 1 auto", "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis"},
                    "nav-link": {"width": "100%", "padding": "8px 0"},
                }
            )

            if selectedPage == 'Home':
                renderHome(tasksDataFrame, assemblyLineDataFrame)
                
            elif selectedPage == 'Unbalanced graph':
                visualize(tasksDataFrame, assemblyLineDataFrame)
                
            elif selectedPage == 'Solver':
                metaData = prepareTheDataForTheSolver()
                if st.button('SOLVE'):
                    solve(tasksDataFrame, assemblyLineDataFrame, metaData)


def applyModificationsToData(dataFrame):
    newDataFrame = pd.read_excel(dataFrame)
    newDataFrame.index = newDataFrame.index + 1
    newDataFrame = newDataFrame.astype(str)

    return newDataFrame
                

def renderHome(tasksDataFrame, assemblyLineDataFrame):
    st.write("### Your data")
    column1, column2 = st.columns([0.6, 0.4])

    with column1:
        st.write("Tasks description")
        st.table(tasksDataFrame)

    with column2:
        st.write("Assembly line nodes")
        st.table(assemblyLineDataFrame)
        
        
def prepareTheDataForTheSolver():
    method = st.selectbox(
        'Choose a method to solve the problem',
        ('RPW', 'SPT'))
    
    timeUnit = st.radio("What\'s your time unit?",
                        ('Hours (h)', 'Minutes (m)', 'Seconds (s)'),
                        horizontal=True)
    
    taktTime = st.number_input(f'Specify the takt time in {timeUnit}')
    
    return {
        'method': method,
        'timeUnit': timeUnit,
        'taktTime': taktTime,
    }
    
            
if __name__ == "__main__":
    main()
        