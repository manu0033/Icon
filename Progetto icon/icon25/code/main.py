import pandas as pd
import recommender as rec
import classification as clf
import KB

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

#funzione per l'inserimento dei dati del film dall'utente
def getUserMovie(choice):
    console = Console()
    title = Prompt.ask("[bold blue]Inserire il nome del film o serie TV che hai apprezzato: [/bold blue]").lower()
    typeM = Prompt.ask(f"[bold blue]{title} è un film? (s/n) [/bold blue]").lower()
    while (str(typeM) != 's' and str(typeM) != 'n'):
        typeM = Prompt.ask("[bold blue]Inserisci un'opzione valida [/bold blue]").lower()
    if typeM == 's':
        typeM = 'Movie'
    else:
        typeM = 'TV Show'
    country = Prompt.ask('[bold blue]Inserire il paese di produzione: [/bold blue] -> ').lower()
    yr = Prompt.ask('[bold blue]Inserire l`anno di rilascio: [/bold blue] -> ').lower()
    yr = releaseYear(yr)
    cast = Prompt.ask('[bold blue]Inserire un membro del cast: [/bold blue] -> ').lower()
    rating = Prompt.ask('[bold blue]Inserire un voto da 1 a 10 sul film/serie TV: [/bold blue] -> ').lower()
    print('\n\n')
    genreM=''
    if choice == 1:
        table = Table(title="Scegli un Genere:")
        table.add_column("Generi", style="cyan", justify="left")
        table.add_row("1. Action")
        table.add_row("2. Anime")
        table.add_row("3. Commedies")
        table.add_row("4. Cult")
        table.add_row("5. Documentary")
        table.add_row("6. Dramas")
        table.add_row("7. Fantasy")
        table.add_row("8. Horror")
        table.add_row("9. Kids")
        table.add_row("10. Musical")
        table.add_row("11. Nature")
        table.add_row("12. Romantic")
        table.add_row("13. Sport")
        table.add_row("14. Stand-up")
        table.add_row("15. Thrillers")
        console.print(table)
        genreM = Prompt.ask('[bold blue]Inserisci il genere: [/bold blue]').lower()
        if (genreM == '1'):
            genreM = 'action'
        elif (genreM == '2'):
            genreM = 'anime'
        elif (genreM == '3'):
            genreM = 'comedies'
        elif (genreM == '4'):
            genreM = 'cult'
        elif (genreM == '5'):
            genreM = 'documentary'
        elif (genreM == '6'):
            genreM = 'dramas'
        elif (genreM == '7'):
            genreM = 'fantasy'
        elif (genreM == '8'):
            genreM = 'horror'
        elif (genreM == '9'):
            genreM = 'kids'
        elif (genreM == '10'):
            genreM = 'musical'
        elif (genreM == '11'):
            genreM = 'nature'
        elif (genreM == '12'):
            genreM = 'romantic'
        elif (genreM == '13'):
            genreM = 'sport'
        elif (genreM == '14'):
            genreM = 'standup'
        elif (genreM == '15'):
            genreM = 'thrillers' 
        else:
            while (not 1 <= int(genreM) <= 15):
                genreM = Prompt.ask("[bold blue]Perfavore, inserisci un numero corretto.[/bold blue]") 
    data = {'type':[typeM],'title':[title],'cast':[cast],'genre': [genreM],'country':[country],'year_range':[yr],'ratings':[rating]}
    userMovieDF = pd.DataFrame(data)
    return userMovieDF


#funzione del menu principale
def menu():

    console = Console()
    panel = Panel("Benvenuto in FilmView", title="FilmView")
    console.print(panel)

    table = Table(title="Scegli cosa fare:")
    table.add_column("Operazioni Disponibili", style="cyan", justify="left")
    table.add_row("1. Ricevi un consiglio per un nuovo film partendo da uno che ti è piaciuto")
    table.add_row("2. Scopri il genere di un film o di una serie")
    table.add_row("3. Fai una domanda al sistema")
    table.add_row("4. Chiudi il programma")
    console.print(table)

    choice = Prompt.ask("[bold blue]Inserisci l'operazione: [/bold blue]")
    while (int(choice) != 1 and int(choice) != 2 and int(choice) != 3 and int(choice) != 4):
        choice = Prompt.ask("[bold blue]Inserisci un'opzione valida [/bold blue]")
    return int(choice)


#funzione calcolo range anno di rilascio
def releaseYear(year):
    yearI=int(year)
    
    if (yearI < 1950):
            year = '<1950'
    elif (yearI >= 1950 and yearI < 1960):
            year ='1950-1960'
    elif (yearI >= 1960 and yearI < 1970):
            year ='1960-1970'
    elif (yearI >= 1970 and yearI < 1980):
            year ='1970-1980'
    elif (yearI >= 1980 and yearI < 1990):
            year ='1980-1990'
    elif (yearI >= 1990 and yearI < 1995):
            year ='1990-1995'
    elif (yearI >= 1995 and yearI < 2000):
            year ='1995-2000'
    elif (yearI >= 2000 and yearI < 2005):
            year ='2000-2005'
    elif (yearI >= 2005 and yearI < 2010):
            year ='2005-2010'
    elif (yearI >= 2010 and yearI < 2015):
            year ='2010-2015'
    elif (yearI >= 2015 and yearI <= 2020):
            year ='2015-2020'
    return year

def main():
    #preprocessing dei dati
    #prep.main()
    choice = 0
    while choice!=4:
        #menu
        choice = menu()
        
        console = Console()
        label = Text("\n\nINIZIAMO!\n", style="bold green")
        console.print(label)

        if choice == 1:
            userMovie = getUserMovie(choice)
            #recommender system
            rec.main(userMovie)
        if choice == 2:
            userMovie = getUserMovie(choice)
            #predizione genere
            clf.main(userMovie)
        if choice == 3:
            #interrogazione della base di conoscenza sul film
            KB.mainFunz()
        if choice == 4:
            print('Uscita...\n')
            break
 
if __name__ == "__main__":
    main()