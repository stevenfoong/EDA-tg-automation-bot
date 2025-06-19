package main

import (
	"aws-worker/internal/aws"
	"aws-worker/internal/rabbitmq"
	"encoding/json"
	"fmt"
	"log"
	"time"
)

type Task struct {
	Command      string `json:"command"`
	ServerName   string `json:"server_name"`
	InstanceID   string `json:"instance_id"`
	//InstanceID   string `json:"server_name"`
	Region       string `json:"region"`
	AWSAccountID string `json:"aws_account_id"`
	InstanceType string `json:"instance_type"`
	ChatID       int64  `json:"chat_id"`
	UserID       int64  `json:"user_id"`
	TaskID       string `json:"task_id"`
}

func main() {
	err := rabbitmq.Start()
	if err != nil {
		log.Fatalf("Failed to start RabbitMQ: %v", err)
	}

	rabbitmq.Consume(func(body []byte) {
		log.Printf("Raw task payload: %s\n", string(body))

		var task Task
		err := json.Unmarshal(body, &task)
		if err != nil {
			log.Printf("Failed to parse task: %v\n", err)
			return
		}

		log.Printf("Parsed task: %+v\n", task)

		err = aws.LoadCredentials(task.AWSAccountID, task.Region)
		if err != nil {
			log.Printf("Failed to load AWS credentials: %v\n", err)
			return
		}

		//err = aws.RebootInstance(task.InstanceName)
		//err = aws.RebootInstance(task.InstanceType, task.InstanceID)
	
		var instanceid string

		switch task.InstanceType {
		case "lightsail":
			instanceid = task.ServerName
		case "ec2":
			instanceid = task.InstanceID
		default:
			log.Printf("unsupported instance type: %s", task.InstanceType)
        	}
		
		//log.Printf("Before reboot ServerName : %s\n", task.ServerName)
                //err = aws.RebootInstance(task.InstanceType, task.ServerName)

		log.Printf("Before reboot ServerName : %s\n", instanceid)
		err = aws.RebootInstance(task.InstanceType, instanceid)
		if err != nil {
			log.Printf("Failed to reboot instance: %v\n", err)
			return
		}

		log.Printf("Reboot initiated, waiting 1 minute...")
		time.Sleep(60 * time.Second)

		//status, err := aws.GetInstanceState(task.InstanceName)
		status, err := aws.GetInstanceState(task.InstanceType, instanceid)
		if err != nil {
			log.Printf("Failed to get instance status: %v\n", err)
			return
		}

		var message string
		if status == "running" {
			message = fmt.Sprintf("✅ Reboot successful. Instance %s is now running.", task.ServerName)
			log.Printf("Published reboot success for %s", task.ServerName)
		} else {
			message = fmt.Sprintf("⚠️ Reboot attempted, but instance %s is not in 'running' state. Please check manually.", task.ServerName)
			log.Printf("Instance %s not running after reboot", task.ServerName)
		}

		outMsg := map[string]interface{}{
			"chat_id": task.ChatID,
			"user_id": task.UserID,
			"task_id": task.TaskID,
			"message": message,
		}
		b, _ := json.Marshal(outMsg)
		rabbitmq.Publish(b)

	})
}
