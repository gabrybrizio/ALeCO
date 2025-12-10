public class _3Backtrack {

    /**
     * Metodo wrapper per avviare la visualizzazione pulita.
     */
    public static void risolvi(boolean[][] grafo, int m) {
        int n = grafo.length;
        int[] soluzione = new int[n];
        System.out.println("--- INIZIO BACKTRACKING (m=" + m + ") ---");
        System.out.println("Legenda: [NODO] := COLORE ? -> Esito");
        risposte(grafo, m, soluzione, 0);
        System.out.println("--- FINE RICERCA ---");
    }

    /**
     * Metodo Core con stampe di debug per l'albero.
     */
    private static void risposte(boolean[][] grafo, int m, int[] soluzione, int j) {
        // Calcoliamo l'indentazione grafica basata su 'j'
        String indent = "    ".repeat(j); // Richiede Java 11+, altrimenti usa un ciclo for

        // 1. CHECK VALIDITÀ (Bound)
        // Verifichiamo se l'assegnazione fatta al livello precedente (j-1) è valida.
        if (rifiuta(grafo, soluzione, j)) {
            // Se c'è conflitto, stampiamo il taglio del ramo e torniamo indietro.
            System.out.println(indent + "❌ RIFIUTA (Conflitto rilevato)");
            return; // PRUNING (Backtracking)
        }

        // 2. CHECK COMPLETAMENTO
        if (completa(soluzione, j)) {
            System.out.println(indent + "✅ SOLUZIONE TROVATA: " + toString(soluzione, j));
            // Non c'è return qui se vogliamo trovare TUTTE le soluzioni.
            // Se ne volessimo solo una, potremmo mettere un return o lanciare un'eccezione.
        } else {
            // 3. BRANCHING (Generazione Figli)
            // Se siamo qui, il nodo parziale è valido, ma non completo. Espandiamo.
            
            for (int c = 0; c < m; c++) {
                // Azione: Assegna colore
                soluzione[j] = c; 
                
                // Visualizzazione tentativo
                System.out.println(indent + "🔹 [Nodo " + j + "] := Colore " + c + " ?");
                
                // Chiamata Ricorsiva
                risposte(grafo, m, soluzione, j + 1);
                
                // (Al ritorno dalla ricorsione, il ciclo continua col prossimo colore)
            }
        }
    }

    // --- FUNZIONI DI SUPPORTO (Invariate nella logica) ---

    public static boolean completa(int[] a, int j) {
        return j == a.length;
    }

    private static boolean rifiuta(boolean[][] grafo, int[] soluzione, int j) {
        boolean rifiuta = false;
        // Verifica conflitti tra il nodo appena inserito (j-1) e i precedenti
        if (grafo.length > 1 && j >= 2) {
            for (int i = 0; i < j - 1 && !rifiuta; i++) {
                if (grafo[j - 1][i] || grafo[i][j - 1]) { // Se adiacenti
                    if (soluzione[j - 1] == soluzione[i]) { // E stesso colore
                        rifiuta = true;
                    }
                }
            }
        }
        return rifiuta;
    }

    private static String toString(int[] soluzione, int j) {
        StringBuilder sb = new StringBuilder("[");
        for(int i=0; i<j; i++) sb.append(soluzione[i]).append(i<j-1?",":"");
        sb.append("]");
        return sb.toString();
    }

    // --- MAIN DI ESEMPIO ---
    public static void main(String[] args) {
        // Definiamo un grafo semplice a 3 nodi (Triangolo: tutti collegati tra loro)
        // 0 -- 1
        //  \  /
        //   2
        boolean[][] grafo = {
            {false, true, false},  // Nodo 0 collegato a 1
            {true, false, true},  // Nodo 1 collegato a 0 e 2
            {false, true, false},   // Nodo 2 collegato a 0 e 1
        };

        // Proviamo a colorarlo con 2 colori (Impossibile -> molto pruning)
        // Poi con 3 colori (Possibile)
        risolvi(grafo, 3);
    }
}