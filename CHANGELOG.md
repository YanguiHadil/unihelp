# Changelog

All notable changes to UniHelp will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-02-27

### Added - Enterprise Edition

#### Infrastructure & Performance
- ✨ Structured logging with file rotation (.log files)
- ⚡ Smart caching system with TTL (3600s default)
- 🔄 Retry logic with exponential backoff (3 attempts)
- 📊 Analytics tracking system (.unihelp_analytics.json)
- ⏱️ Rate limiting (10 req/60s per session)
- 🔐 Session management with timeout (30min default)

#### Security & Validation
- 🛡️ Input sanitization (XSS prevention)
- ✅ Question validation (length, spam detection)
- 🔒 Secure session IDs (SHA256 hashing)
- 📝 GDPR-compliant data handling
- 🚫 Special character filtering

#### Export & Features
- 📥 Multi-format export: PDF, Markdown, HTML, Plain Text
- 🌙 Dark mode support (UI toggle)
- 💬 User feedback system
- 📈 Usage analytics dashboard
- 🌍 Enhanced multi-language (FR/EN)

#### DevOps & Deployment
- 🐳 Production Dockerfile with health checks
- 📦 Docker Compose configuration
- 🔧 GitHub Actions CI/CD pipeline
- 📚 Comprehensive README.md
- 📖 Technical documentation (TECHNICAL.md)
- 📄 MIT License
- 🚫 .gitignore for sensitive files
- 📦 requirements.txt with pinned versions

#### Code Quality
- 🏗️ Modular architecture
- 📝 Type hints throughout
- 📋 Comprehensive docstrings
- 🧪 CI/CD integration (lint, test, build)
- 🔍 Security scanning (Bandit)

### Changed
- ♻️ Refactored session state initialization
- 🔧 Improved error handling with logging
- 📊 Enhanced analytics with session attribution
- 🎨 Updated UI with better spacing and colors

### Fixed
- 🐛 Model deprecation handling (auto-fallback)
- 🔧 PDF export navigation issues
- 📱 Chrome browser compatibility
- ⚡ Performance bottlenecks in history loading

---

## [2.0.0] - 2026-02-26

### Added - Premium Edition
- 🎨 Advanced UI with premium gradient header
- 📜 Chat history persistence (JSON)
- 📧 Email history with timestamps
- 🌐 Multi-language support (FR/EN)
- 📥 PDF export for emails
- 📑 Tab-based navigation
- 🎯 Sidebar settings panel
- 🗑️ History clearing buttons

### Changed
- 🎨 Improved styling with custom CSS
- 📦 Better file organization
- 🔧 Streamlit configuration optimization

---

## [1.0.0] - 2026-02-25

### Added - Initial Release
- ✅ RAG-based question answering
- ✅ Administrative email generator (4 types)
- ✅ Groq API integration
- ✅ Document-based context injection
- ✅ Basic UI with Streamlit
- ✅ .env configuration
- ✅ Simple success/error messaging

### Features
- Question answering from documents.txt
- Email templates:
  - Enrollment certificate
  - Internship request
  - Absence justification
  - Complaint
- Fallback message for unavailable information

---

## Future Roadmap

### [4.0.0] - Planned
- [ ] PostgreSQL database backend
- [ ] Redis distributed caching
- [ ] REST API endpoints
- [ ] Admin dashboard
- [ ] Multi-tenant support
- [ ] Advanced analytics with charts
- [ ] Email templates customization
- [ ] Webhook integrations
- [ ] Mobile app (React Native)

### [3.1.0] - Next Sprint
- [ ] Prometheus metrics export
- [ ] Grafana dashboard templates
- [ ] Advanced search in history
- [ ] Bulk email generation
- [ ] Template management UI
- [ ] Custom branding options

---

## Notes

### Breaking Changes
- **v3.0.0**: New session management requires session_id initialization
- **v2.0.0**: History file format changed to include timestamps

### Migration Guides
- **v2.x → v3.x**: No manual migration needed, session data auto-initialized
- **v1.x → v2.x**: History files auto-convert on first load

### Security Notices
- **2026-02-27**: Added rate limiting to prevent API abuse
- **2026-02-26**: Implemented input sanitization for XSS prevention

---

[3.0.0]: https://github.com/yourorg/unihelp/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/yourorg/unihelp/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/yourorg/unihelp/releases/tag/v1.0.0
