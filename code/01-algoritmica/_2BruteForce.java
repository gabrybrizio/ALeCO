import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

class Quesito {
    int id;
    int votoMax;        // Peso
    double votoAssegnato; // Valore

    public Quesito(int id, int votoMax, double votoAssegnato) {
        this.id = id;
        this.votoMax = votoMax;
        this.votoAssegnato = votoAssegnato;
    }
}

public class _2BruteForce {

    static double maxValoreTrovato = -1;
    static List<Quesito> soluzioneOttima = new ArrayList<>();
    static long combinazioniTotali = 0;
    static long combinazioniValide = 0;

    public static void main(String[] args) {
        // --- CONFIGURAZIONE DATI ---
        List<Quesito> lista = new ArrayList<>();
        // Inserisco pochi elementi (6) perché 2^6 = 64 combinazioni.
        lista.add(new Quesito(1, 3, 1.5));
        lista.add(new Quesito(2, 3, 1.0));
        lista.add(new Quesito(3, 3, 3.0));
        lista.add(new Quesito(4, 5, 4.5)); 
        lista.add(new Quesito(5, 10, 8.0));
        lista.add(new Quesito(6, 2, 0.0));

        int capienzaMax = 12; // Limite stretto per forzare combinazioni non valide

        System.out.println("--- GENERATORE PURO SPAZIO DEGLI STATI ---");
        System.out.println("Quesiti: " + lista.size() + " | Capienza Max: " + capienzaMax);
        System.out.println("L'algoritmo genererà tutte le 2^" + lista.size() + " = " + (int)Math.pow(2, lista.size()) + " combinazioni.");
        System.out.println("---------------------------------------------------------------");
        System.out.printf("%-30s | %-10s | %-10s | %s%n", "Combinazione (ID)", "Peso Tot", "Valore", "Stato");
        System.out.println("---------------------------------------------------------------");

        // Avvio algoritmo
        generaTutteLeCombinazioni(lista, capienzaMax, 0, new ArrayList<>());

        // Report Finale
        System.out.println("---------------------------------------------------------------");
        System.out.println("MIGLIORE SOLUZIONE TROVATA:");
        if (!soluzioneOttima.isEmpty()) {
            int pesoOttimo = soluzioneOttima.stream().mapToInt(q -> q.votoMax).sum();
            String ids = soluzioneOttima.stream().map(q -> String.valueOf(q.id)).collect(Collectors.joining(","));
            System.out.println("Quesiti: [" + ids + "]");
            System.out.println("Peso: " + pesoOttimo + " / " + capienzaMax);
            System.out.println("Valore Totale: " + maxValoreTrovato);
        } else {
            System.out.println("Nessuna soluzione valida trovata.");
        }
        System.out.println("Totale combinazioni generate: " + combinazioniTotali);
        System.out.println("Di cui valide (Peso <= Max): " + combinazioniValide);
    }

    /**
     * Genera ogni possibile sottoinsieme.
     */
    public static void generaTutteLeCombinazioni(List<Quesito> quesiti, int capienzaMax, int indice, List<Quesito> selezioneAttuale) {

        // CASO BASE: Siamo arrivati alla fine della lista di quesiti (Foglia dell'albero)
        if (indice == quesiti.size()) {
            combinazioniTotali++;
            
            // Calcolo somme attuali
            int pesoTotale = selezioneAttuale.stream().mapToInt(q -> q.votoMax).sum();
            double valoreTotale = selezioneAttuale.stream().mapToDouble(q -> q.votoAssegnato).sum();

            // Creazione stringa ID per output pulito
            String ids = selezioneAttuale.isEmpty() ? "{}" : 
                         "{" + selezioneAttuale.stream().map(q -> String.valueOf(q.id)).collect(Collectors.joining(",")) + "}";

            // VALIDAZIONE: È qui che controlliamo se la soluzione è ammissibile
            boolean isValid = pesoTotale <= capienzaMax;
            String stato = isValid ? "VALIDA" : "SCARTATA (Peso > " + capienzaMax + ")";

            // Stampa riga sintetica
            System.out.printf("%-30s | %-10d | %-10.1f | %s%n", ids, pesoTotale, valoreTotale, stato);

            // Se valida, controlliamo se è la migliore
            if (isValid) {
                combinazioniValide++;
                if (valoreTotale > maxValoreTrovato) {
                    maxValoreTrovato = valoreTotale;
                    soluzioneOttima = new ArrayList<>(selezioneAttuale);
                }
            }
            return;
        }

        Quesito q = quesiti.get(indice);

        selezioneAttuale.add(q);
        generaTutteLeCombinazioni(quesiti, capienzaMax, indice + 1, selezioneAttuale);
        
        selezioneAttuale.remove(selezioneAttuale.size() - 1);

        generaTutteLeCombinazioni(quesiti, capienzaMax, indice + 1, selezioneAttuale);
    }
}