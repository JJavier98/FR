import java.net.ServerSocket;
import java.net.Socket;

public class Hebrita extends Thread
{
	// En este ejemplo almacenamos el número
	// de ejecuciones del bucle principal.
	private Socket socket;
	// En el constructor podemos pasarle alguna variable que hayamos
	// creado en otra clase. Así podemos compartir algunos datos.
	Hebrita(Socket s)
	{
		this.socket=s;
	}
	// El contenido de este método se ejecutará tras llamar al
	// método "start()". Se trata del procesamiento de la hebra.
	public void run()
	{
		int i = 1;
		int sum = 0;
		while(i < 1000000000)
		{
			sum += i;
			sum /= i;
			++i;
		}

		System.out.println(sum);
		ProcesadorYodafy procesador = new ProcesadorYodafy(socket);
		procesador.procesa();
	}
}
