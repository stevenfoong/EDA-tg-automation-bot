docker compose -f docker-compose.yml down
#docker rmi automation-bot-output-telegram-bot
docker rmi automation-bot-input-telegram-bot
#docker rmi automation-bot-bash-worker
docker rmi automation-bot-aws-worker
#docker compose -f docker-compose.yml build --no-cache
docker compose -f docker-compose.yml up -d
