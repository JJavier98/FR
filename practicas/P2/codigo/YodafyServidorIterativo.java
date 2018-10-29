import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;

//
// YodafyServidorIterativo
// (CC) jjramos, 2012
//
public class YodafyServidorIterativo {

	public static void main(String[] args) {
	
		// Puerto de escucha
		int port=8989;
		// array de bytes auxiliar para recibir o enviar datos.
		byte []buffer=new byte[256];
		// Número de bytes leídos
		int bytesLeidos=0;
		//Server Socket
		ServerSocket socketServidor;
		Socket socketServicio;
		PrintWriter outPrinter = new
			PrintWriter(socketServicio.getOutputStream(),true);

		
		try {
			// Abrimos el socket en modo pasivo, escuchando el en puerto indicado por "port"
			//////////////////////////////////////////////////
			// ...serverSocket=... (completar)
			//////////////////////////////////////////////////
			socketServidor = new ServerSocket(port);
			
			// Mientras ... siempre!
			do {
				
				// Aceptamos una nueva conexión con accept()
				/////////////////////////////////////////////////
				// socketServicio=... (completar)
				//////////////////////////////////////////////////Socket socketConexion = null;
				
				socketServicio = socketServidor.accept();
				
				// Creamos un objeto de la clase ProcesadorYodafy, pasándole como 
				// argumento el nuevo socket, para que realice el procesamiento
				// Este esquema permite que se puedan usar hebras más fácilmente.
				ProcesadorYodafy procesador=new ProcesadorYodafy(socketServicio);
				procesador.procesa();

				Socket socketConexion = null;

				try{
					socketConexion = socketServidor.accept();
				} catch(IOException e) {
					System.out.println("Error: no se pudo aceptar la conexion solicitada");
				}
				
			} while (true);
			
			}
			catch (IOException e) {
				System.err.println("Error al escuchar en el puerto "+port);
			}
	}

}
