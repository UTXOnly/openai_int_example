import os
import logging
import time
from openai import OpenAI
from ddtrace import tracer
from datadog.dogstatsd import DogStatsd

log_directory = "/app/logs"
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(log_directory, "app.log")
logging.basicConfig(
    level=logging.INFO,
    filename=log_file,
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Set tracer to Datadog agent host
tracer.configure(hostname=os.getenv("DD_AGENT_HOST", "localhost"), port=8126)

# Configure DogStatsD client
statsd_host = os.getenv("DD_AGENT_HOST")
statsd_port = 8125
statsd = DogStatsd(host=statsd_host, port=statsd_port)

def get_openai_response(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}], model="gpt-4"
        )
        logger.info("OpenAI API response received successfully.")
        return chat_completion
    except Exception as e:
        logger.error(f"Error interacting with OpenAI API: {e}")
        statsd.increment(
            "openai.api.error", tags=["status:error", f"error:{type(e).__name__}"]
        )
        return None

def process_response(response):
    try:
        processed_text = response.choices[0].message.content.strip()
        logger.info(f"Processed response: {processed_text}")
        return processed_text
    except Exception as e:
        logger.error(f"Error processing response: {e}")
        return None

def main():
    while True:
        prompt = "Tell me about this: https://platform.openai.com/docs/api-reference/batch/create?lang=python, provide python API call examples"
        response = get_openai_response(prompt)
        if response:
            processed_text = process_response(response)
            if processed_text:
                logger.info(processed_text)
            else:
                logger.error("Failed to process the response.")
        else:
            logger.error("Failed to get a valid response from OpenAI API.")
        time.sleep(10)

if __name__ == "__main__":
    main()
