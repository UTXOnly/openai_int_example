
# OpenAI and Datadog Integration

This example creates a Python application using OpenAI's GPT-4 model alongside Datadog for monitoring. It collects metrics, traces, and logs. The application runs in Docker containers managed by Docker Compose. For account usage metrics, use [Datadog's OpenAI integration](https://app.datadoghq.com/integrations/openai?search=openai).


## Prerequisites

Before you begin, ensure you have the following installed:
- Docker
- Docker Compose

## Setup

1. **Clone the Repository**
   ```sh
   git clone https://github.com/UTXOnly/openai_int_example.git
   cd openai_int_example
   ```

2. **Create a `.env` File**
   Create a `.env` file in the root directory of the project and add the following environment variables:
   ```env
   DATADOG_API_KEY=your_datadog_api_key
   OPENAI_API_KEY=your_actual_openai_api_key
   ```

3. **Build and Run the Containers**
   Use Docker Compose to build and run the containers:
   ```sh
   docker-compose up --build
   ```


## Configuration

- **OpenAI API Key**: Make sure to set your OpenAI API key in the `.env` file.
- **Datadog API Key**: Make sure to set your Datadog API key in the `.env` file.

## Usage

The application sends a prompt to OpenAI's GPT-4 model and logs the response. It also sends metrics to Datadog for monitoring.

### Viewing Logs

Application logs are stored in the `logs/` directory. You can view them using the following command:
```sh
tail -f logs/app.log
```

### Checking Environment Variables in Containers

To ensure environment variables are set correctly, you can check them inside the running container:
```sh
docker exec -it <container_name> bash
echo $DATADOG_API_KEY
echo $OPENAI_API_KEY
```

Replace `<container_name>` with the name of your container.

## Troubleshooting

- **API Key Errors**: Ensure that the API keys in the `.env` file are correct and have the necessary permissions.
- **Connection Issues**: Verify that the Datadog agent and the application can communicate by checking the logs and network settings.


