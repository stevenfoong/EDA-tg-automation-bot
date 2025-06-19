package rabbitmq

import (
	"log"
	"os"
	"github.com/streadway/amqp"
)

var (
	rabbitHost  = os.Getenv("RABBITMQ_HOST")
	rabbitUser  = os.Getenv("RABBITMQ_USER")
	rabbitPass  = os.Getenv("RABBITMQ_PASS")

	channel     *amqp.Channel
)

const (
	AWSWorkerQueue = "aws_worker_queue"
	OutputQueue    = "output_tg_queue"
)

func Start() error {
	conn, err := amqp.Dial("amqp://" + rabbitUser + ":" + rabbitPass + "@" + rabbitHost + ":5672/")
	if err != nil {
		return err
	}

	channel, err = conn.Channel()
	if err != nil {
		return err
	}

	_, err = channel.QueueDeclare(AWSWorkerQueue, true, false, false, false, nil)
	if err != nil {
		return err
	}

	_, err = channel.QueueDeclare(OutputQueue, true, false, false, false, nil)
	if err != nil {
		return err
	}

	return nil
}

func Consume(handler func([]byte)) {
	msgs, err := channel.Consume(AWSWorkerQueue, "", true, false, false, false, nil)
	if err != nil {
		log.Fatal(err)
	}

	log.Println(" [*] Waiting for messages...")
	for msg := range msgs {
		log.Printf("Received message: %s", string(msg.Body))
		handler(msg.Body)
	}
}

func Publish(msg []byte) {
	if channel == nil {
		log.Println("RabbitMQ channel not initialized")
		return
	}
	_ = channel.Publish("", OutputQueue, false, false, amqp.Publishing{
		ContentType: "application/json",
		Body:        msg,
	})
}


