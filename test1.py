import argparse
import re

filepath = './MAFFT.fa'

def main():

    lista_seq = read_file(filepath)

    ref = lista_seq[0]
    #rimuoviamo ref dalla lista
    lista_seq.pop(0)

    variazioni(lista_seq, ref)

def read_file(filepath):

    lista_elementi = []
    nomi_sequenze = []
    elemento_corrente = ""

    with open(filepath, 'r') as file:   
        for linea in file:
            if linea.startswith('>'):
                if elemento_corrente != "":  # Se abbiamo già raccolto una sequenza, la aggiungiamo alla lista
                    lista_elementi.append(elemento_corrente)
                    elemento_corrente = ""  
            else:
                elemento_corrente += linea.strip()  # Aggiungiamo la linea corrente (senza '\n') alla sequenza

        # Aggiungiamo l'ultimo elemento alla lista, se esiste
        if elemento_corrente:
            lista_elementi.append(elemento_corrente)
       
    return lista_elementi

def variazioni(lista_delle_sequenze, ref):

    start = 0
    end = len(ref)
    lista=[]

    for elemento in lista_delle_sequenze:
        for i, base in enumerate(elemento): 
                if base == '-': 
                    continue        
                else:
                    start = i
                    break
                
        for i in reversed(range(len(elemento))):
                if elemento[i] == '-': 
                    continue        
                else:
                    end = i+1
                    break       
        
        listina = []

        for i, base in enumerate(elemento[start: end]): 
            if base != ref[i+start]:
                if base == '-': 
                    # print('posizione', i+start, ': inserimento di', ref[i+start])
                    listina.append(('posizione '+str(i+start+1)+' : inserimento di '+ref[i+start]))
                if base == {'A','C','G','T','N'} and ref[i+start] == '-': 
                    #print('posizione', i+start, ': cancellazione di', base) 
                    listina.append(('posizione '+str(i+start+1)+' : cancellazione di '+base))
                if base == {'A','C','G','T'} and ref[i+start] =='N' :
                    continue
                elif base in {'A','C','G','T'} and ref[i+start] != base:
                    #print('posizione', i+start, ': sostituzione ', ref[i+start], '->', base)
                    listina.append( ('posizione '+str(i+start+1)+' : sostituzione '+ref[i+start]+' -> '+base))

        lista.append( listina)
    
    stampo_tutte_var(lista)
#   print(lista)

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

    print('genoma' ,lista_gen[maxlista] ,'massimo: ', max(len(elemento) for elemento in lista)) 
    print('genoma' ,lista_gen[minlista] ,'minimo: ', min(len(elemento) for elemento in lista)) 
    
    print('-----------------------------------------------------------------------------------------------------------------')

    lista_var_in_tutte = []
     
    for elemento in lista:
        if lista_var_in_tutte == []:
            lista_var_in_tutte = elemento
        else:
            set1 = {re.match(r'[^:]+',stringa).group() for stringa in lista_var_in_tutte} 
            set2 = {re.match(r'[^:]+',stringa).group() for stringa in elemento}
            lista_var_in_tutte = set1.intersection(set2)
    
    #ordina le posizioni tramite una lambda expression
    lista_var_in_tutte = sorted(lista_var_in_tutte, key=lambda x: int(x.split()[1]))

    for elemento in lista_var_in_tutte:
        print(elemento)

    print(len(lista_var_in_tutte))


    
    print('-----------------------------------------------------------------------------------------------------------------')



    lista_var_in_tutte_uguale = []
     
    for elemento in lista:
        if lista_var_in_tutte_uguale == []:
            lista_var_in_tutte_uguale = elemento
        else:
            set1 = set(lista_var_in_tutte_uguale)
            set2 = set(elemento)
            
            lista_var_in_tutte_uguale = set1.intersection(set2)
    
    #ordina le posizioni tramite una lambda expression
    lista_var_in_tutte_uguale = sorted(lista_var_in_tutte_uguale, key=lambda x: int(x.split()[1]))

    for elemento in lista_var_in_tutte_uguale:
        print(elemento)

    print(len(lista_var_in_tutte_uguale))

def cerco_gen(filepath):

    with open(filepath, 'r') as file:
        testo = file.read()
        patter = r'>([^ ]+)'
        corrispondenze = re.findall(patter , testo)
        #rimuoviamo ref dalla lista      
        corrispondenze.pop(0)
        
    return corrispondenze
    

def stampo_tutte_var(lista):

    lista_nomi=cerco_gen(filepath)
    for i, nome in enumerate(lista_nomi):
        print(nome)
        for i in lista[i]:
                print(i)
        print('------------------------------------------------------------------------------------')



                
main()

            
        





