import asyncio
from services.rabbitmq_consumer import consume_tasks
from services.task_executor import handle_task

async def main():
    await consume_tasks(handle_task)

if __name__ == "__main__":
    asyncio.run(main())

