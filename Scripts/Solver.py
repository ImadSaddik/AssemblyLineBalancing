import streamlit as st

from PIL import Image

import networkx as nx

from Visualizer import getGraph, plotGraph


def solve(tasksData, edgesData, metaData):
    method = metaData['method']
    balancedGraph = None
    
    if method == 'RPW':
        graph = getGraph(tasksData, edgesData)
        takeTime = metaData['taktTime']
        
        balancedGraph = calculateRPW(graph, takeTime)
        outputPath = '../Output/balanced.png'
        plotGraph(balancedGraph, outputPath)
        
        balancedGraphImage = Image.open(outputPath)
        st.markdown("<br>", unsafe_allow_html=True)
        st.image(balancedGraphImage, caption="Balanced line")
    
    elif method == 'SPT':
        pass
    
    elif method == '':
        pass
    
    else:
        pass
        
        
    return balancedGraph


def calculateRPW(G_digraph, limit):
    rpw_weights = {
        i: sum(
            G_digraph.nodes[j].get('weight')
            for j in list(nx.dfs_tree(G_digraph, source=i))
        )
        for i in G_digraph.nodes
    }
    sorted_rpw_weights = dict(
        sorted(rpw_weights.items(), key=lambda item: item[1], reverse=True)
    )
    sorted_rpw_weights_keys = list(sorted_rpw_weights.keys())    

    count=0
    totalweight=0
    group={}
    group_key=1
    tmpgrp = []
    nodeweight = [];

    for count in range(len(sorted_rpw_weights_keys)):
        totalweight += G_digraph.nodes[sorted_rpw_weights_keys[count]].get('weight')
        tmpgrp += [sorted_rpw_weights_keys[count]]
        
        if (count+1 > len(sorted_rpw_weights_keys)-1):
            group[group_key] = tmpgrp
            nodeweight.append(totalweight)
            break
        
        if (totalweight + G_digraph.nodes[sorted_rpw_weights_keys[count+1]].get('weight')) > limit:
            group[group_key] = tmpgrp
            tmpgrp = []
            group_key += 1
            nodeweight.append(totalweight)
            totalweight = 0

    G_balanced_line = nx.DiGraph()
    str1 = ", "
    G_balanced_line.add_nodes_from({ k: (str1.join(group[k])) for k in range(1, len(group)+1) })
    G_balanced_line.add_edges_from({ k: (k,k+1) for k in range(1,len(group)+1) if (k+1 < len(group)+1) }.values())
    nx.set_node_attributes(
        G_balanced_line,
        {k: {'label': f"{str(k)} {str(group[k])}"} for k in group},
    )

    nx.set_node_attributes(G_balanced_line, { k+1: {'weight':nodeweight[k]} for k in range(len(nodeweight)) })
    nx.set_node_attributes(G_balanced_line, {k: {'group':group[k]} for k in group})
    
    return G_balanced_line