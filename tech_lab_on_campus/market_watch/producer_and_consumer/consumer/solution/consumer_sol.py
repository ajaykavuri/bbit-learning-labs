import pika
import os

class mqConsumer(mqConsumerInterface):
    def __init__(self, binding_key: str, exchange_name: str, queue_name: str):
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.setupRMQConnection()
        self.channel = None
        self.exchange = None
        self.connection = None

    def setupRMQConnection(self) -> None:
        if not self.channel:
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue={self.queue_name})
        if not self.exchange:
            self.exchange = self.channel.exchange_declare(exchange="Exchange Name")
            
        self.channel.queue_bind(
                queue= self.queue_name,
                routing_key= self.binding_key,
                exchange= self.exchange_name,
            )
        
        self.channel.basic_consume(
            self.queue_name, self.on_message_callback(), auto_ack=False
        )

     def on_message_callback(
        self, channel, method_frame, header_frame, body
    ) -> None:
        
        channel.basic_ack(method_frame.delivery_tag, False)
        
        print(header_frame + " " + body)

        
    def startConsuming(self) -> None:
        print("[*] Waiting for messages. To exit press CTRL+C")
        

        self.channel.start_consuming
        
    
    def __del__(self) -> None:
        # Print "Closing RMQ connection on destruction"
        
        # Close Channel

        # Close Connection
        self.connection.close()
        self.channel.close()
        pass