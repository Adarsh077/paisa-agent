# Paisa Agent 🤖💰

An intelligent AI agent system for the Paisa finance application, providing conversational interfaces for managing financial transactions through chat.

## 🌟 Overview

The Paisa Agent is a FastAPI-based service that acts as an intelligent intermediary between users and the Paisa financial management system. It processes natural language requests and converts them into structured financial operations using a sophisticated multi-stage pipeline.

### Key Features

- **Conversational Finance Management**: Natural language processing for financial transactions
- **Intelligent Planning**: AI-powered request analysis and execution planning
- **MCP Integration**: Seamless integration with Model Context Protocol tools
- **Docker Ready**: Containerized deployment for easy scaling

## 🏗️ Architecture

The agent follows a modular pipeline architecture:

```
User Input → Preprocessor → Planner → Executor → Viewer → Response
```

### Core Components

- **Preprocessor**: Cleans and normalizes user input
- **Planner**: Analyzes requests and creates execution plans
- **Executors**: 
  - Chat Executor: Handles web-based conversations
  - SMS Executor: Processes SMS-based requests
- **Viewer**: Formats responses for different output channels
- **MCP Client**: Manages connections to external MCP tools

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Docker (optional)
- Access to Paisa MCP server

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Adarsh077/paisa-agent.git
   cd paisa-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the service**
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8002
   ```

### Docker Deployment

```bash
# Build and run using the provided script
chmod +x bin/run.sh
./bin/run.sh
```

Or manually:

```bash
docker build -t paisa-agent .
docker run --name paisa-agent \
  --add-host=host.docker.internal:host-gateway \
  --env-file .env \
  -p 8002:8002 \
  -d paisa-agent
```

## 📡 API Endpoints

### Chat Interface
```http
POST /chat
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "Add an expense of $50 for groceries today"
    }
  ]
}
```

### SMS Interface
```http
POST /sms
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "messages": [
    {
      "role": "user", 
      "content": "Show my expenses this month"
    }
  ]
}
```

## 🏢 Paisa Ecosystem

The Paisa Agent is part of a comprehensive financial management ecosystem:

### Related Repositories

| Repository | Description | Technology Stack | Status |
|------------|-------------|------------------|---------|
| **[paisa-app](https://github.com/Adarsh077/paisa-app)** 📱 | Flutter mobile application | Flutter, Dart | Active |
| **[paisa-api](https://github.com/Adarsh077/paisa-api)** 🌐 | Backend API server | Node.js, MongoDB, Express | Active |
| **[paisa-agent](https://github.com/Adarsh077/paisa-agent)** 🤖 | AI agent service (this repo) | Python, FastAPI, LLamaIndex | Active |
| **[paisa-mcp](https://github.com/Adarsh077/paisa-mcp)** 🔧 | MCP server with financial tools | Python, MCP Protocol | Active |

## 🛠️ Development

### Project Structure

```
src/
├── agents.py              # Main agent logic (chat & SMS)
├── main.py               # FastAPI application entry point
├── config.py             # Configuration management
├── executors/            # Request execution handlers
│   ├── chat_executor.py
│   └── sms_executor.py
├── planner/              # AI planning logic
├── preprocessor/         # Input preprocessing
├── selector/             # Tool selection logic
├── tools/                # MCP client and tool management
└── viewer/               # Response formatting
```

### Environment Variables

```bash
# MCP Server Configuration
MCP_API_URL=http://localhost:8001

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Logging
LOG_LEVEL=INFO
```
