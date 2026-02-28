# 🚀 UniHelp - Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Copy template
copy .env.example .env

# Edit .env and add your Groq key
GROQ_API_KEY=your_actual_key_here
```

### 3. Run the App
```bash
streamlit run app.py
```

✅ **Done!** Open http://localhost:8501

---

## Docker Quick Start

```bash
# Build and run in one command
docker-compose up --build
```

---

## First Steps

1. **Try Q&A**: Go to Tab A, ask: "What is the deadline to submit internship documentation?"
2. **Generate Email**: Go to Tab B, select "Internship request", click "Generate Email"
3. **Export**: Download your email in PDF, Markdown, HTML, or Text
4. **Check History**: Go to Tab C to see all your activity

---

## Key Features at a Glance

| Feature | Location | Description |
|---------|----------|-------------|
| 🤖 Q&A Chatbot | Tab A | Ask questions based on official docs |
| 📧 Email Generator | Tab B | Create 4 types of admin emails |
| 📜 History | Tab C | View past Q&A and emails |
| 🌍 Language | Sidebar | Switch FR/EN instantly |
| 📊 Analytics | Tab C | Usage statistics |
| 📥 Export | Tab B/C | PDF, MD, HTML, TXT formats |

---

## Troubleshooting

**App won't start?**
- Check Python version: `python --version` (need 3.10+)
- Install dependencies: `pip install -r requirements.txt`

**"Missing GROQ_API_KEY"?**
- Create `.env` file
- Add: `GROQ_API_KEY=your_key`
- Get key at: https://console.groq.com

**Rate limit error?**
- Wait 60 seconds
- Default: 10 requests per minute

---

## Pro Tips

💡 **Use caching**: Identical questions return instantly  
💡 **Dark mode**: Toggle in sidebar (coming soon)  
💡 **Keyboard shortcuts**: Ctrl+Enter to submit  
💡 **Export history**: All formats available in Tab C  
💡 **Clear data**: Sidebar → Clear history buttons  

---

## Next Steps

- 📖 Read [README.md](README.md) for full documentation
- 🔧 Read [TECHNICAL.md](TECHNICAL.md) for developer details
- 🐳 Deploy with [Docker](Dockerfile)
- 🚀 Set up [CI/CD](.github/workflows/ci-cd.yml)

---

**Need help?** Check [README.md](README.md) or open an issue!
