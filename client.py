import openai
import logging
import os
from ddtrace import tracer
from datadog import statsd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set tracer to Datadog agent host
tracer.configure(hostname=os.getenv('DD_AGENT_HOST', 'localhost'), port=8126)

# Configure DogStatsD client
statsd_host = os.getenv('DD_AGENT_HOST', 'localhost')
statsd_port = 8125
statsd.initialize(statsd_host, statsd_port)

def get_openai_response(prompt):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=50
        )
        logger.info("OpenAI API response received successfully.")
        statsd.increment('openai.api.success', tags=["status:success"])
        return response
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        statsd.increment('openai.api.error', tags=["status:error", f"error:{type(e).__name__}"])
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        statsd.increment('openai.api.error', tags=["status:error", "error:UnexpectedError"])
        return None

def process_response(response):
    try:
        processed_text = response.choices[0].text.strip()
        logger.info(f"Processed response: {processed_text}")
        return processed_text
    except Exception as e:
        logger.error(f"Error processing response: {e}")
        statsd.increment('openai.api.processing_error', tags=["status:error", "error:ProcessingError"])
        return None

def main():
    prompt = "Once upon a time"
    response = get_openai_response(prompt)
    if response:
        processed_text = process_response(response)
        if processed_text:
            print(processed_text)
        else:
            logger.error("Failed to process the response.")
    else:
        logger.error("Failed to get a valid response from OpenAI API.")

if __name__ == "__main__":
    main()
