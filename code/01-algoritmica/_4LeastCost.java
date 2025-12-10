import java.util.*;

// 1. STRUTTURA DEL NODO
class ArrIntInt {
    private static int ID_COUNTER = 0; // Contatore statico per ID univoci
    
    public int id;          // ID univoco del nodo
    public int parentId;    // ID del padre 
    public int[] perm;      // La permutazione
    public int level;       // Livello (Profondità)
    public double cost;     // Costo (per LC)

    public ArrIntInt(int[] perm, int level, int parentId) {
        this.id = ID_COUNTER++;
        this.parentId = parentId;
        this.perm = perm;
        this.level = level;
        this.cost = 0.0;
    }
    
    public static void resetCounter() { ID_COUNTER = 0; }

    @Override
    public String toString() {
        return Arrays.toString(perm);
    }
}

// INTERFACCIA STRATEGIA (Invariata)
interface Strategy {
    void add(ArrIntInt node);
    ArrIntInt remove();
    boolean isEmpty();
    String getName();
}

// --- IMPLEMENTAZIONI STRATEGIE ---

class FifoStrategy implements Strategy {
    private Queue<ArrIntInt> queue = new LinkedList<>();
    public void add(ArrIntInt node) { queue.offer(node); }
    public ArrIntInt remove() { return queue.poll(); }
    public boolean isEmpty() { return queue.isEmpty(); }
    public String getName() { return "FIFO (Breadth-First / A Livelli)"; }
}

class LifoStrategy implements Strategy {
    private Stack<ArrIntInt> stack = new Stack<>();
    public void add(ArrIntInt node) { stack.push(node); }
    public ArrIntInt remove() { return stack.pop(); }
    public boolean isEmpty() { return stack.isEmpty(); }
    public String getName() { return "LIFO (Depth-First / In Profondità)"; }
}

class LeastCostStrategy implements Strategy {
    private PriorityQueue<ArrIntInt> pq;
    private double wH, wG;

    public LeastCostStrategy(double wH, double wG) {
        this.wH = wH; this.wG = wG;
        // Ordina per costo crescente
        this.pq = new PriorityQueue<>(Comparator.comparingDouble(n -> n.cost));
    }

    public void add(ArrIntInt node) {
        // Funzione Costo: c(x) = wH*level + wG*euristica
        node.cost = (wH * node.level) + (wG * 0); 
        pq.offer(node);
    }
    public ArrIntInt remove() { return pq.poll(); }
    public boolean isEmpty() { return pq.isEmpty(); }
    public String getName() { return "Least-Cost (wLevel=" + wH + ")"; }
}

// ----------------------------------------------------------
// 2. SOLVER CON VISUALIZZAZIONE GRAFICA
// ----------------------------------------------------------
public class _4LeastCost {

    public static void solve(int[] input, Strategy strategy) {
        ArrIntInt.resetCounter(); // Reset ID per ogni run
        System.out.println("\n==================================================");
        System.out.println(" STRATEGIA: " + strategy.getName());
        System.out.println(" Legenda: [ID] (Padre) | Costo | Stato");
        System.out.println("==================================================");
        
        int n = input.length;
        
        // Radice (Parent ID = -1)
        ArrIntInt root = new ArrIntInt(input.clone(), 0, -1);
        strategy.add(root);

        while (!strategy.isEmpty()) {
            
            // A. SELEZIONE (E-Node)
            ArrIntInt u = strategy.remove();
            
            // VISUALIZZAZIONE NODO
            printNodeVisual(u);

            // B. CONTROLLO FINE (Foglia)
            if (u.level == n) {
                System.out.println(getIndent(u.level) + "   ✨ SOLUZIONE COMPLETA");
                continue; 
            }

            // C. BRANCHING
            for (int i = n - 1; i >= u.level; i--) {
                int[] newPerm = u.perm.clone();
                swap(newPerm, u.level, i);
                
                ArrIntInt v = new ArrIntInt(newPerm, u.level + 1, u.id);
                strategy.add(v);
            }
        }
    }

    // --- METODI DI VISUALIZZAZIONE ---

    // Crea l'indentazione grafica ad albero
    private static void printNodeVisual(ArrIntInt u) {
        String indent = getIndent(u.level);
        
        // Connettore grafico
        String connector = (u.level == 0) ? "ROOT" : "└──";
        
        // Formattazione stringa
        System.out.printf("%s%s [%d] (p:%d) | c:%.1f | %s%n", 
            indent, connector, u.id, u.parentId, u.cost, Arrays.toString(u.perm));
    }

    private static String getIndent(int level) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < level; i++) {
            sb.append("    "); // 4 spazi per livello
        }
        return sb.toString();
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    // ----------------------------------------------------------
    // MAIN DI TEST
    // ----------------------------------------------------------
    public static void main(String[] args) {
        int[] input = {1, 2, 3};

        // 1. LIFO (Depth-First): Vedrai una struttura ad albero classica, scendendo subito.
        solve(input, new LifoStrategy());

        // 2. FIFO (Breadth-First): Vedrai l'albero espandersi per livelli (tutti i nodi liv 1, poi liv 2).
        solve(input, new FifoStrategy());
        
        // 3. Least-Cost (Simulazione DFS): PriorityQueue che premia la profondità.
        solve(input, new LeastCostStrategy(-1.0, 0.0));
    }
}