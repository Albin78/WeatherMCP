# WeatherMCP 🌤️

A high-performance weather service built with **Model Context Protocol (MCP)** and **Server-Sent Events (SSE)**. Provides real-time weather forecasts and alerts through an async, scalable architecture.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-1.12.4+-green.svg)](https://modelcontextprotocol.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

## ✨ Features

- 🌤️ **Real-time weather forecasts** via National Weather Service (NWS) API
- 🔄 **Async SSE transport** for multiple concurrent clients
- 🐳 **Docker containerization** for easy deployment
- 🚀 **Built with FastMCP** and Python async/await
- 📍 **Support for multiple US locations**
- 🔌 **Extensible MCP tool architecture**
- 📊 **Weather alerts and forecasts**
- 🌍 **Multi-client support**

## 🏗️ Architecture

```
┌─────────────┐    HTTP/JSON    ┌─────────────┐    MCP Protocol    ┌─────────────┐
│   NWS API   │ ──────────────→ │   Server    │ ─────────────────→ │   Client    │
│ (Weather)   │                 │ (server.py) │                     │(client-sse)│
└─────────────┘                 └─────────────┘                     └─────────────┘
                                       │
                                       ▼
                                ┌─────────────┐
                                │   Docker    │
                                │ Container   │
                                └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- UV package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/WeatherMCP.git
   cd WeatherMCP
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the server**
   ```bash
   uv run mcpserver/server.py
   ```

4. **Test with client**
   ```bash
   uv run mcpserver/client-sse.py
   ```

### Docker Deployment

```bash
# Build the container
docker build -t weather-mcp mcpserver

# Run the container
docker run -p 8000:8000 weather-mcp
```

## 📁 Project Structure

```
WeatherMCP/
├── mcpserver/
│   ├── server.py          # MCP weather server
│   ├── client-sse.py      # SSE client
│   ├── client-stdio.py    # stdio client
│   ├── Dockerfile         # Docker configuration
│   └── requirements.txt   # Python dependencies
├── client_forecast.py     # Multi-city forecast demo
├── test_server.py         # Server testing script
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## 🔧 Available Tools

### `get_forecast(latitude, longitude)`
Get detailed weather forecast for specific coordinates.

**Example:**
```python
result = await session.call_tool("get_forecast", arguments={
    "latitude": 37.7749, 
    "longitude": -122.4194
})
```

### `get_result(state)`
Get weather alerts for a US state.

**Example:**
```python
result = await session.call_tool("get_result", arguments={
    "state": "CA"
})
```

## 🌐 API Endpoints

- **SSE Transport**: `http://localhost:8000/sse`
- **Port**: 8000 (configurable)
- **Protocol**: MCP over Server-Sent Events

## 🧪 Testing

### Test Server Connection
```bash
uv run test_server.py
```

### Multi-Client Demo
```bash
uv run client_forecast.py
```

### Monitor Server Health
```bash
uv run client_monitor.py
```

## 🔌 Transport Methods

### Server-Sent Events (SSE)
- **Use case**: Network-based communication
- **Port**: 8000
- **Client**: `client-sse.py`

### Standard I/O (stdio)
- **Use case**: Local process communication
- **Port**: None required
- **Client**: `client-stdio.py`

## 🐳 Docker Support

The project includes a complete Docker setup:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install uv
COPY requirements.txt .
RUN uv pip install -r requirements.txt
COPY server.py .
EXPOSE 8000
CMD ["uv", "run", "server.py"]
```

## 📊 Performance Features

- **Async/await**: Non-blocking I/O operations
- **Concurrent clients**: Handle multiple connections simultaneously
- **Connection pooling**: Efficient HTTP client management
- **Error handling**: Graceful fallbacks and timeouts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io) for the communication framework
- [National Weather Service](https://weather.gov) for weather data
- [FastMCP](https://github.com/jlowin/fastmcp) for the server framework
