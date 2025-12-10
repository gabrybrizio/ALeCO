import pandas as pd
from _6AlgoritmiGreedy import genera_istanza

def knapsack_dp_bottom_up():
    print("--- RISOLUZIONE KNAPSACK PROBLEM (DP - BOTTOM UP) ---\n")

    # 1. Generazione Istanza
    N_OGGETTI = 4
    P_MAX = 50
    W_MAX = 20
    profitti, pesi, C = genera_istanza(N_OGGETTI, W_MAX, P_MAX)

    print(f"Capacità Zaino (C): {C}")
    print(f"Vettore Profitti (p): {profitti}")
    print(f"Vettore Pesi (w):     {pesi}")
    print("-" * 50)

    # Corrispondenza con la teoria (dove spesso gli indici partono da 1), aggiunendo un elemento fittizio all'inizio delle liste.
    w = [0] + pesi
    p = [0] + profitti

    # 2. INIZIALIZZAZIONE MATRICE (Tabella Z)
    # Creiamo una matrice (n+1) x (C+1) inizializzata a 0
    # Righe (i): da 0 a n (oggetti)
    # Colonne (d): da 0 a C (capacità parziali)
    z = [[0 for _ in range(C + 1)] for _ in range(N_OGGETTI + 1)]

    # 3. LOGICA DELL'ALGORITMO (Cicli annidati)
    print("Calcolo della matrice Z...")
    
    for i in range(1, N_OGGETTI + 1):
        for d in range(1, C + 1):
            
            # CASO 1: L'oggetto è troppo pesante per la capacità attuale d
            if w[i] > d:
                z[i][d] = z[i-1][d]
            
            # CASO 2: L'oggetto può entrare
            else:
                # Confrontiamo due opzioni:
                # 1. NON prenderlo: z[i-1][d] (valore della riga sopra)
                # 2. PRENDERLO: p[i] + valore ottimo con la capacità residua (z[i-1][d - w[i]])
                valore_senza = z[i-1][d]
                valore_con = p[i] + z[i-1][d - w[i]]
                
                z[i][d] = max(valore_senza, valore_con)

    # Il valore ottimo è nell'ultima cella in basso a destra
    ottimo_globale = z[N_OGGETTI][C]

    # 4. OUTPUT: STAMPA DELLA MATRICE
    df = pd.DataFrame(z, columns=[f"d={c}" for c in range(C+1)], index=[f"Obj {i}" for i in range(N_OGGETTI+1)])
    print("\nMatrice Z (Righe=Oggetti, Colonne=Capacità):")
    print(df)
    print("-" * 60)
    print(f"VALORE OTTIMO CALCOLATO (Z[n][C]): {ottimo_globale}")
    print("-" * 60)

    # 5. RICOSTRUZIONE DELLA SOLUZIONE (Backtracking)
    # Risaliamo dalla cella Z[n][C] per capire quali decisioni sono state prese
    print("\nRicostruzione oggetti scelti (Backtracking):")
    
    res = ottimo_globale
    w_residuo = C
    oggetti_presi = []

    for i in range(N_OGGETTI, 0, -1): # Partiamo dall'ultimo oggetto e andiamo all'indietro
        # Se il valore è diverso da quello della riga sopra, significa che l'oggetto i è stato INCLUSO
        if res != z[i-1][w_residuo]:
            oggetti_presi.append(i) # Salviamo l'indice (1-based)
            
            print(f"-> Oggetto {i} selezionato (Peso: {w[i]}, Profitto: {p[i]})")
            print(f"   Motivo: Z[{i}][{w_residuo}] ({z[i][w_residuo]}) != Z[{i-1}][{w_residuo}] ({z[i-1][w_residuo]})")
            
            res -= p[i]       # Riduciamo il profitto rimanente da cercare
            w_residuo -= w[i] # Riduciamo la capacità disponibile
        else:
            # L'oggetto non è stato preso, passiamo alla riga sopra mantenendo lo stesso w_residuo
            pass

    print(f"\nSoluzione finale (indici oggetti): {oggetti_presi[::-1]}")

# Esecuzione
if __name__ == "__main__":
    knapsack_dp_bottom_up()