import pika

# Conexión al servidor RabbitMQ en localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Asegurarse de que la cola existe
channel.queue_declare(queue='hello')

# Función que se llama cada vez que se recibe un mensaje
def callback(ch, method, properties, body):
    print(f" [x] Recibido: {body.decode()}")

# Asociar la función a la cola
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Esperando mensajes. Para salir presiona CTRL+C')
channel.start_consuming()
