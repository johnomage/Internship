import java.util.Scanner;
import java.io.File;
import org.encog.neural.data.NeuralDataSet;
import org.encog.neural.networks.BasicNetwork;
import org.encog.neural.networks.training.Train;
import org.encog.neural.networks.training.propagation.resilient.ResilientPropagation;
import org.encog.persist.EncogPersistedCollection;

class Hello{
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("Enter name: ");
        String edus = input.nextLine();
        input.close();
        System.out.println("Hello, " + edus);
        System.out.println(add_num(30,24));
    }

    public static int add_num(int a, int b){
        return a + b;
    }
}