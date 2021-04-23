import networkx as nx
import matplotlib.pyplot as plt
import random
import igraph as ig
import time
import pandas as pd
import numpy as np
import csv
import math
import cartopy as cp
from data_visualization import get_coordinates

years = ['2019', '2020']
months = ['01', '02'] #'03', '04', '05', '06', '07', '08', '09', '10', '11', '12'
vertices = {}
verticeslist = []
for i in range(len(years)):
    for j in range(len(months)):
        filename = f"EU_flights_{years[i]}_{months[j]}"
        print(f"EU_flights_{years[i]}_{months[j]}")
        path = f'C:\\Users\\phili\\PycharmProjects\\Test-Analysis-Simulation\\{years[i]}_Filtered\\{filename}.csv'

        """Creating a graph from data"""
        data = pd.read_csv(path, usecols=[1, 2])
        g0 = ig.Graph.DataFrame(edges=data, directed=True)


        list1 = []

        vertices["time"] = {}
        vertices["airports"] = {}

        vertices["time"] = months[j] + "_" + years[i]
        for v in g0.vs():
            list1.append(v["name"])
        vertices["airports"] = list1
