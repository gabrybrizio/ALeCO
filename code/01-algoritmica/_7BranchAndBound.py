import collections
from _6AlgoritmiGreedy import genera_istanza 

class Nodo:
    """
    Rappresenta un nodo nell'albero (E-node) con metadati per la visualizzazione.
    """
    def __init__(self, id_nodo, id_padre, livello, profitto, peso, decisione=None):
        self.id = id_nodo           # Identificativo univoco
        self.parent_id = id_padre   # ID del nodo padre
        self.livello = livello      # Indice oggetto corrente
        self.profitto = profitto
        self.peso = peso
        self.bound = 0.0
        self.decisione = decisione  # "IN" (preso) o "OUT" (scartato)
        self.stato = "APERTO"       # Stati: APERTO, CHIUSO (foglia), PRUNED (tagliato), INFEASIBLE (peso eccessivo)

class KPFIFOBB_Visual:
    """
    Versione con visualizzazione dell'albero.
    """
    def __init__(self, profitti, pesi, capacita):
        self.C = capacita
        self.z_star = 0  
        self.n = len(profitti)
        self.nodi_generati = [] # Archivio per la stampa finale
        self.node_counter = 0   # Contatore per ID univoci
        
        # PRE-PROCESSING (Ordinamento)
        items = []
        for i, (p, w) in enumerate(zip(profitti, pesi)):
            items.append({'orig_id': i, 'p': p, 'w': w, 'ratio': p/w})
        
        self.items = sorted(items, key=lambda x: x['ratio'], reverse=True)

    def _nuovo_nodo(self, parent_id, livello, profitto, peso, decisione):
        """Helper per creare e registrare un nodo."""
        nodo = Nodo(self.node_counter, parent_id, livello, profitto, peso, decisione)
        self.node_counter += 1
        self.nodi_generati.append(nodo)
        return nodo

    def stimaCostoPerEccesso(self, nodo):
        # Stessa logica Greedy-LKP (z_LP)
        if nodo.peso > self.C:
            return 0.0

        bound = float(nodo.profitto)
        peso_totale = nodo.peso
        j = nodo.livello + 1
        
        while j < self.n:
            item = self.items[j]
            if peso_totale + item['w'] <= self.C:
                peso_totale += item['w']
                bound += item['p']
                j += 1
            else:
                residuo = self.C - peso_totale
                bound += residuo * (item['p'] / item['w'])
                break 
        return bound

    def rifiuta(self, nodo):
        return nodo.peso > self.C

    def accetta(self, nodo):
        if not self.rifiuta(nodo):
            if nodo.profitto > self.z_star:
                self.z_star = nodo.profitto

    def completo(self, nodo):
        nodo.bound = self.stimaCostoPerEccesso(nodo)
        
        # Check Ammissibilità
        if self.rifiuta(nodo):
            nodo.stato = "INFEASIBLE (Peso > C)"
            return True

        # Check Soluzione
        if nodo.livello == self.n - 1:
            nodo.stato = "SOLUZIONE"
            return True
            
        # Check Bounding (Pruning)
        # UB <= LB -> Taglio
        if nodo.bound <= self.z_star:
            nodo.stato = f"PRUNED (UB {nodo.bound:.1f} <= z* {self.z_star})"
            return True
            
        return False

    def risposte(self):
        Q = collections.deque()
        
        # Radice
        root = self._nuovo_nodo(parent_id=-1, livello=-1, profitto=0, peso=0, decisione="ROOT")
        root.bound = self.stimaCostoPerEccesso(root)
        
        if root.bound > self.z_star:
            Q.append(root)
        else:
            root.stato = "PRUNED_ROOT"
        
        while Q:
            u = Q.popleft()
            
            # Controllo ritardato del bound (poiché z* potrebbe essere aumentato)
            if u.bound <= self.z_star and u.id != 0: # Saltiamo check su root
                u.stato = f"PRUNED (Late) (UB {u.bound:.1f} <= z* {self.z_star})"
                continue
            
            next_level = u.livello + 1
            if next_level >= self.n: continue

            next_item = self.items[next_level]
            
            # --- FIGLIO SINISTRO (IN - Prendo l'oggetto) ---
            v_in = self._nuovo_nodo(u.id, next_level, 
                                    u.profitto + next_item['p'], 
                                    u.peso + next_item['w'], 
                                    decisione="SX (IN)")
            
            # Logica specifica: Aggiorno z* PRIMA di controllare completo()
            # Questo aiuta a potare più rami successivamente
            self.accetta(v_in)
            
            if not self.completo(v_in):
                Q.append(v_in)
            
            # --- FIGLIO DESTRO (OUT - Lascio l'oggetto) ---
            v_out = self._nuovo_nodo(u.id, next_level, 
                                     u.profitto, 
                                     u.peso, 
                                     decisione="DX (OUT)")
            
            if not self.completo(v_out):
                Q.append(v_out)
                
        return self.z_star

    def stampa_albero(self):
        """
        Ricostruisce la gerarchia dai nodi salvati e stampa l'albero.
        """
        print("\n--- ALBERO DI RICERCA (Visualizzazione Gerarchica) ---")
        print("Legenda: [ID] Decisione | Peso, Profitto | UB=Upper Bound | Stato")
        
        # Mappa i figli per ogni genitore per la stampa ricorsiva
        children_map = collections.defaultdict(list)
        root = None
        for node in self.nodi_generati:
            if node.parent_id == -1:
                root = node
            else:
                children_map[node.parent_id].append(node)
        
        def print_recursive(node, prefix="", is_last=True):
            # Simboli per l'albero
            connector = "└── " if is_last else "├── "
            
            # Formattazione info nodo
            info = f"[{node.id}] {node.decisione:<8} | w:{node.peso:<2} p:{node.profitto:<2} | UB:{node.bound:<4.1f}"
            
            # Aggiunta stato se non è APERTO
            if node.stato != "APERTO":
                info += f" -> {node.stato}"
            
            print(f"{prefix}{connector}{info}")
            
            # Gestione prefisso per i figli
            new_prefix = prefix + ("    " if is_last else "│   ")
            
            children = children_map[node.id]
            count = len(children)
            for i, child in enumerate(children):
                print_recursive(child, new_prefix, i == count - 1)

        if root:
            print_recursive(root)
        else:
            print("Nessun albero generato.")

# --------------------------------------------------------------------------
# MAIN DI TEST
# --------------------------------------------------------------------------
if __name__ == "__main__":
    # 1. Generazione Istanza
    N_OGGETTI = 4
    P_MAX = 50
    W_MAX = 20
    profitti, pesi, capacita = genera_istanza(N_OGGETTI, W_MAX, P_MAX)

    print(f"\nCapacità Zaino (C): {capacita}")
    print(f"Vettore Profitti (p): {profitti}")
    print(f"Vettore Pesi (w):     {pesi}")
    print("-" * 50)
    
    solver = KPFIFOBB_Visual(profitti, pesi, capacita)
    opt = solver.risposte()
    
    print(f"\nSOLUZIONE OTTIMA (z*): {opt}")
    
    # QUI GENERIAMO LA GRAFICA
    solver.stampa_albero()