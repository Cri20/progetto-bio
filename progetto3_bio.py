import re

filepath = './MAFFT.fa'

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# il main richiama le varie funzioni in modo da eseguire le richieste del progetto e generare il report a linea di comando

def main():

    lista_seq = read_file(filepath)

    ref = lista_seq[0]
    #rimuoviamo ref dalla lista
    lista_seq.pop(0)

    lista_variazioni=search_variation(lista_seq, ref) 
    stampo_tutte_var(lista_variazioni)

    rep_of_variation(lista_variazioni)
    print('-----------------------------------------------------------------------------------------------------------------')
   
    stamp_max_min(lista_variazioni)
    print('-----------------------------------------------------------------------------------------------------------------')
   
    all_common_position(lista_variazioni)
    print('-----------------------------------------------------------------------------------------------------------------')
   
    all_common_variation(lista_variazioni)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# il read_file legge il file di input MAFFT.fa e restituisce le varie sequenze genomiche

def read_file(filepath):
    List_genomi = []
    temp = ""

    with open(filepath, 'r') as file:   
        for row in file:
            if row.startswith('>'):
                if temp != "":  # Se abbiamo già raccolto una sequenza, la aggiungiamo alla lista
                    List_genomi.append(temp)
                    temp = ""  
            else:
                temp += row.strip()  # Aggiungiamo la linea corrente (senza '\n') alla sequenza

        # Aggiungiamo l'ultimo genoma alla lista, se esiste
        if temp:
            List_genomi.append(temp)
       
    return List_genomi

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# search_variatio restituisce una lista composta da liste ognuna delle quali elenca le varie variazioni del genoma rispetto al reference

def search_variation(List_genomi, ref):

    start = 0
    end = len(ref)
    lista_variazioni=[]

    for genoma in List_genomi:
        for i, base in enumerate(genoma): 
                if base == '-': 
                    continue        
                else:
                    start = i
                    break
                
        for i in reversed(range(len(genoma))):
                if genoma[i] == '-': 
                    continue        
                else:
                    end = i+1
                    break       
        
        variazioni_genoma = []

        for i, base in enumerate(genoma[start: end]): 
            if base != ref[i+start]:
                if base == '-': 
                    variazioni_genoma.append(('Posizione '+ str(i+start+1) +' : inserimento di '+ref[i+start]))
                if base == {'A','C','G','T','N'} and ref[i+start] == '-':  
                    variazioni_genoma.append(('Posizione '+ str(i+start+1) +' : cancellazione di '+ base))
                if base == {'A','C','G','T'} and ref[i+start] =='N' :
                    continue
                elif base in {'A','C','G','T'} and ref[i+start] != base:  
                    variazioni_genoma.append( ('Posizione '+str(i+start+1) +' : sostituzione '+ ref[i+start]+' -> '+base))

        lista_variazioni.append(variazioni_genoma)

    return lista_variazioni 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#stampo_tutte_var stampa l'identificatorele di ogni genoma seguito dalla lista delle variazioni rispetto al refrence

def stampo_tutte_var(lista_variazioni):
    
    lista_nomi=cerco_gen(filepath)
    for i, nome in enumerate(lista_nomi):
        print('Variazione di: '+ nome)
        for i in lista_variazioni[i]:
                print(i)
        print('-----------------------------------------------------------------------------------------------------------------')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# il cerco_gen legge il file di input MAFFT.fa e restituisce i vari identificatori delle sequenze genomiche

def cerco_gen(filepath):
    
    with open(filepath, 'r') as file:
        text = file.read()
        patter = r'>([^ ]+)'
        corrispondenze = re.findall(patter , text)
        #rimuoviamo ref dalla lista      
        corrispondenze.pop(0)
        
    return corrispondenze

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# rep_of_variation cerca quante volte una variazione occorre nei vari genomi allo stesso modo
# restituisce una lista di tuple ordinate per posizione della variazione seguita dal numero di volte che occorre

def rep_of_variation(lista_variazioni):
    
    list_frequency_of_variation = []

    for list_var_genoma in lista_variazioni:
        for var in list_var_genoma:
            # found = elemento booleano per controllare la presenza dell'elemento var (stringa della variazione) nella lista di tuple
            found = any(tup[0] == var for tup in list_frequency_of_variation) 
            if  found: 
                # cerca la posizione in cui è presente la var nella lista di tuple e fa +1 alla sua frequenza
                for index, (string, number) in enumerate(list_frequency_of_variation): 
                    if string == var:   
                        list_frequency_of_variation[index]=(string,(number+1))          
            else:
                #se var non è presente lo si aggiunge alla lista con frequenza 1
                list_frequency_of_variation.append((var, 1))  
    
    # ordina la lista per il primo elemento della tupla (stringa variazione) effettuando uno split e considerando la seconda parte della stringa (la posizione)
    list_frequency_of_variation = sorted(list_frequency_of_variation, key=lambda x: int(x[0].split()[1]))

    for  (string, number) in list_frequency_of_variation:
        print(string +' , la variazione rispetto al reference si ripete in '+ str(number) +' genomi')

            
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# stamp_max_min stampa l'identificatore dei genomi con il massimo e minimo numero di variazioni rispetto al reference

def stamp_max_min(lista_variazioni):

    # restituisce la lunghezza massima e minima tra tutte le liste di variazioni
    maxlength = max(len(elemento) for elemento in lista_variazioni)
    minlength = min(len(elemento) for elemento in lista_variazioni)
 
    # cerca la posizione dei genomi con le lunghezze trovate sopra
    for elemento in lista_variazioni:
        if maxlength == len(elemento):
            maxlista = lista_variazioni.index(elemento)
        if minlength == len(elemento):
            minlista = lista_variazioni.index(elemento)

    lista_gen = cerco_gen(filepath)

    print('Il genoma' , lista_gen[maxlista] ,'è quello con il numero massimo di variazioni: ', max(len(elemento) for elemento in lista_variazioni)) 
    print('Il genoma' , lista_gen[minlista] ,'è quello con il numero minimo di variazioni: ', min(len(elemento) for elemento in lista_variazioni)) 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# all_common_position stampa l'elenco delle posizioni del reference rispetto a cui tutti i genomi variano

def all_common_position(lista_variazioni):

    list_all_common_position = []   
    
    print('Elenco delle posizioni del reference rispetto a cui tutti i genomi variano: ')
    print()
    
    for pos in lista_variazioni:
        if list_all_common_position == []:
            # aggiungiamo la lista delle variazioni del primo genoma alla lista
            list_all_common_position = pos
        else:
            # creiamo due liste troncando il loro contenuto al carattere ':' tramite una RE per poter confrontare solo le posizioni
            set1 = {re.match(r'[^:]+',stringa).group() for stringa in list_all_common_position} 
            set2 = {re.match(r'[^:]+',stringa).group() for stringa in pos}
            
            # effettuiamo l'intersezione tra gli elementi comuni delle due liste
            list_all_common_position = set1.intersection(set2) 
    
    # ordina la lista effettuando uno split e considerando la seconda parte della stringa (la posizione)
    list_all_common_position = sorted(list_all_common_position, key=lambda x: int(x.split()[1]))

    for pos in list_all_common_position:
        print(pos)

    print()
    print('Numero di posizioni del reference rispetto a cui tutti i genomi variano: '+ str(len(list_all_common_position)))
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# all_common_variation stampa l'elenco delle posizioni del reference rispetto a cui tutti i genomi variano allo stesso modo

def all_common_variation(lista_variazioni):

    list_all_common_variation = []
    
    print('Elenco delle posizioni del reference rispetto a cui tutti i genomi variano allo stesso modo: ')
    print()

    for var in lista_variazioni:
        if list_all_common_variation == []:
            # aggiungiamo la lista delle variazioni del primo genoma alla lista
            list_all_common_variation = var
        else:
            # creiamo due liste da poter controntare nella loro interezza
            set1 = set(list_all_common_variation)
            set2 = set(var)
            
            # effettuiamo l'intersezione tra gli elementi comuni delle due liste
            list_all_common_variation = set1.intersection(set2)
    
    # ordina la lista effettuando uno split e considerando la seconda parte della stringa (la posizione)
    list_all_common_variation = sorted(list_all_common_variation, key=lambda x: int(x.split()[1]))

    for var in list_all_common_variation:
        print(var)

    print()
    print('Numero di posizioni del reference rispetto a cui tutti i genomi variano allo stesso modo: '+ str(len(list_all_common_variation)))
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
                
main()

            
        





