import argparse
import re

filepath = './MAFFT.fa'


#-----------------------------------------------------------------------------------------------------------------------------------------------------------

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
                   
                    variazioni_genoma.append(('Posizione '+str(i+start+1)+' : inserimento di '+ref[i+start]))
                if base == {'A','C','G','T','N'} and ref[i+start] == '-': 
                   
                    variazioni_genoma.append(('Posizione '+str(i+start+1)+' : cancellazione di '+base))
                if base == {'A','C','G','T'} and ref[i+start] =='N' :
                    continue
                elif base in {'A','C','G','T'} and ref[i+start] != base:
                   
                    variazioni_genoma.append( ('Posizione '+str(i+start+1)+' : sostituzione '+ref[i+start]+' -> '+base))

        lista_variazioni.append(variazioni_genoma)
    return lista_variazioni 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def stampo_tutte_var(lista):
    
    lista_nomi=cerco_gen(filepath)
    for i, nome in enumerate(lista_nomi):
        print('Variazione di: '+ nome)
        for i in lista[i]:
                print(i)
        print('-----------------------------------------------------------------------------------------------------------------')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def cerco_gen(filepath):
    
    with open(filepath, 'r') as file:
        text = file.read()
        patter = r'>([^ ]+)'
        corrispondenze = re.findall(patter , text)
        #rimuoviamo ref dalla lista      
        corrispondenze.pop(0)
        
    return corrispondenze

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def rep_of_variation(lista_variazioni):
    
    list_frequency_of_variation = []

    for list_var_genoma in lista_variazioni:
        for var in list_var_genoma:
            found = any(tup[0] == var for tup in list_frequency_of_variation)
            if  found:
                for index, (string, number) in enumerate(list_frequency_of_variation):
                    if string == var:
                        list_frequency_of_variation[index]=(string,(number+1))          
            else:
                list_frequency_of_variation.append((var, 1))
    
    
    list_frequency_of_variation = sorted(list_frequency_of_variation, key=lambda x: int(x[0].split()[1]))

    for  (string, number) in list_frequency_of_variation:
        print(string +' , la variazione ripetto al reference si ripete in '+ str(number) +' genomi')

            
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
        
def stamp_max_min(lista):
    maxlength=max(len(elemento) for elemento in lista)
    minlength=min(len(elemento) for elemento in lista)
 
    for elemento in lista:
        if maxlength == len(elemento):
            maxlista = lista.index(elemento)
        if minlength == len(elemento):
            minlista = lista.index(elemento)

    lista_gen = cerco_gen(filepath)
    #print(len(lista_gen))

    #for elemento in lista:
        #print(len(elemento))

    print('Il genoma' ,lista_gen[maxlista] ,'è quello con il numero massimo di variazioni: ', max(len(elemento) for elemento in lista)) 
    print('Il genoma' ,lista_gen[minlista] ,'è quello con il numero minimo di variazioni: ', min(len(elemento) for elemento in lista)) 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
               
def all_common_position(lista_variazioni):
    list_all_common_position = []
    
    
    print('Elenco delle posizioni del reference rispetto a cui tutti i genomi variano: ')
    print()
    
    for pos in lista_variazioni:
        if list_all_common_position == []:
            list_all_common_position = pos
        else:
            set1 = {re.match(r'[^:]+',stringa).group() for stringa in list_all_common_position} 
            set2 = {re.match(r'[^:]+',stringa).group() for stringa in pos}
            list_all_common_position = set1.intersection(set2)
    
    #ordina le posizioni tramite una lambda expression
    list_all_common_position = sorted(list_all_common_position, key=lambda x: int(x.split()[1]))

    for pos in list_all_common_position:
        print(pos)
    print()
    print('Numero di posizioni del reference rispetto a cui tutti i genomi variano: '+ str(len(list_all_common_position)))
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def all_common_variation(lista_variazioni):

    list_all_common_variation = []
    
    print('Elenco delle posizioni del reference rispetto a cui tutti i genomi variano allo stesso modo: ')
    print()

    for var in lista_variazioni:
        if list_all_common_variation == []:
            list_all_common_variation = var
        else:
            set1 = set(list_all_common_variation)
            set2 = set(var)
            
            list_all_common_variation = set1.intersection(set2)
    
    #ordina le posizioni tramite una lambda expression
    list_all_common_variation = sorted(list_all_common_variation, key=lambda x: int(x.split()[1]))

    for var in list_all_common_variation:
        print(var)

   
    print()
    print('Numero di posizioni del reference rispetto a cui tutti i genomi variano allo stesso modo: '+ str(len(list_all_common_variation)))
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

                
main()

            
        





