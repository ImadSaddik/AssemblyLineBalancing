import streamlit as st

from PIL import Image
import numpy as np

import matplotlib.pyplot as plt
import plotly.graph_objects as go

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph


def visualize(tasksData, edgesData):    
    graph = getGraph(tasksData, edgesData)
    outputPath = '../Output/og.png'
    plotGraph(graph, outputPath)
    
    unbalancedGraphImage = Image.open(outputPath)
    st.markdown("<br>", unsafe_allow_html=True)
    st.image(unbalancedGraphImage, caption="Unbalanced line")
    
    
def getGraph(tasksData, edgesData):
    fromNodes = edgesData[edgesData.columns[0]].tolist()
    toNodes = edgesData[edgesData.columns[1]].tolist()

    taskNames = tasksData[tasksData.columns[0]].tolist()
    taskTimes = tasksData[tasksData.columns[1]].tolist()
    
    return populateGraph(fromNodes, toNodes, taskNames, taskTimes)
    

def populateGraph(fromNodes, toNodes, taskNames, taskTimes):
    graph = nx.DiGraph()
    graph.add_nodes_from([str(i) for i in range(1, len(taskTimes)+1)])
    [graph.add_edges_from([ [fromNode, toNode] ]) for fromNode, toNode in zip(fromNodes, toNodes)]
    
    nx.set_node_attributes(graph, { str(i): {'name':taskNames[i-1]} for i in range(len(taskNames)+1)})
    nx.set_node_attributes(graph, { str(i): {'weight':float(taskTimes[i-1])} for i in range(len(taskTimes)+1)})
    nx.set_node_attributes(
        graph,
        {
            str(i): {'label': f"{str(i)}-({str(taskTimes[i - 1])})"}
            for i in range(1, len(taskTimes) + 1)
        },
    )
    
    return graph


def plotGraph(graph, outputPath):
    graph.graph['graph']={'rankdir': 'LR'} 
    graph.graph['node'] = {'shape': 'circle'}
    graph.graph['edges'] = {'arrowsize': '2.0'}
    graph.graph['labelloc'] = "t"
    graph.graph['fontsize'] = 20
    
    aGraph = to_agraph(graph)
    aGraph.layout('dot')
    aGraph.draw(outputPath)
    

def plotStackedBarChart(metaData):
    n = len(metaData['taskTimes'])
    indices = list(range(1, n+1))

    taskTimes = metaData['taskTimes']
    idleTimes = metaData['idleTimes']

    maxYVal = max(taskTimes[k] + idleTimes[k] for k in range(n))
    numExp = int(np.floor(np.log10(np.abs(maxYVal))) + 1)
    maxYExp = numExp + 1

    fig = go.Figure()

    fig.add_trace(go.Bar(x=indices, y=taskTimes, name='Task time', marker_color='blue'))
    fig.add_trace(go.Bar(x=indices, y=idleTimes, name='Idle time', marker_color='lime', base=taskTimes))

    fig.update_layout(
        title=metaData['title'],
        xaxis=dict(
            tickvals=indices,
            ticktext=metaData['xTickLabels'],
            title=metaData['xLabel']
        ),
        yaxis=dict(
            title=metaData['yLabel'],
            tickvals=np.arange(0, maxYVal + 10 ** (maxYExp - 1), 10 ** (maxYExp - 1)),
            gridcolor='lightgray'
        ),
        barmode='stack',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            xanchor='center',
            y=1.02,
            x=0.5
        )
    )

    fig.add_shape(
        type='line',
        x0=0,
        y0=maxYVal,
        x1=max(indices)+1,
        y1=maxYVal,
        line=dict(
            color='white',
            dash='dash'
        )
    )

    fig.add_annotation(
        x=0,
        y=maxYVal+0.1,
        text="Takt time: {:.2f}".format(maxYVal),
        showarrow=False,
        xshift=-15
    )
    
    st.plotly_chart(fig)
