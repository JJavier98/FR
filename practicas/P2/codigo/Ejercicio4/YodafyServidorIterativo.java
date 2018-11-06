import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

//
// YodafyServidorIterativo
// (CC) jjramos, 2012
//
public class YodafyServidorIterativo {

	public static void main(String[] args) {
		
		// Puerto de escucha
		int port=8989;
		try
		{
			DatagramSocket socketUDP = new DatagramSocket(port);
			byte []buffer=new byte[1000];

			do
			{
				// Creamos un objeto de la clase ProcesadorYodafy, pasándole como 
				// argumento el nuevo socket, para que realice el procesamiento
				// Este esquema permite que se puedan usar hebras más fácilmente.
				ProcesadorYodafy procesador=new ProcesadorYodafy(socketUDP);
				procesador.procesa();


			} while (true);
			
		}
		catch (IOException e) {
			System.err.println("Error al escuchar en el puerto "+port);
		}

	}

}
