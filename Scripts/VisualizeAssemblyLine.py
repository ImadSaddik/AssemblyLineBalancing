import streamlit as st

from PIL import Image

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph


def visualize(tasksData, edgesData):
    fromNodes = edgesData[edgesData.columns[0]].tolist()
    toNodes = edgesData[edgesData.columns[1]].tolist()

    taskNames = tasksData[tasksData.columns[0]].tolist()
    taskTimes = tasksData[tasksData.columns[1]].tolist()
    
    G = nx.DiGraph()
    G.add_nodes_from([str(i) for i in range(1, len(taskTimes)+1)])
    [G.add_edges_from([ [fromNode, toNode] ]) for fromNode, toNode in zip(fromNodes, toNodes)]
    
    nx.set_node_attributes(G, { str(i): {'name':taskNames[i-1]} for i in range(len(taskNames)+1)})
    nx.set_node_attributes(G, { str(i): {'weight':float(taskTimes[i-1])} for i in range(len(taskTimes)+1)})
    nx.set_node_attributes(
        G,
        {
            str(i): {'label': f"{str(i)}-({str(taskTimes[i - 1])})"}
            for i in range(1, len(taskTimes) + 1)
        },
    )
    outputPath = '../Output/og.png'
    plotGraph(G, outputPath)
    
    unbalancedGraphImage = Image.open(outputPath)
    st.markdown("<br>", unsafe_allow_html=True)
    st.image(unbalancedGraphImage, caption="Unbalanced line")
    

def plotGraph(G, ofname):
        G.graph['graph']={'rankdir':'LR'} 
        G.graph['node'] = {'shape':'circle'}
        G.graph['edges'] = {'arrowsize':'2.0'}
        G.graph['labelloc'] = "t"
        G.graph['fontsize'] = 20
        
        A = to_agraph(G)
        A.layout('dot')
        A.draw(ofname)
        