# 🎓 UniHelp - Enterprise Edition v3.0

**Professional AI-powered university administrative assistant with RAG capabilities.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)](https://streamlit.io)

---

## 🚀 Features

### Core Functionality
- ✅ **RAG-based Q&A** - Answer questions strictly from official university documents
- ✅ **Email Generator** - Professional administrative email templates
- ✅ **Multi-language** - Full French/English support
- ✅ **History Tracking** - Persistent chat and email history

### Enterprise Features
- 🔒 **Security** - Input sanitization, rate limiting, session management
- 📊 **Analytics** - Usage tracking and metrics dashboard
- ⚡ **Performance** - Smart caching with TTL, retry logic with exponential backoff
- 📥 **Multi-format Export** - PDF, Markdown, HTML, Plain Text
- 🌙 **Dark Mode** - Eye-friendly interface
- 💬 **Feedback System** - User feedback collection
- 🔄 **Auto-retry** - Resilient API calls with fallback models
- 📝 **Structured Logging** - Production-ready logging with rotation
- ⏱️ **Rate Limiting** - API quota management
- 🔐 **GDPR Compliant** - Data privacy and user control

---

## 📋 Prerequisites

- Python 3.10 or higher
- Groq API key ([Get one here](https://console.groq.com))
- 512 MB RAM minimum
- Modern web browser (Chrome/Firefox/Edge recommended)

---

## 🛠️ Installation

### Quick Start

```bash
# Clone or download the repository
cd unihelp

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_key_here

# Run the application
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 🐳 Docker Deployment

```bash
# Build image
docker build -t unihelp:latest .

# Run container
docker run -p 8501:8501 --env-file .env unihelp:latest
```

---

## 📁 Project Structure

```
unihelp/
├── app.py                  # Main application (Enterprise Edition)
├── documents.txt           # University official documents (RAG source)
├── .env                    # Environment variables (API keys)
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── .gitignore             # Git exclusions
├── README.md              # This file
├── unihelp.log            # Application logs (auto-generated)
└── .unihelp_*.json        # Data persistence files (auto-generated)
```

---

## 🔧 Configuration

### Environment Variables

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
GROQ_MODEL=llama-3.1-8b-instant  # Override default model
```

### App Configuration

Edit `APP_CONFIG` in `app.py` to customize:

- `MAX_QUESTION_LENGTH`: Maximum question length (default: 500)
- `MAX_HISTORY_ITEMS`: History retention limit (default: 100)
- `CACHE_TTL_SECONDS`: Cache expiration time (default: 3600)
- `RATE_LIMIT_REQUESTS`: Max requests per window (default: 10)
- `RATE_LIMIT_WINDOW_SECONDS`: Rate limit window (default: 60)
- `SESSION_TIMEOUT_MINUTES`: Session timeout (default: 30)

---

## 📊 Usage

### 1. Question Answering (RAG)

1. Navigate to **Tab A: Chatbot**
2. Enter your question in the text area
3. Click **"Answer"** button
4. Receive answer based only on official documents

### 2. Email Generation

1. Navigate to **Tab B: Email Generator**
2. Select email type from dropdown
3. Click **"Generate Email"**
4. Export to PDF, Markdown, HTML, or Text

### 3. History & Analytics

1. Navigate to **Tab C: History & Settings**
2. View past Q&A sessions
3. Access generated emails
4. Review usage analytics

### 4. Settings

Use the **sidebar** to:
- Switch language (FR/EN)
- Toggle dark mode
- Clear history
- View session statistics

---

## 🔒 Security Features

- **Input Sanitization**: XSS and injection prevention
- **Rate Limiting**: Prevents API abuse
- **Session Management**: Automatic timeout after inactivity
- **Secure Logging**: Sensitive data excluded from logs
- **HTTPS Ready**: TLS/SSL compatible

---

## 📈 Analytics & Metrics

UniHelp tracks:
- Questions asked (anonymized)
- Emails generated (by type)
- API usage and errors
- Session duration
- Feature usage patterns

Data is stored locally in `.unihelp_analytics.json` and can be reviewed in the Analytics dashboard.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🔧 Troubleshooting

### Issue: "Missing GROQ_API_KEY"
**Solution**: Create `.env` file and add your Groq API key

### Issue: "Model decommissioned"
**Solution**: App automatically retries with fallback models

### Issue: Rate limit exceeded
**Solution**: Wait 60 seconds or adjust `RATE_LIMIT_REQUESTS` in config

### Issue: Session timeout
**Solution**: Adjust `SESSION_TIMEOUT_MINUTES` or refresh the page

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Groq** - Lightning-fast LLM inference
- **Streamlit** - Beautiful web app framework
- **ReportLab** - Professional PDF generation

---

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Contact: support@unihelp.example.com

---

## 🗺️ Roadmap

- [ ] Multi-tenant support
- [ ] PostgreSQL backend option
- [ ] Redis caching layer
- [ ] Prometheus metrics export
- [ ] Admin dashboard
- [ ] API endpoints (REST/GraphQL)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics with charts

---

**Made with ❤️ for universities worldwide**
