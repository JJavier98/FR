//
// YodafyServidorIterativo
// (CC) jjramos, 2012
//
import java.io.*;
import java.util.Random;
import java.net.*;

//
// Nota: si esta clase extendiera la clase Thread, y el procesamiento lo hiciera el método "run()",
// ¡Podríamos realizar un procesado concurrente! 
//
public class ProcesadorYodafy {
	// Referencia a un socket para enviar/recibir las peticiones/respuestas
	private DatagramSocket socketUDP;
	
	// Para que la respuesta sea siempre diferente, usamos un generador de números aleatorios.
	private Random random;
	
	// Constructor que tiene como parámetro una referencia al socket abierto en por otra clase
	public ProcesadorYodafy(DatagramSocket socketServicio) {
		this.socketUDP=socketServicio;
		random=new Random();
	}
	
	
	// Aquí es donde se realiza el procesamiento realmente:
	void procesa(){
		byte[] buffer = new byte[256];
		DatagramPacket paquetePeticion;
		try {
			
			paquetePeticion = new DatagramPacket(buffer, buffer.length);

			socketUDP.receive(paquetePeticion);

			System.out.print("Datagrama recibido del host: " +
                           paquetePeticion.getAddress());

        	System.out.println(" desde el puerto remoto: " +
                           paquetePeticion.getPort());
			
			// Yoda hace su magia:
			// Creamos un String a partir de un array de bytes de tamaño "bytesRecibidos":
			// Yoda reinterpreta el mensaje:
			String peticion = new String(paquetePeticion.getData());
			peticion = yodaDo(peticion);

			byte[] respuestaStr = peticion.getBytes();

			DatagramPacket respuestaPkg = new DatagramPacket(respuestaStr, respuestaStr.length,
										paquetePeticion.getAddress(), paquetePeticion.getPort());

			socketUDP.send(respuestaPkg);
			
		} catch (SocketException e) {
      		System.out.println("Socket: " + e.getMessage());
		} catch (IOException e) {
			System.err.println("Error al obtener los flujo de entrada/salida.");
		}

	}

	// Yoda interpreta una frase y la devuelve en su "dialecto":
	private String yodaDo(String peticion) {
		// Desordenamos las palabras:
		String[] s = peticion.split(" ");
		String resultado="";
		
		for(int i=0;i<s.length;i++){
			int j=random.nextInt(s.length);
			int k=random.nextInt(s.length);
			String tmp=s[j];
			
			s[j]=s[k];
			s[k]=tmp;
		}
		
		resultado=s[0];
		for(int i=1;i<s.length;i++){
		  resultado+=" "+s[i];
		}
		
		return resultado;
	}
}
