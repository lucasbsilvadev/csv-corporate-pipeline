# 📊 CSV Processing Corporate Pipeline

**Enterprise-grade data processing pipeline with Java, Python, and full CI/CD**

[![Corporate Pipeline](https://img.shields.io/badge/status-production_ready-success)](https://github.com/yourusername/csv-corporate-pipeline)
[![Java](https://img.shields.io/badge/Java-21-blue)](https://openjdk.org/)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://python.org)
[![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.2-brightgreen)](https://spring.io)

## 🏗 Architecture

```mermaid
graph TB
    A[Client Request] --> B[Java REST API]
    B --> C[Python Worker]
    C --> D[CSV Processing]
    D --> E[Output CSV]
    B --> F[Health Check]
    C --> G[Structured Logs]
    
    H[GitHub Actions] --> I[Build & Test]
    I --> J[Docker Build]
    J --> K[Deploy Simulation]

    Try it yourself:

# 1. Clone repository
git clone https://github.com/bsilvalucasdev/csv-corporate-pipeline.git

# 2. Start with Docker Compose
docker-compose up -d

# 3. Access API
curl http://localhost:8080/api/v1/health