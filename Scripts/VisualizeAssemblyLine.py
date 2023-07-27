import streamlit as st

from PIL import Image

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
        