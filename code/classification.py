
import sys
import joblib
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import make_scorer
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_validate

from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text


def console_ask(title: str, is_ask: bool = False):
    if is_ask:
        ret = Prompt.ask(f"[bold blue]{title} [/bold blue]")
        return ret
    else:
        console = Console()
        label = Text(title, style="bold green")
        console.print(label)

#funzione di conversione  dei dati per la classificazione da categorici a numerici
def prepDataset(df):

    #genre
    def creazioneArrayGenre(row, array):
        if row['genre'] is not None: 
                array.append(row['genre']);
            
    genre =[]
    df.apply(lambda row: creazioneArrayGenre(row,genre),axis=1) 
    nGenre = len(genre)
    genreDict = {}
    j = 0
    for k in range(nGenre):
        genreDict[genre[k]] = k;
        j = k
    genreDict['unknown'] = j+1
        
    def subGenre(row,dizionario):
        if row['genre'] is not None:
            element = row['genre']
            if element in dizionario:
                    row['genre'] = genreDict[element]
        return row['genre']

    df['genre']=df.apply(lambda row: subGenre(row,genreDict),axis=1)

    #type
    def creazioneArrayType(row, array):
        if row['type'] is not None: 
                array.append(row['type']);
            
    ty =[]
    df.apply(lambda row: creazioneArrayType(row,ty),axis=1) 
    nType = len(ty)
    typeDict = {}
    j = 0
    for n in range(nType):
        typeDict[ty[n]] = n;
        j = n
    typeDict['unknown'] = j+1
        
    def subType(row,dizionario):
        if row['type'] is not None:
            element = row['type']
            if element in dizionario:
                    row['type'] = typeDict[element]
        return row['type']

    df['type']=df.apply(lambda row: subType(row,typeDict),axis=1)


    #title
    def creazioneArrayTitle(row, array):
        if row['title'] is not None: 
                array.append(row['title']);
            
    title =[]
    df.apply(lambda row: creazioneArrayTitle(row,title),axis=1) 
    nTitle = len(title)
    titleDict = {}
    j = 0
    for i in range(nTitle):
        titleDict[title[i]] = i;
        j = i
    titleDict['unknown'] = j+1
        
    def subTitle(row,dizionario):
        if row['title'] is not None:
            element = row['title']
            if element in dizionario:
                    row['title'] = titleDict[element]
        return row['title']

    df['title']=df.apply(lambda row: subTitle(row,titleDict),axis=1)

    #year range
    def creazioneArrayYear(row, array):
        if row['year_range'] is not None: 
                array.append(row['year_range']);
            
    years =[]
    df.apply(lambda row: creazioneArrayYear(row,years),axis=1) 
    nYears = len(years)
    yearsDict = {}
    j = 0
    for k in range(nYears):
        yearsDict[years[k]] = k;
        j = k
    yearsDict['unknown'] = j+1
        
    def subYear(row,dizionario):
        if row['year_range'] is not None:
            element = row['year_range']
            if element in dizionario:
                    row['year_range'] = yearsDict[element]
        return row['year_range']

    df['year_range']=df.apply(lambda row: subYear(row,yearsDict),axis=1)


    #country
    def creazioneArrayCountry(row, array):
        if row['country'] is not None: 
                array.append(row['country']);
            
    country =[]
    df.apply(lambda row: creazioneArrayCountry(row,country),axis=1) 
    nCountry = len(country)
    countryDict = {}
    j = 0
    for k in range(nCountry):
        countryDict[country[k]] = k;
        j = k
    countryDict['unknown'] = j+1
        
    def subCountry(row,dizionario):
        if row['country'] is not None:
            element = row['country']
            if element in dizionario:
                    row['country'] = countryDict[element]
        return row['country']

    df['country']=df.apply(lambda row: subCountry(row,countryDict),axis=1)

    #cast
    def creazioneArrayCast(row, array):
        if row['cast'] is not None: 
                array.append(row['cast']);
            
    cast =[]
    df.apply(lambda row: creazioneArrayCast(row,cast),axis=1) 
    nCast = len(cast)
    castDict = {}
    j = 0
    for p in range(nCast):
        castDict[cast[p]] = p;
        j = p
    castDict['unknown'] = j+1
        
    def subCast(row,dizionario):
        if row['cast'] is not None:
            element = row['cast']
            if element in dizionario.keys():
                row['cast'] = castDict[element]
        return row['cast']

    df['cast']=df.apply(lambda row: subCast(row,castDict),axis=1)

    #costruzione dataset definendo colonna target
    y = df['genre'] #colonna target 
    df.drop('genre', axis=1, inplace=True)
    x=df #training set

    #bilanciamento
    ros = RandomOverSampler(sampling_strategy = "not majority")
    X_res, y_res = ros.fit_resample(x,y)

    #split
    xtr,xts,ytr,yts = train_test_split(X_res,y_res,test_size=0.3,random_state=0)

    class prepElements:
        x_train = xtr
        y_train = ytr
        x_test = xts
        y_test = yts
        genreD=genreDict
        castD=castDict
        yearsD=yearsDict
        countryD=countryDict
        titleD=titleDict
        typeD=typeDict
        X_train_complete=X_res
        y_train_complete=y_res
    
    prep=prepElements()
    return(prep)

#funzione per la ricerca dei parametri dei classificatori
def searchClassificator(xtr,ytr,xts,yts):
    #grid searching key hyperparametres per KNeighborsClassifier
    knn = KNeighborsClassifier()

    #parametri che vogliamo testare
    n_neighbors = [1, 3, 7, 11]
    weights = ['uniform', 'distance']
    metric = ['euclidean', 'manhattan', 'hamming']

    # definizione grid search
    score = 'accuracy'
    grid = dict(n_neighbors=n_neighbors,weights=weights,metric=metric)
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=2)
    target_names = ['anime','cult','fantasy','action','documentary','nature','romantic','sport','thrillers','kids','dramas','horror','standup','commedies','musical']

    #testing grid
    console_ask("# Tuning degli iperparametri\n")
    #ricerca iperparametri più performanti tramite cross validation
    grid_search = GridSearchCV(estimator=knn, param_grid=grid, n_jobs=-1, cv=cv, scoring=score ,error_score=0)
    grid_result = grid_search.fit(xtr, ytr)

    console_ask("Miglior combinazione di parametri ritrovata:\n")
    console_ask(grid_search.best_params_)
    console_ask()
    console_ask("Classification report:\n")
    console_ask("Il modello è stato addestrato sul training set completo\n")
    console_ask(" Le metriche sono state calcolate sul test set.\n")
    y_true, y_pred = yts, grid_search.predict(xts)
    
    console_ask(classification_report(y_true, y_pred,target_names=target_names))
    console_ask()


    #grid searching key hyperparametres per RandomForestClassifier
    randomForest = RandomForestClassifier()

    #parametri che vogliamo testare
    n_estimators = [10, 50, 100]
    max_features = ['sqrt', 'log2']

    # definizione grid search
    score = 'accuracy'
    target_names = ['anime','cult','fantasy','action','documentary','nature','romantic','sport','thrillers','kids','dramas','horror','standup','commedies','musical']
    grid = dict(n_estimators=n_estimators,max_features=max_features)
    cv = 10


    #testing grid
    console_ask("# Tuning degli iperparametri\n")
    #ricerca iperparametri più performanti tramite cross validation
    grid_search = GridSearchCV(estimator=randomForest, param_grid=grid, n_jobs=-1, cv=cv, scoring=score ,error_score=0)
    grid_result = grid_search.fit(xtr, ytr)

    console_ask("Miglior combinazione di parametri ritrovata:\n")
    console_ask(grid_search.best_params_)
    console_ask()
    console_ask("Classification report:\n")
    console_ask("Il modello è stato addestrato sul training set completo\n")
    console_ask(" Le metriche sono state calcolate sul test set.\n")
    y_true, y_pred = yts, grid_search.predict(xts)
    
    console_ask(classification_report(y_true, y_pred,target_names=target_names))
    console_ask()


    #grid searching key hyperparameters per BaggingClassifier
    bagging = BaggingClassifier()

    #parametri da testare
    n_estimators = [10, 50, 100]

    # definizione grid search
    score = "accuracy"
    target_names = ['anime','cult','fantasy','action','documentary','nature','romantic','sport','thrillers','kids','dramas','horror','standup','commedies','musical']
    grid = dict(n_estimators=n_estimators)
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=2)

    #testing grid
    console_ask("# Tuning degli iperparametri\n")
    #print()
    grid_search = GridSearchCV(estimator=bagging, param_grid=grid, n_jobs=-1, cv=cv, scoring=score, error_score=0)
    grid_result = grid_search.fit(xtr, ytr)

    console_ask("Miglior combinazione di parametri ritrovata:\n")
    console_ask(grid_search.best_params_)
    console_ask()
    console_ask("Classification report:\n")
    console_ask("Il modello è stato addestrato sul training set completo.\n")
    console_ask("Le metriche sono state calcolate sul test set.\n")
    y_true, y_pred = yts, grid_search.predict(xts)
    
    console_ask(classification_report(y_true, y_pred,target_names=target_names))
    console_ask()



#training finale
def finalClassification(X,y):
    clf=RandomForestClassifier(n_estimators=100,max_features='sqrt',class_weight='balanced')
    clf.fit(X,y) 
    #salvataggio modello
    filename =r'C:\Users\Asus\Desktop\Progetto icon\icon25\code\finalized_rf.sav'
    joblib.dump(clf, filename)



#Funzione per la predizione
def predictionGenre(filename,userInput,prepElement):
    
    user=userInput.copy()
    #conversione rating a numerico
    user["ratings"]=user.ratings.astype(float)

    user.drop('genre', axis=1, inplace=True)
    
    if user.at[0,'title'] in prepElement.titleD.keys():
        user.at[0,'title'] = prepElement.titleD[user.at[0,'title']]
    else:
        user.at[0,'title'] = prepElement.titleD['unknown']
    
    
    if user.at[0,'type'] in prepElement.typeD.keys():
        user.at[0,'type'] = prepElement.typeD[user.at[0,'type']]
    else:
        user.at[0,'type'] = prepElement.typeD['unknown']

    
    if user.at[0,'country'] in prepElement.countryD.keys():
        user.at[0,'country'] = prepElement.countryD[user.at[0,'country']]
    else:
        user.at[0,'country'] = prepElement.countryD['unknown']

    if user.at[0,'year_range'] in prepElement.yearsD.keys():
        user.at[0,'year_range'] = prepElement.yearsD[user.at[0,'year_range']]
    else:
        user.at[0,'year_range'] = prepElement.yearsD['unknown']

    if user.at[0,'cast'] in prepElement.castD.keys():
        user.at[0,'cast'] = prepElement.castD[user.at[0,'cast']]
    else:
        user.at[0,'cast'] = prepElement.castD['unknown']
    
    user['title']=user.title.astype(int)
    user['type']=user.type.astype(int)
    user['cast']=user.cast.astype(int)
    user['country']=user.country.astype(int)
    user['year_range']=user.year_range.astype(int)
    
    #caricamento modello
    model = joblib.load(filename)
    gen= model.predict(user)
    
    for genre, val in prepElement.genreD.items(): 
      if val == gen:
          gen=genre
    
    userInput.at[0,'genre'] = gen
    return gen 
    


def main(userMovie):
    
    df = pd.read_csv(r'C:\Users\Asus\Desktop\Progetto icon\icon25\datasets\Netflix_preprocessato.csv', sep=',')
        
    prepInfo=prepDataset(df)

    #ricerca parametri classificatori 
    #searchClassificator(prepInfo.x_train,prepInfo.y_train,prepInfo.x_test,prepInfo.y_test)
    
    #Fitting con il classificatore corretto
    finalClassification(prepInfo.X_train_complete,prepInfo.y_train_complete)
    
    #predizione del genere del file dato dall'utente
    result= predictionGenre(r"C:\Users\Asus\Desktop\Progetto icon\icon25\code\finalized_rf.sav",userMovie,prepInfo)
    console_ask('Il genere del film o serie TV da te inserito è %s \n' % result)


if __name__ == "__main__":
    main(sys.argv[1])
