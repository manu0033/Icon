import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from kmodes.kmodes import KModes
from fuzzywuzzy import fuzz
import KB
import sys 
import os

from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

'''calcolo delle similarità tra i valori del film inserito dall utente e quelli presenti nel
cluster, restituendo il valore totale di similarità dell'intero cluster'''


def console_ask(title: str, is_ask: bool = False):
    if is_ask:
        ret = Prompt.ask(f"[bold blue]{title} [/bold blue]")
        return ret
    else:
        console = Console()
        label = Text(title, style="bold green")
        console.print(label)


def similarities(cluster, userMovie):
    totalSum = 0
    cluster['sum'] = 0
    for i in range(0, len(cluster)):
        rowSum = fuzz.ratio(cluster['genre'].values[i], userMovie['genre'].values[0])
        rowSum += fuzz.ratio(cluster['title'].values[i], userMovie['title'].values[0])
        rowSum += fuzz.ratio(cluster['cast'].values[i], userMovie['cast'].values[0])
        rowSum += fuzz.ratio(cluster['year_range'].values[i], userMovie['year_range'].values[0])
        rowSum += fuzz.ratio(cluster['country'].values[i], userMovie['country'].values[0])
        cluster['sum'].values[i] = rowSum
        totalSum += rowSum
    return totalSum

'''Operazioni sul dataset per renderlo utilizzabile ai fine della clusterizzazione.
    Nello specifico, viene discretizzata la colonna relativa al rating.'''
def dataOperations(df):
    #discretizzazione colonna ratings
    bins = [0,5,np.inf]
    names = ['<5','>5']
    df['ratings_range'] = pd.cut(df['ratings'],bins, labels=names)
    df = df.drop(['ratings'],axis =1)
    df= df.dropna(subset=['ratings_range'])
    return df

'''' Utilizzo del metodo del gomito per determinare il valore di k corretto.'''
def KChoice(df):
    cost = []
    K = range(1,10)
    for num_clusters in list(K):
        kmode = KModes(n_clusters=num_clusters, init = "random", n_init = 5, verbose=1)
        kmode.fit_predict(df)
        cost.append(kmode.cost_)
    plt.plot(K, cost, 'bx-')
    plt.xlabel('No. of clusters')
    plt.ylabel('Cost')
    plt.title('Elbow Method For Optimal k')
    plt.show()

'''Definizione di dataframe Pandas separati per ciascun cluster, rimuovendo 
    la colonna indicatrice del numero di cluster corrispondente per ciascuna row.'''
def clusterOperations(df,n):
    cluster = df[df.cluster == n]
    cluster = cluster.drop(columns = ['cluster'])
    return cluster

'''Stampa dei film da suggerire all utente.'''
def toUser(topTen):
    print("\n\n")
    table = Table(title="Potresti apprezzare:")
    table.add_column("Da Guardare", style="cyan", justify="left")
    for element in topTen:
        table.add_row(element)
    console = Console()
    console.print(table)

'''Definizione dei film da suggerire all utente, mediante calcoli relativi
    le similarità con i cluster.'''
def recommendation(cluster1,cluster2,cluster3,userMovie):
    totSum1 = similarities(cluster1, userMovie)
    totSum2 = similarities(cluster2, userMovie)
    totSum3 = similarities(cluster3, userMovie)
    simil = [totSum1,totSum2,totSum3]
    choice = simil.index(max(simil))
    if choice==0:
        cluster1.sort_values(by=['sum'], ascending=False, inplace = True)
        topTen = cluster1['title'].head(10)
    elif choice==1:
        cluster2.sort_values(by=['sum'], ascending=False, inplace = True)
        topTen = cluster2['title'].head(10)
    elif choice==2:
        cluster3.sort_values(by=['sum'], ascending=False, inplace = True)
        topTen = cluster3['title'].head(10)
    toUser(topTen)

    rispostaUtente=console_ask('Se vuoi approfondire le raccomandazioni mostrate, scrivi kb: ', True)
    if(rispostaUtente=='kb'):
        KB.explainResultsCluster(cluster1, cluster2, cluster3, simil, choice)
    else:
        print('Niente spiegazioni\n')


'''Classe utile per bloccare le stampe automatiche del modello.'''
class HandlePrint():
    def __init__(self):
        self.initial_stout = sys.stdout

    def blockPrint(self):
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def resetPrint(self):
        sys.stdout = self.initial_stout


def main(userMovie):
    df = pd.read_csv(r'C:\Users\Asus\Desktop\Progetto icon\icon25\datasets\Netflix_preprocessato.csv', sep=',')
    df = dataOperations(df)
    #KChoice(df) # Utilizzo del metodo del gomito per determinare il valore di k corretto
    
    # Building the model with 3 clusters
    handle = HandlePrint()
    handle.blockPrint()
    kmode = KModes(n_clusters=3, init = "random", n_init = 5, verbose=1)
    df['cluster'] = kmode.fit_predict(df)
    handle.resetPrint()
    cluster1 = clusterOperations(df,0)
    cluster2 = clusterOperations(df,1)
    cluster3 = clusterOperations(df,2)
    recommendation(cluster1, cluster2, cluster3, userMovie)
    
if __name__ == "__main__":
    main(sys.argv[1])