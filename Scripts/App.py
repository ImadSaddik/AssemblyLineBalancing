import pandas as pd

from PIL import Image

import streamlit as st
from streamlit_option_menu import option_menu

from Visualizer import visualize, getGraph, plotStackedBarChart, plotStackedBarChart
from Solver import solve
from Report import showReport, saveReport


if 'reportMetaData' not in st.session_state:
    st.session_state.reportMetaData = {}


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
                options=["Home", "Unbalanced graph", "Solver", "Reports"],
                icons=['house', 'diagram-3', 'gear', 'clipboard-check'],
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
                metaData = prepareDataForSolver()
                if st.button('SOLVE'):
                    if metaData['taktTime'] > 0:
                        reportMetaData = canSolve(metaData, tasksDataFrame, assemblyLineDataFrame)
                        st.session_state.reportMetaData = reportMetaData
                    else:
                        st.warning('Takt time should be > 0', icon="⚠️")

            else:
                showReport(st.session_state.reportMetaData)
                report = saveReport(st.session_state.reportMetaData)
                stringBuilder = "".join(line + '\n' for line in report)
                st.download_button('Download report', stringBuilder, 'report.txt')
                

def canSolve(metaData, tasksDataFrame, assemblyLineDataFrame):
    balancedGraph = solve(tasksDataFrame, assemblyLineDataFrame, metaData)
    unBalancedGraph = getGraph(tasksDataFrame, assemblyLineDataFrame)
    
    solveAndVisualize(balancedGraph, metaData, prefix='Balanced')
    solveAndVisualize(unBalancedGraph, metaData, prefix='Unbalanced')
    
    return {
        'balancedGraph': balancedGraph,
        'unBalancedGraph': unBalancedGraph,
        'demand': metaData['demand'],
        'taktTime': metaData['taktTime'],
        'totalWorkTime': metaData['totalWorkTime'],
        'timeUnit': metaData['timeUnit'],
    }


def solveAndVisualize(graph, metaData, prefix):
    graphMetaData = getGraphMetaData(graph, metaData['taktTime'], titlePrefix=prefix)
    plotStackedBarChart(graphMetaData)
    

def getGraphMetaData(graph, taktTime, titlePrefix):
    taskTimes = [graph.nodes[i].get('weight') for i in graph.nodes]
    idleTimes = [taktTime - j for j in taskTimes]

    return {
        'taskTimes': taskTimes,
        'idleTimes': idleTimes,
        'title': f'{titlePrefix} assembly line with task times and idle times',
        'xTickLabels': list(graph.nodes.keys()),
        'xLabel': 'Tasks',
        'yLabel': 'Processing time',
    }
    

def applyModificationsToData(dataFrame):
    newDataFrame = pd.read_excel(dataFrame)
    newDataFrame.index = newDataFrame.index + 1
    newDataFrame = newDataFrame.astype(str)

    return newDataFrame
                

def renderHome(tasksDataFrame, assemblyLineDataFrame):
    st.write("### Your data")
    column1, column2 = st.columns([0.7, 0.3])

    with column1:
        st.write("Tasks description")
        st.dataframe(tasksDataFrame, use_container_width=True)

    with column2:
        st.write("Assembly line nodes")
        st.dataframe(assemblyLineDataFrame, use_container_width=True)
        
        
def prepareDataForSolver():
    method = st.selectbox(
        'Choose a method to solve the problem',
        ('RPW', 'SPT'))
    
    timeUnit = st.radio("What\'s your time unit?",
                        ('Hours (h)', 'Minutes (m)', 'Seconds (s)'),
                        horizontal=True)
    timeMultiplier = {'Hours (h)': 1, 'Minutes (m)': 60, 'Seconds (s)': 3600}
    
    column1, column2 = st.columns(2)
    with column1:
        totalWorkTimeInHours = st.number_input('Specify the total work time in Hours (h)')
        totalTimeByUnit = totalWorkTimeInHours * timeMultiplier[timeUnit]
        
    with column2:
        demand = st.number_input('Specify the total demand', min_value=1)
    
    return {
        'method': method,
        'taktTime': (totalTimeByUnit / demand),
        'demand': demand,
        'totalWorkTime': totalTimeByUnit,
        'timeUnit': timeUnit,
    }
    
            
if __name__ == "__main__":
    main()
        