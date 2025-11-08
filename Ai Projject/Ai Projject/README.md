# Healthcare RAG Assistant

A backend service for a RAG-powered healthcare knowledge assistant that helps clinicians retrieve medical guidelines and research summaries in both English and Japanese.

## Features

✅ **Bilingual Support**: English and Japanese document ingestion and retrieval  
✅ **FAISS Vector Database**: Fast semantic similarity search using embeddings  
✅ **Multi-language Processing**: Automatic language detection and translation  
✅ **Mock LLM Generation**: Combine retrieved documents with LLM responses  
✅ **API Key Authentication**: Secure endpoints with X-API-Key header  
✅ **RESTful API**: Clean, documented endpoints with OpenAPI/Swagger support  
✅ **Modular Architecture**: Separation of concerns with services, routers, and utilities  
✅ **Docker Deployment**: Production-ready Docker and docker-compose setup  
✅ **GitHub Actions CI/CD**: Automated testing and deployment pipeline  

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- 2GB RAM minimum, 4GB+ recommended

### Run with Docker

\`\`\`bash
# Clone the repository
git clone <repository-url>
cd healthcare-rag-assistant

# Build and start the service
docker-compose up --build

# Service will be available at http://localhost:8000
# API Documentation: http://localhost:8000/docs
\`\`\`

### Run Locally (Development)

\`\`\`bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export API_KEY=your-secret-key

# Run application
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

## API Endpoints

### Health Check
\`\`\`bash
GET /health
\`\`\`
Returns service status and FAISS index statistics.

### Document Ingestion
\`\`\`bash
POST /ingest
X-API-Key: your-api-key
Content-Type: application/json

{
  "filename": "diabetes_guidelines.txt",
  "content": "Type 2 diabetes management recommendations...",
  "language": "en"  # Optional, auto-detected
}
\`\`\`

### Document Retrieval
\`\`\`bash
POST /retrieve
X-API-Key: your-api-key
Content-Type: application/json

{
  "query": "What are the latest recommendations for Type 2 diabetes management?",
  "language": "en",  # Optional, auto-detected
  "top_k": 3
}
\`\`\`

### Generate Response
\`\`\`bash
POST /generate
X-API-Key: your-api-key
Content-Type: application/json

{
  "query": "What are the latest recommendations for Type 2 diabetes management?",
  "language": "en",
  "output_language": "ja",  # Optional, defaults to query language
  "include_sources": true
}
\`\`\`

## Example Usage

### Python Client

\`\`\`python
import requests

BASE_URL = "http://localhost:8000"
API_KEY = "ai-secret-key"
HEADERS = {"X-API-Key": API_KEY}

# 1. Ingest a medical document
ingest_payload = {
    "filename": "type2_diabetes.txt",
    "content": """Type 2 Diabetes Management:
    Recent guidelines recommend...
    1. Lifestyle modifications
    2. Pharmacological interventions
    ...""",
    "language": "en"
}

response = requests.post(
    f"{BASE_URL}/ingest",
    json=ingest_payload,
    headers=HEADERS
)
print(response.json())

# 2. Retrieve relevant documents
retrieve_payload = {
    "query": "What are the latest recommendations for diabetes management?",
    "language": "en",
    "top_k": 3
}

response = requests.post(
    f"{BASE_URL}/retrieve",
    json=retrieve_payload,
    headers=HEADERS
)
print(response.json())

# 3. Generate a response
generate_payload = {
    "query": "What are the latest recommendations for diabetes management?",
    "language": "en",
    "output_language": "ja",
    "include_sources": True
}

response = requests.post(
    f"{BASE_URL}/generate",
    json=generate_payload,
    headers=HEADERS
)
print(response.json())
\`\`\`

### cURL Examples

\`\`\`bash
# Set API key
export API_KEY="T1-ai-secret-key-2025"

# Ingest document
curl -X POST http://localhost:8000/ingest \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "diabetes.txt",
    "content": "Type 2 diabetes management guidelines...",
    "language": "en"
  }'

# Retrieve documents
curl -X POST http://localhost:8000/retrieve \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "diabetes management",
    "top_k": 3
  }'

# Generate response
curl -X POST http://localhost:8000/generate \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "diabetes management",
    "output_language": "ja"
  }'
\`\`\`

## Architecture

### Project Structure
\`\`\`
healthcare-rag-assistant/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── models.py               # Pydantic request/response models
│   ├── middleware.py           # Custom middleware (auth, logging)
│   ├── routers/
│   │   ├── ingest.py          # Document ingestion endpoints
│   │   ├── retrieve.py        # Document retrieval endpoints
│   │   └── generate.py        # LLM response generation
│   ├── services/
│   │   ├── faiss_service.py   # FAISS vector DB management
│   │   ├── language_detector.py # Language detection
│   │   ├── translator.py       # Bilingual translation
│   │   └── llm_service.py      # Mock LLM responses
│   └── utils/
│       └── helpers.py          # Utility functions
├── data/
│   ├── faiss_index/            # Persisted FAISS indices
│   └── documents/              # Uploaded documents
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
\`\`\`

### Core Components

#### FAISS Service
- Manages vector embeddings using `sentence-transformers`
- Handles document ingestion with automatic chunking
- Performs semantic similarity search
- Persists index to disk for recovery

#### Language Detection & Translation
- Automatic language detection using `langdetect`
- Bilingual support: English ↔ Japanese
- Uses Helsinki-NLP models for translation
- Fallback to original if translation fails

#### Mock LLM Service
- Generates contextual medical responses
- Routes to appropriate medical guidelines based on query
- Integrates with retrieved documents
- Supports both English and Japanese output

## Design Notes: Scalability & Future Improvements

### Current Architecture

The system is built with modularity and scalability in mind. Each component (FAISS service, language detection, translation, LLM generation) is independently testable and replaceable. The API key authentication provides basic security, and the modular router structure allows easy endpoint extension.

### Scalability Considerations

1. **Vector Database**: Currently uses FAISS with in-memory index saved to disk. For production scale (millions of documents), consider:
   - Milvus or Pinecone for distributed vector search
   - Sharding documents across multiple FAISS indices
   - Redis caching for frequent queries

2. **LLM Integration**: Replace mock LLM with real models:
   - OpenAI API for production-grade responses
   - LLaMA for on-premise deployments
   - Fine-tuned models for medical domain

3. **Deployment**: Scale horizontally with:
   - Kubernetes orchestration for auto-scaling
   - Load balancing across multiple replicas
   - Shared persistent storage (S3, GCS) for FAISS indices

4. **Performance**: Optimize with:
   - Caching layer (Redis) for frequent queries
   - Async processing for long-running ingestions
   - Database indexing for metadata lookups

### Future Improvements

1. **Enhanced Security**:
   - OAuth2/JWT authentication
   - Role-based access control (RBAC)
   - Request rate limiting
   - Audit logging

2. **Better LLM Integration**:
   - Real LLM API integration (OpenAI, Anthropic)
   - Few-shot prompting with domain-specific examples
   - Streaming responses for large outputs
   - Response quality metrics and evaluation

3. **Advanced Retrieval**:
   - Multi-modal search (text + images)
   - Hybrid search (keyword + semantic)
   - Re-ranking for improved relevance
   - Document metadata filtering

4. **Monitoring & Observability**:
   - Prometheus metrics for API performance
   - ELK stack for centralized logging
   - Distributed tracing with Jaeger
   - Dashboard for system health

5. **Testing & Quality**:
   - Unit tests for all services
   - Integration tests for API endpoints
   - Load testing with locust
   - Continuous integration with GitHub Actions

6. **Documentation**:
   - OpenAPI/Swagger spec (auto-generated)
   - Architecture decision records (ADRs)
   - Deployment guides for different platforms
   - Medical content guidelines for ingestion

## Environment Variables

\`\`\`bash
# API Configuration
API_KEY=your-secret-key-here
HOST=0.0.0.0
PORT=8000
DEBUG=False
\`\`\`

## Security

- **API Key Authentication**: All endpoints protected with X-API-Key header
- **Input Validation**: Pydantic models validate all requests
- **Non-root User**: Docker container runs as unprivileged user
- **HTTPS Ready**: Production deployment should use reverse proxy with TLS

## Performance Notes

- Initial startup may take 1-2 minutes (downloading embedding models)
- First query is slower due to model loading
- Subsequent queries are fast (~100-500ms)
- FAISS is optimized for CPU-based similarity search
- Consider GPU for production deployments

## Troubleshooting

### FAISS Index Not Loading
\`\`\`bash
# Clear index and restart
docker-compose down
rm -rf data/faiss_index/
docker-compose up --build
\`\`\`

### Translation Models Not Available
\`\`\`bash
# Models download automatically on first use
# Check internet connectivity and disk space (2GB+ required)
\`\`\`

### Memory Issues
\`\`\`bash
# Increase Docker memory limit in docker-compose.yml
# Reduce chunk size in app/config.py
# Use FAISS GPU version for large indices
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


