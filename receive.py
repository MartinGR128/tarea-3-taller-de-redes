import pika

def callback(ch, method, properties, body):
    print(f" [x] Mensaje recibido: {body.decode()}")

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*Esperando mensajes. Para salir presione CTRL+C')
channel.start_consuming()
