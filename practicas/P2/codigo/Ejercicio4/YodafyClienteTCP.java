//
// YodafyServidorIterativo
// (CC) jjramos, 2012
//
import java.io.*;
import java.net.*;

public class YodafyClienteTCP {

	public static void main(String[] args) {
		
		try {
			DatagramSocket socketUDP = new DatagramSocket();
			String msj = new String("Al monte del volcán debes ir sin demora");
			byte[] mensaje = msj.getBytes();
			String host="localhost";
			InetAddress direccion = InetAddress.getByName(host);
			int port=8989;


			DatagramPacket paquete = new DatagramPacket(mensaje, mensaje.length, direccion, port);

			socketUDP.send(paquete);

			byte[] buffer = new byte[1000];
			DatagramPacket respuesta = new DatagramPacket(buffer, buffer.length);
			socketUDP.receive(respuesta);

			
			System.out.println("Recibido: ");
			System.out.println(new String(respuesta.getData()));
			
			socketUDP.close();

			// Excepciones:
		} catch (UnknownHostException e) {
			System.err.println("Error: Nombre de host no encontrado.");
		} catch (IOException e) {
			System.err.println("Error de entrada/salida al abrir el socket.");
		}
	}
}
