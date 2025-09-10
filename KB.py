import pandas as pd
import numpy as np

from rich.prompt import Prompt
from rich.console import Console
from rich.text import Text
# Inizio KB
# Lettura csv
movieDataString = pd.read_csv(r'C:\Users\Asus\Desktop\Progetto icon\icon25\datasets\Netflix_preprocessato.csv', sep=',')

#Creazione delle liste per ogni singola colonna
type = movieDataString.loc[:,'type']
title = movieDataString.loc[:, 'title']
genre = movieDataString.loc[:, 'genre']
country = movieDataString.loc[:, 'country']
ratings = movieDataString.loc[:, 'ratings']
year_range= movieDataString.loc[:, 'year_range']


def console_ask(title: str, is_ask: bool = False):
    if is_ask:
        ret = Prompt.ask(f"[bold blue]{title} [/bold blue]")
        return ret
    else:
        console = Console()
        label = Text(title, style="bold green")
        console.print(label)

# dato un genere, restituisce una lista con tutti i film che trova di quel genere
def trovaGenere(genere:str):    
    j = 0
    listaRisultati = {}
    for i in range(len(genre)):
        if(genre[i] == genere):
            listaRisultati[j] = [title[i]]
            j += 1         
    return listaRisultati


# determina se un film esiste
def titoloEsiste(titolo:str):
    for i in range(len(title)):
        if(title[i] == titolo or title[i].lower() == titolo.lower()):
            return True
    return False

# determina in che posizione si trova il film
def whereTitoloEsiste(titolo:str):
    for i in range(len(title)):
        if(title[i] == titolo or title[i].lower() == titolo.lower()):
            return i
    return i # altrimenti ritonra un mess di errore

# determina se un determinato genere esiste nel dataset
def genereEsiste(genere:str):
    for i in range(len(genre)):
        if(genre[i] == genere):
            return True
    return False

# dato un indice, restituisce il genere corrispondente a quell'indice
def estrapolaGenere(i: int):
    return genre[i]

# determina se i due generi in input sono uguali
def generiUguali(primoGenere:str, secondoGenere:str):
    if(primoGenere==secondoGenere):
        return True
    return False

# trova la corrispondenza nel dataset tra un titolo e un genere
def corrispondenzaEsiste(titolo:str, genere:str):
    i = whereTitoloEsiste(titolo)

    if(genre[i]==genere):
        return True
    return False

# dato un titolo e un genere in input, risponde se ha trovato una corrispondenza nel dataset
def askGenereDaTitolo(titolo:str,genere:str):
    # Controllo se titolo scritto bene
    if(not titoloEsiste(titolo)):
        console_ask("Il titolo non esiste") 
        return

    #controllo se genere scritto bene
    if(not genereEsiste(genere)):
        console_ask("Il genere non è presente") 
        return
    
    stringa = titolo + "_" + genere
    
    # Trova la corrispondenza tra titolo e genere
    risposta = corrispondenzaEsiste(titolo,genere) 
    if(risposta):
        console_ask("SI")
    else:
        console_ask("NO")
    
    # spiega come si è arrivati alla soluzione
    rispostaUtente=console_ask("Digitare how per la spiegazione: ", True)
    if (rispostaUtente.lower()=="how"):
       console_ask("askGenereDaTitolo("+titolo+","+genere+") <=> "+stringa)
       rispostaUtente=console_ask("Scrivi how i, sostituendo a i il numero dell’atomo : ", True)
       if(rispostaUtente.lower()=='how 1'):
           console_ask(f"{stringa} <=> {risposta}")
       else:
           console_ask("Errore di digitazione esiste solo un atomo ")
    else:
         console_ask("Errore di digitazione")
    
# dati due titoli, risponde se presentano lo stesso genere 
def askStessoGenere(titolo1:str, titolo2:str):
    
    if(not titoloEsiste(titolo1)):
        console_ask("Il primo titolo inserito non è presente")
        return
    if(not titoloEsiste(titolo2)):
        console_ask("Il secondo titolo inserito non è presente")
        return
    
    # Identifico la posizione dei titoli visto che sono presenti nel dataset
    primoTitolo = whereTitoloEsiste(titolo1)
    secondoTitolo = whereTitoloEsiste(titolo2)

    # Estrapolo i generi dei titoli
    primoGenere = estrapolaGenere(primoTitolo)
    secondoGenere = estrapolaGenere(secondoTitolo)
               
    risposte = {}
    
    risposte[1] = corrispondenzaEsiste(titolo1,primoGenere)
    risposte[2] = corrispondenzaEsiste(titolo2, secondoGenere)
    risposte[3] = generiUguali(primoGenere, secondoGenere)

    if(risposte.get(1) == True and risposte.get(2) == True and risposte.get(3) == True):
        console_ask("SI")
    else:
        console_ask("NO")
    
    # Spiega come si è arrivati ai risultati
    rispostaUtente=console_ask("Digitare how per la spiegazione: ", True)
    if (rispostaUtente.lower()=="how"):
       console_ask("askStessoGenere("+titolo1+","+titolo2+") <=> "+titolo1+"_"+primoGenere+ " and "+titolo2+"_"+secondoGenere+" and generiUguali("+primoGenere+","+secondoGenere+")")

       rispostaUtente=console_ask("Digita how i, sostituendo a i il numero dell’atomo, per avere ulteriori informazioni:", True)
       if(rispostaUtente.lower()=='how 1'):
           console_ask(titolo1+"_"+primoGenere+" <=>", risposte.get(1))
           rispostaUtente=console_ask("Digita how i, sostituendo a i il numero dell’atomo, per avere ulteriori informazioni: ", True)
           if(rispostaUtente.lower() =="how 2"):
               console_ask(titolo2+"_"+secondoGenere+" <=>",risposte.get(2))       
               rispostaUtente=console_ask("Digita how i, sostituendo a i il numero dell’atomo, per avere ulteriori informazioni: ", True)
               if(rispostaUtente=="how 3"): 
                   console_ask("generiUguali("+primoGenere+","+secondoGenere+") <=>", risposte[3])       
               else:
                   console_ask("Errore di digitazione")
           else: 
               console_ask("Errore di digitazione")
       else:
           if(rispostaUtente.lower() =="how 2"):
               console_ask("SecondaCorrispondenza("+titolo2+") <=> corrispondenzaEsiste("+titolo2+" , " + secondoGenere+ ") <=>", risposte.get(2))       
               rispostaUtente=console_ask("Digitare 'how i' specificando in i il numero dell'atomo per ulteriori informazioni: ", True)
               
               if(rispostaUtente.lower()=="how 1"):
                   console_ask("PrimaCorrispondenza("+titolo1+") <=> corrispondenzaEsiste("+titolo1+" , " + primoGenere+ ") <=>", risposte.get(1))
               else:
                   if(rispostaUtente=="how 3"): 
                       console_ask("stessoGenere("+titolo1+","+titolo2+") <=> "+primoGenere+"_"+secondoGenere+" <=>", risposte[3])       
                   else:
                       console_ask("Errore di digitazione")
                
           else:
               if(rispostaUtente.lower() =="how 3"):
                   console_ask("stessoGenere("+titolo1+","+titolo2+") <=>  generiUguali("+primoGenere+","+secondoGenere+") <=>", risposte[3])
                   rispostaUtente=console_ask("Digita how i, sostituendo a i il numero dell’atomo, per avere ulteriori informazioni : ", True)
                   if(rispostaUtente.lower() =="how 2"):
                       console_ask("SecondaCorrispondenza("+titolo2+") <=> corrispondenzaEsiste("+titolo2+" , " + secondoGenere+ ") <=>", risposte.get(2))       
                       rispostaUtente=console_ask("Digita how i, sostituendo a i il numero dell’atomo, per avere ulteriori informazioni : ", True)
                        
                       if(rispostaUtente.lower()=="how 1"):
                           console_ask("PrimaCorrispondenza("+titolo1+" ) <=> corrispondenzaEsiste("+titolo1+" , " + primoGenere+ ") is ", risposte.get(1))
                       else:
                           if(rispostaUtente=="how 2"): 
                               console_ask("SecondaCorrispondenza("+titolo2+") <=> corrispondenzaEsiste("+titolo2+" , " + secondoGenere+ ") is ", risposte.get(2))       
                           else:
                               console_ask("Errore di digitazione")
               else:
                   console_ask("Errore di digitazione")
    else:
        console_ask("Errore di digitazione") 
        

# spiega i risultati ottenuti dalle raccomandazioni effettuate col clustering

def explainResultsCluster(cluster1, cluster2, cluster3, similarities, choice):
    choice+=1
    console_ask(f'Il cluster di appartenenza è il valore di choice: {choice}')
    console_ask(f'Le metriche restituite tra tutti i cluster sono le seguenti: {similarities}')
    if(choice == 1):
        copia = cluster1.drop(columns=['ratings_range','type','genre','cast','year_range','country'])
        copia = copia.rename(columns={"sum": "similarity"})
        console_ask(f'\nLe singole metriche di similarità restituite per il cluster {choice} sono:\n {copia.head(10)} \n')
    if(choice == 2):
        copia = cluster2.drop(columns=['ratings_range','genre','cast','year_range','country'])
        copia = copia.rename(columns={"sum": "similarity"})
        console_ask(f'\nLe singole metriche di similarità restituite per il cluster {choice} sono:\n {copia.head(10)} \n')
    if(choice == 3):
        copia = cluster3.drop(columns=['ratings_range','genre','cast','year_range','country'])
        copia = copia.rename(columns={"sum": "similarity"})
        console_ask(f'\nLe singole metriche di similarità restituite per il cluster {choice} sono:\n {copia.head(10)} \n')

def mainFunz():
    # askGenereDaTitolo
    console_ask('1) Inserendo un titolo e un genere, la KB può verificare se il titolo appartiene al genere indicato tramite la funzione askGenereDaTitolo, restituendo SI se corrisponde e NO in caso contrario. \n')
    
    # askStessoGenere
    console_ask('2) Fornendo due titoli, la KB può verificare se appartengono allo stesso genere tramite la funzione askStessoGenere, restituendo SI se corrispondono, NO altrimenti.\n')
    
    rispostaUtente=console_ask("Digita il numero della funzione che si vuole eseguire : ", True)
    if (rispostaUtente=="1"):
        titoloUtente = console_ask("Digita il titolo del film: ", True)
        genereUtente = console_ask("Digita il genere del film: ", True)
        askGenereDaTitolo(titoloUtente, genereUtente)   
    else:
        if(rispostaUtente=="2"):
            titoloUtente1 = console_ask("Digita il titolo del primo film: ", True)
            titoloUtente2 = console_ask("Digita il titolo del secondo film: ", True)
            askStessoGenere(titoloUtente1,titoloUtente2) 
        else: 
            console_ask('Errore di digitazione')

if __name__ == "__main__":
    mainFunz()