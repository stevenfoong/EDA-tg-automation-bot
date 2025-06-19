import json
import inspect

from services.rabbitmq_publisher import publish_to_rabbitmq
from tasks import common, network, system, diag

TASK_MAP = {
    "ping": network.ping_host,
    "disk_usage": system.check_disk_usage,
    "say_hello": common.say_hello,
    "lookup_ip_location": network.lookup_ip_location,
    "diagnostic_cloud_proxy": diag.diag_cloud_proxy,
}

async def handle_task(payload):
    try:
        task = json.loads(payload)
        task_name = task.get("task")
#        params = task.get("params", {})

        if task_name not in TASK_MAP:
            print(f"Unknown task: {task_name}")
            return

        func = TASK_MAP[task_name]

        # Extract correct parameters, whether from "params" or top-level
        sig = inspect.signature(func)
        raw_params = task.get("params")
        if raw_params:
            accepted_params = {k: v for k, v in raw_params.items() if k in sig.parameters}
        else:
            accepted_params = {k: v for k, v in task.items() if k in sig.parameters}

        # Filter only accepted params
        #sig = inspect.signature(func)
        #accepted_params = {k: v for k, v in params.items() if k in sig.parameters}

        # Execute the task function and collect result
        result = await func(**accepted_params)

        #params = task.get("params")
        #if not params:
            # fallback: use the task itself (except 'task')
            #params = {k: v for k, v in task.items() if k != "task"}

        #await func(**params)

        # Format message based on task name and result
        message_text = ""

        if task_name == "diagnostic_cloud_proxy":
            if result.get("success"):
                message_text = (
                    f"✅ Proxy test passed for {result['server']} ({result['proxy_ip']})\n"
                    f"→ Public IP: {result['public_ip']}\n"
                    f"→ Country (ip-api): {result['country_ipapi']}\n"
                    f"→ Country (ipinfo): {result['country_ipinfo']}"
                )
            else:
                message_text = (
                    f"❌ Proxy test FAILED for {result['server']} ({result['proxy_ip']})\n"
                    f"Reason: {result['error']}"
                )

        # Default fallback message
        if not message_text:
            message_text = f"✅ Task '{task_name}' completed successfully."

        # Send message to RabbitMQ
        response = {
            "chat_id": task.get("chat_id"),
            "user_id": task.get("user_id"),
            "diagnostic_id": task.get("diagnostic_id"),
            "message": message_text
        }
        await publish_to_rabbitmq(response)

    except Exception as e:
        print(f"Error handling task: {e}")

