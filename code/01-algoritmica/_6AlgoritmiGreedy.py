import random
import math

def genera_istanza(n, peso_max, profitto_max, fattore_capacita=0.5):
    """
    Genera un'istanza casuale del problema dello zaino.
    
    Args:
        n (int): Numero di oggetti.
        peso_max (int): Peso massimo possibile per un oggetto.
        profitto_max (int): Profitto massimo possibile per un oggetto.
        fattore_capacita (float): Determina la capacità C come % della somma dei pesi.
        
    Returns:
        tuple: (profitti, pesi, capacita)
    """
    w = [random.randint(1, peso_max) for _ in range(n)]
    p = [random.randint(1, profitto_max) for _ in range(n)]
    
    # La capacità è definita come una frazione della somma totale dei pesi
    C = int(sum(w) * fattore_capacita)
    
    return p, w, C

def risolvi_knapsack_gerarchia(p, w, C):
    """
    Esegue gli algoritmi Greedy e verifica la gerarchia delle approssimazioni.
    
    1. Greedy-split (p_hat): Profitto fermandosi prima dell'oggetto che sfora.
    2. Greedy Standard (z_G): Continua dopo lo split per riempire i buchi.
    3. Rilassamento Lineare (z_LP): Riempie esattamente la capacità con una frazione dello split.
    """
    n = len(p)
    
    # ---------------------------------------------------------
    # FASE 1: Pre-processing e Ordinamento
    # ---------------------------------------------------------
    # Creiamo una lista di dizionari per mantenere l'associazione indice-dati
    oggetti = []
    for i in range(n):
        efficienza = p[i] / w[i] # p_i / w_i
        oggetti.append({
            'id': i,
            'p': p[i],
            'w': w[i],
            'ratio': efficienza
        })
    
    # Ordiniamo in modo DECRESCENTE basandoci sul rapporto tra valore e peso
    oggetti_ordinati = sorted(oggetti, key=lambda x: x['ratio'], reverse=True)
    
    # ---------------------------------------------------------
    # FASE 2: Esecuzione degli Algoritmi
    # ---------------------------------------------------------
    
    peso_corrente = 0
    profitto_corrente = 0
    
    z_split = 0      # Greedy-split (p_hat)
    z_greedy = 0     # Greedy Standard (z_G)
    z_lp = 0.0       # Linear Relaxation (z_LP)
    
    split_index = -1 # Per tracciare dove ci siamo fermati
    
    # Ciclo principale
    for i, obj in enumerate(oggetti_ordinati):
        if peso_corrente + obj['w'] <= C:
            # L'oggetto entra interamente
            peso_corrente += obj['w']
            profitto_corrente += obj['p']
        else:
            # L'oggetto NON entra -> Abbiamo trovato l'elemento SPLIT (break item)
            split_index = i
            item_split = obj
            
            # --- 1. Calcolo Greedy-split (p_hat) ---
            # È il profitto accumulato ESCLUSO l'elemento split
            z_split = profitto_corrente 
            
            # --- 2. Calcolo Rilassamento Lineare (z_LP) ---
            # Formula: Profitto corrente + (Capacità residua * Efficienza elemento split)
            # NOTA: Usiamo p_split / w_split. La formula teorica è:
            # z_LP = p_hat + (C - w_hat) * (p_s / w_s)
            capacita_residua = C - peso_corrente
            z_lp = profitto_corrente + (capacita_residua * item_split['ratio'])
            
            # Interrompiamo il riempimento qui, ma per il 
            # Greedy Standard dobbiamo continuare a scorrere la lista
            break
            
    # --- 3. Completamento Greedy Standard (z_G) ---
    # Partiamo dalla situazione dello split e vediamo se gli oggetti SUCCESSIVI entrano nello spazio rimasto.
    z_greedy = z_split
    peso_greedy = peso_corrente # Peso accumulato prima dello split
    
    # Se abbiamo trovato uno split (cioè non abbiamo preso TUTTI gli oggetti)
    if split_index != -1:
        for i in range(split_index + 1, n):
            obj = oggetti_ordinati[i]
            if peso_greedy + obj['w'] <= C:
                peso_greedy += obj['w']
                z_greedy += obj['p']
    else:
        # Caso limite: Tutti gli oggetti entravano nello zaino
        z_split = profitto_corrente
        z_greedy = profitto_corrente
        z_lp = float(profitto_corrente)

    return z_split, z_greedy, z_lp, oggetti_ordinati

# ---------------------------------------------------------
# MAIN: Esecuzione e Verifica
# ---------------------------------------------------------
if __name__ == "__main__":
    print("--- DIMOSTRAZIONE GERARCHIA GREEDY (KNAPSACK) ---\n")
    
    # 1. Generazione Istanza
    N_OGGETTI = 10
    P_MAX = 50
    W_MAX = 20
    p_vect, w_vect, Cap = genera_istanza(N_OGGETTI, W_MAX, P_MAX)
    
    print(f"Capacità Zaino (C): {Cap}")
    print(f"Vettore Profitti (p): {p_vect}")
    print(f"Vettore Pesi (w):     {w_vect}")
    print("-" * 50)
    
    # 2. Risoluzione
    p_hat, z_G, z_LP, ordinati = risolvi_knapsack_gerarchia(p_vect, w_vect, Cap)
    
    # Visualizzazione Ordinamento (Didattica)
    print("Oggetti ordinati per efficienza (p/w) decrescente:")
    print(f"{'ID':<4} {'Prof':<6} {'Peso':<6} {'Ratio (p/w)':<12}")
    for obj in ordinati:
        print(f"{obj['id']:<4} {obj['p']:<6} {obj['w']:<6} {obj['ratio']:.2f}")
    print("-" * 50)
    
    # 3. Risultati
    z_LP_floor = math.floor(z_LP)
    
    print(f"RISULTATI ALGORITMI:")
    print(f"1. Greedy-split (p_hat):  {p_hat}")
    print(f"2. Greedy Standard (z_G): {z_G}")
    print(f"3. Greedy-LKP (z_LP):     {z_LP:.2f} (Floor: {z_LP_floor})")
    
    print("-" * 50)
    
    # 4. Verifica della Gerarchia Teorica
    # Teoria: p_hat <= z_G <= floor(z_LP) <= z_LP
    
    check_1 = p_hat <= z_G
    check_2 = z_G <= z_LP_floor
    check_3 = z_LP_floor <= z_LP
    
    # Costruiamo la stringa di disuguaglianza con i valori reali
    formula_str = f"{p_hat} <= {z_G} <= {z_LP_floor} <= {z_LP:.2f}"
    
    print(f"Verifica Gerarchia: {formula_str}")
    
    if check_1 and check_2 and check_3:
        print("\n[SUCCESSO] La gerarchia delle approssimazioni è RISPETTATA.")
        print("Nota Didattica: z_LP è un Upper Bound valido per la soluzione intera ottima.")
        print("Nel Branch&Bound, usiamo z_LP per decidere se tagliare un nodo.")
    else:
        print("\n[ATTENZIONE] Qualcosa non torna nella gerarchia (controllare casi limite).")