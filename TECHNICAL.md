# UniHelp Enterprise - Technical Documentation

## Architecture Overview

### Technology Stack

- **Frontend**: Streamlit 1.31+
- **Backend**: Python 3.10+
- **LLM Provider**: Groq (llama-3.1-8b-instant, llama-3.3-70b-versatile)
- **PDF Generation**: ReportLab 4.0+
- **Configuration**: python-dotenv

### System Architecture

```
┌─────────────────┐
│   Browser UI    │
│   (Streamlit)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Application    │
│   Layer (app.py)│
├─────────────────┤
│ • Rate Limiting    │
│ • Input Validation │
│ • Caching          │
│ • Analytics        │
└────────┬────────┘
         │
         ├──────────► Groq API (LLM)
         ├──────────► Local Storage (JSON)
         └──────────► Documents (RAG source)
```

## Core Components

### 1. Infrastructure Layer

**Rate Limiting** (`rate_limit` decorator)
- Window-based request limiting
- Per-session tracking
- Configurable thresholds

**Caching** (`SimpleCache` class)
- TTL-based expiration
- In-memory storage
- Hash-based keys

**Retry Logic** (`retry_on_error` decorator)
- Exponential backoff
- Configurable attempts
- Error logging

**Analytics** (`track_analytics` function)
- Event tracking
- Session attribution
- JSON persistence

### 2. Security Layer

**Input Sanitization** (`sanitize_input`)
```python
# HTML escape
# Pattern filtering
# Length validation
```

**Session Management**
```python
# Unique session IDs (SHA256)
# Timeout detection
# Activity tracking
```

**Validation** (`validate_question`)
```python
# Length checks
# Spam detection
# Pattern analysis
```

### 3. Business Logic Layer

**RAG Question Answering** (`ask_rag_question`)
- Document context injection
- Strict answer constraints
- Fallback messaging

**Email Generation** (`generate_administrative_email`)
- Template-based generation
- Context-aware content
- Professional formatting

**Multi-format Export**
- PDF (`generate_email_pdf`)
- Markdown (`generate_email_markdown`)
- HTML (`generate_email_html`)
- Plain Text (`generate_email_text`)

### 4. Presentation Layer

**Multi-language Support**
- French/English toggle
- Dynamic text rendering
- Localized error messages

**Session State Management**
```python
st.session_state = {
    "session_id": str,
    "language": str,
    "chat_history": list,
    "email_history": list,
    "current_email": str | None,
    "dark_mode": bool,
    "last_activity": datetime
}
```

## Data Flow

### Question Answering Flow

```
1. User Input → Validation → Sanitization
                    ↓
2. Rate Limit Check
                    ↓
3. Cache Lookup (cache hit? → return)
                    ↓
4. Document Loading (cached)
                    ↓
5. Prompt Construction
                    ↓
6. Groq API Call (with retry)
                    ↓
7. Response Processing
                    ↓
8. Cache Storage
                    ↓
9. History Persistence
                    ↓
10. Analytics Tracking
                    ↓
11. UI Display
```

### Email Generation Flow

```
1. Type Selection → Validation
                    ↓
2. Rate Limit Check
                    ↓
3. Context Loading
                    ↓
4. Prompt Construction
                    ↓
5. Groq API Call (with retry)
                    ↓
6. Response Processing
                    ↓
7. History Persistence
                    ↓
8. Multi-format Export Options
                    ↓
9. Analytics Tracking
```

## Configuration Management

### Environment Variables

```env
# Required
GROQ_API_KEY=<your_api_key>

# Optional
GROQ_MODEL=llama-3.1-8b-instant
```

### Application Config (`APP_CONFIG`)

```python
{
    "MODEL_CANDIDATES": [...],
    "QA_TEMPERATURE": 0.2,
    "EMAIL_TEMPERATURE": 0.3,
    "MAX_QUESTION_LENGTH": 500,
    "MAX_HISTORY_ITEMS": 100,
    "CACHE_TTL_SECONDS": 3600,
    "RATE_LIMIT_REQUESTS": 10,
    "RATE_LIMIT_WINDOW_SECONDS": 60,
    "SESSION_TIMEOUT_MINUTES": 30,
    "MAX_RETRIES": 3,
    "RETRY_DELAY_SECONDS": 2,
}
```

## Performance Optimization

### Caching Strategy

1. **Document Caching**: `@st.cache_data` on document loading
2. **Query Caching**: SimpleCache with TTL for repeated questions
3. **Model Response Caching**: Expensive LLM calls cached

### Rate Limiting Strategy

- **Per-session tracking**: Prevents single-user abuse
- **Sliding window**: 10 requests per 60 seconds (default)
- **Graceful degradation**: Warning message instead of hard error

### Database Schema (JSON Files)

**Chat History** (`.unihelp_chat_history.json`)
```json
[
  {
    "timestamp": "2026-02-27T12:34:56",
    "question": "...",
    "answer": "..."
  }
]
```

**Analytics** (`.unihelp_analytics.json`)
```json
[
  {
    "timestamp": "2026-02-27T12:34:56",
    "event": "question_asked",
    "data": {...},
    "session_id": "abc123"
  }
]
```

## Error Handling

### Retry Strategy

```python
@retry_on_error(max_retries=3, delay=2.0)
def api_call():
    # Exponential backoff: 2s, 4s, 8s
    pass
```

### Fallback Models

```python
for model in ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]:
    try:
        return groq_api_call(model)
    except Exception:
        continue  # Try next model
```

### Logging Hierarchy

```
INFO: Normal operations
WARNING: Rate limits, retries
ERROR: Failed operations
DEBUG: Cache hits, detailed traces
```

## Security Considerations

### Input Validation
- Max length enforcement
- HTML escape
- Special character filtering
- Spam pattern detection

### Session Security
- Unique session IDs (SHA256)
- Timeout after inactivity
- No sensitive data in logs

### API Security
- Key stored in environment variables
- Rate limiting prevents abuse
- Retry backoff prevents hammering

## Scalability

### Current Limitations
- In-memory caching (single instance)
- JSON file storage (not concurrent-safe)
- No horizontal scaling support

### Future Enhancements
- Redis for distributed caching
- PostgreSQL for persistent storage
- Load balancer support
- Multi-tenant isolation

## Monitoring & Observability

### Metrics Tracked
- Questions asked (count, rate)
- Emails generated (by type)
- API errors (by model)
- Cache hit rate
- Session duration
- Rate limit triggers

### Log Analysis

```bash
# View recent errors
grep ERROR unihelp.log

# Track API usage
grep "Groq API" unihelp.log

# Monitor rate limits
grep "Rate limit" unihelp.log
```

## Development Guidelines

### Code Style
- PEP 8 compliant
- Type hints required
- Docstrings for all functions
- Max line length: 127

### Testing Strategy
```bash
# Syntax check
python -m py_compile app.py

# Security scan
bandit -r app.py

# Linting
flake8 app.py
```

### Git Workflow
1. Feature branches (`feature/xyz`)
2. Pull requests for review
3. CI/CD automatic checks
4. Main branch protected

## Deployment

### Docker Deployment
```bash
docker build -t unihelp:latest .
docker run -p 8501:8501 --env-file .env unihelp:latest
```

### Cloud Platforms

**Streamlit Cloud**
- Direct GitHub integration
- Free tier available
- Automatic SSL

**AWS ECS**
- Fargate serverless option
- Auto-scaling support
- Load balancer integration

**Google Cloud Run**
- Containerized deployment
- Pay-per-request pricing
- Global CDN

## API Reference

### Core Functions

#### `ask_rag_question(client, documents_context, user_question, lang) -> str`
RAG-based question answering.

**Parameters:**
- `client`: Groq client instance
- `documents_context`: Official document content
- `user_question`: User's sanitized question
- `lang`: Language code ("FR"/"EN")

**Returns:** Answer string or fallback message

#### `generate_administrative_email(client, email_type, documents_context, lang) -> str`
Generate formatted administrative email.

**Parameters:**
- `client`: Groq client instance
- `email_type`: Email category
- `documents_context`: Official document content
- `lang`: Language code

**Returns:** Formatted email string

#### `track_analytics(event, data) -> None`
Record analytics event.

**Parameters:**
- `event`: Event name (string)
- `data`: Optional event metadata (dict)

**Returns:** None

## Troubleshooting

### Common Issues

**Issue: High memory usage**
- Solution: Reduce `MAX_HISTORY_ITEMS` and `CACHE_TTL_SECONDS`

**Issue: Slow responses**
- Check: Groq API latency, cache hit rate
- Solution: Increase cache TTL, optimize prompts

**Issue: Rate limiting too aggressive**
- Solution: Adjust `RATE_LIMIT_REQUESTS` in config

**Issue: Session timeouts**
- Solution: Increase `SESSION_TIMEOUT_MINUTES`

## Maintenance

### Regular Tasks
- **Daily**: Check logs for errors
- **Weekly**: Review analytics for usage patterns
- **Monthly**: Update dependencies, security patches
- **Quarterly**: Backup history data, performance review

### Log Rotation
```python
# Automatic with logging.handlers.RotatingFileHandler
# Max size: 10MB
# Backups: 5 files
```

## License

MIT License - see LICENSE file for details.

## Support

Technical questions: dev@unihelp.example.com  
Bug reports: GitHub Issues
