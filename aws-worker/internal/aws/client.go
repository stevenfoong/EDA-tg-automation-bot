package aws

import (
	"log"
	"context"
	"fmt"
	"os"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/credentials"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/lightsail"
	"github.com/joho/godotenv"
)

var (
	lightsailClient *lightsail.Client
	ec2Client       *ec2.Client
)

func LoadCredentials(accountID, region string) error {
	err := godotenv.Load(".env")
	if err != nil {
		return fmt.Errorf("error loading .env: %w", err)
	}

	keyID := os.Getenv(fmt.Sprintf("AWS_%s_ACCESS_KEY_ID", accountID))
	secret := os.Getenv(fmt.Sprintf("AWS_%s_SECRET_ACCESS_KEY", accountID))

	if keyID == "" || secret == "" || region == "" {
		return fmt.Errorf("credentials or region missing for account: %s", accountID)
	}

	cfg, err := config.LoadDefaultConfig(context.TODO(),
		config.WithRegion(region),
		config.WithCredentialsProvider(aws.NewCredentialsCache(
			credentials.NewStaticCredentialsProvider(keyID, secret, ""),
		)),
	)
	if err != nil {
		return fmt.Errorf("unable to load AWS config: %w", err)
	}

	lightsailClient = lightsail.NewFromConfig(cfg)
	ec2Client = ec2.NewFromConfig(cfg)
	log.Printf("Loading AWS config for account %s in region %s", accountID, region)
	return nil
}

func RebootInstance(instanceType, instanceID string) error {

	//log.Printf("AWS config : %s ", lightsailClient)
	log.Printf("Instance ID %s ", instanceID)

	switch instanceType {
	case "lightsail":
		//_, err := lightsailClient.RebootInstance(context.TODO(), &lightsail.RebootInstanceInput{
		//	InstanceName: &instanceID,
		//})

		_, err := lightsailClient.RebootInstance(context.TODO(), &lightsail.RebootInstanceInput{
                        InstanceName: aws.String(instanceID),
                })

		if err != nil {
			return fmt.Errorf("lightsail reboot error: %w", err)
		}
		return nil
	case "ec2":
		_, err := ec2Client.RebootInstances(context.TODO(), &ec2.RebootInstancesInput{
			InstanceIds: []string{instanceID},
		})

		if err != nil {
			return fmt.Errorf("ec2 reboot error: %w", err)
		}
		return nil
	default:
		return fmt.Errorf("unsupported instance type: %s", instanceType)
	}
}

func GetInstanceState(instanceType, instanceID string) (string, error) {
	switch instanceType {
	case "lightsail":
		res, err := lightsailClient.GetInstanceState(context.TODO(), &lightsail.GetInstanceStateInput{
			InstanceName: &instanceID,
		})
		if err != nil {
			return "", fmt.Errorf("lightsail status error: %w", err)
		}
		return aws.ToString(res.State.Name), nil
		//return string(res.State.Name), nil
	case "ec2":
		included := true
		res, err := ec2Client.DescribeInstanceStatus(context.TODO(), &ec2.DescribeInstanceStatusInput{
			InstanceIds:         []string{instanceID},
			IncludeAllInstances: &included,
		})
		if err != nil {
			return "", fmt.Errorf("ec2 status error: %w", err)
		}
		if len(res.InstanceStatuses) == 0 {
			return "", fmt.Errorf("ec2 instance status not found")
		}
		return string(res.InstanceStatuses[0].InstanceState.Name), nil
	default:
		return "", fmt.Errorf("unsupported instance type: %s", instanceType)
	}
}
