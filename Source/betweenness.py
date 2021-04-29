import igraph as ig
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

start_time = time.time()

def get_betweenness(filename):

    """Creating a graph from data"""
    data = pd.read_csv(filename, usecols = [1,2])
    g0 = ig.Graph.DataFrame(edges=data,directed=True)


    """Creating a weighted graph from the adjacency matrix"""

    adj_matrix = g0.get_adjacency()
    adj_matrix = list(adj_matrix)

    g = ig.Graph.Weighted_Adjacency(adj_matrix)
    g.vs["name"] = g0.vs["name"]

    """Betweenness analysis"""

    vertbet = g.vs.betweenness(weights=None)
    #use this line for normalized betweenness
    #vertbet = 1/((len(vertbet)-1) * (len(vertbet)-2)) * np.array(vertbet)

    highbet = []
    highbet_names = []
    zerobets = []

    for i in range(len(vertbet)):
        if vertbet[i] in sorted(vertbet,key=float,reverse=True)[0:10] and vertbet[i] not in highbet:
            highbet.append(vertbet[i])
            highbet_names.append(g.vs[i]["name"])

    for i in range(len(vertbet)):
        if vertbet[i] == 0:
            zerobets.append(vertbet[i])

    avg_bet = sum(vertbet)/len(vertbet)
    avg_highbet = sum(highbet)/len(highbet)
    max_bet = max(highbet)

    for i in range(len(highbet)):
        if highbet[i] == max_bet:
            max_bet_name = highbet_names[i]

    zero_bet = len(zerobets)
    zero_bet_per = zero_bet / len(vertbet) * 100

    return avg_bet, avg_highbet, max_bet, max_bet_name, zero_bet, zero_bet_per


avg_bets2019 = []
avg_highbets2019 = []
max_bets2019 = []
max_bet_names2019 = []
zero_bets2019 = []
zero_bets_per2019 = []

for i in range(12):
    name = "EU_flights_2019_" + str(i+1) + ".csv"
    f = get_betweenness(name)
    avg_bets2019.append(f[0])
    avg_highbets2019.append(f[1])
    max_bets2019.append(f[2])
    max_bet_names2019.append(f[3])
    zero_bets2019.append(f[4])
    zero_bets_per2019.append(f[5])

print(avg_bets2019)
print(avg_highbets2019)
print(max_bets2019)
print(max_bet_names2019)
print(zero_bets2019)
print(zero_bets_per2019)

avg_bets2020 = []
avg_highbets2020 = []
max_bets2020 = []
max_bet_names2020 = []
zero_bets2020 = []
zero_bets_per2020 = []

for i in range(12):
    name = "EU_flights_2020_" + str(i+1) + ".csv"
    f = get_betweenness(name)
    avg_bets2020.append(f[0])
    avg_highbets2020.append(f[1])
    max_bets2020.append(f[2])
    max_bet_names2020.append(f[3])
    zero_bets2020.append(f[4])
    zero_bets_per2020.append(f[5])


x = np.arange(len(avg_bets2019))

plt.figure()

plt.subplot(121)
plt.plot(x,avg_bets2019, label = "2019: Average", linewidth = 2)
plt.plot(x,avg_bets2020, label = "2020: Average", linewidth = 2)
plt.xticks(ticks = x, labels = ["January","February","March","April","May","June","July","August","September","October","November","December"], rotation = 45)
plt.xlim([0,len(x)-1])
plt.title("Average betweenness of all airports")
plt.legend()
plt.grid(axis = "x", linestyle = "--")
plt.xlabel("Date")
plt.ylabel("Betweenness")

plt.subplot(122)
plt.plot(x,avg_highbets2019, label = "2019: Average of highest 10", linewidth = 2)
plt.scatter(x,max_bets2019, label = "2019: Maximum")
for i, name in enumerate(max_bet_names2019):
    plt.annotate(max_bet_names2019[i],(x[i],max_bets2019[i]))

plt.plot(x,avg_highbets2020, label = "2020: Average of highest 10", linewidth = 2)
plt.scatter(x,max_bets2020, label = "2020: Maximum")
for i, name in enumerate(max_bet_names2020):
    plt.annotate(max_bet_names2020[i],(x[i],max_bets2020[i]))

plt.xticks(ticks = x, labels = ["January","February","March","April","May","June","July","August","September","October","November","December"], rotation = 45)
plt.xlim([0,len(x)-1])
plt.title("Average and maximum betweenness of chosen airports")
plt.legend()
plt.grid(axis = "x", linestyle = "--")
plt.xlabel("Date")
plt.ylabel("Betweenness")

plt.show()

plt.plot(x,zero_bets2019, label = "2019: Absolute", linewidth = 2, color = "pink")
plt.plot(x,zero_bets2020, label = "2020: Absolute", linewidth = 2, color = "darkred")
plt.xticks(ticks = x, labels = ["January","February","March","April","May","June","July","August","September","October","November","December"], rotation = 45)
plt.xlim([0,len(x)-1])
plt.ylim(0,100)
plt.yticks(np.linspace(0,100,6), color = "red")
plt.title("Zero betweenness airports")
plt.legend()
plt.grid(axis = "x", linestyle = "--")
plt.xlabel("Date")
plt.ylabel("Number", color = "red")
plt.twinx()
plt.plot(x,zero_bets_per2019, label = "2019: Percentage", linewidth = 2, color = "lightblue")
plt.plot(x,zero_bets_per2020, label = "2020: Percentage", linewidth = 2, color = "darkblue")
plt.ylim(0,50)
plt.yticks(np.linspace(0,50,6), color = "blue")
plt.ylabel("Percentage",color = "blue")
plt.legend(loc = "center right")
plt.show()

print(time.time() - start_time)