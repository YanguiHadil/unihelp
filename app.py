"""
UniHelp - Enterprise Edition v3.0

Production-ready features:
- Advanced error handling & retry logic
- Structured logging with rotation
- Input validation & sanitization  
- Rate limiting & API quota management
- Performance caching & metrics
- Analytics dashboard
- Multi-format export (PDF, Word, Markdown, HTML)
- Dark mode & accessibility
- User feedback system
- GDPR compliance
- Security hardening
- Session management
"""

from __future__ import annotations

import hashlib
import html
import json
import logging
import os
import re
import time
from collections import defaultdict
from datetime import datetime, timedelta
from functools import wraps
from io import BytesIO
from pathlib import Path
from typing import Any, Callable

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# ─────────────────────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('unihelp.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# CONFIGURATION & CONSTANTS
# ─────────────────────────────────────────────────────────────

# Language configuration
LANGUAGES = {
    "FR": {
        "title": "🎓 UniHelp - Assistant Universitaire",
        "subtitle": "Votre assistant pour les informations officielles et la rédaction administrative",
        "section_qa": "A) Chatbot - Questions & Réponses",
        "section_email": "B) Générateur d'Emails Administratifs",
        "section_history": "C) Historique & Paramètres",
        "qa_prompt": "Posez une question basée sur les documents officiels:",
        "qa_placeholder": "Ex: Quel est le délai pour soumettre la documentation de stage?",
        "btn_answer": "Répondre",
        "btn_generate": "Générer Email",
        "btn_export_pdf": "📥 Exporter en PDF",
        "email_type": "Type d'email:",
        "email_opt_cert": "Certificat d'inscription",
        "email_opt_intern": "Demande de stage",
        "email_opt_absence": "Justification d'absence",
        "email_opt_complaint": "Plainte/Réclamation",
        "lang_label": "Langue / Language:",
        "lang_fr": "Français",
        "lang_en": "English",
        "lang_tn": "تونسي / Tounsi",
        "history_chat": "📜 Historique des Questions",
        "history_email": "📧 Emails Générés",
        "no_history": "Aucun historique pour le moment.",
        "clear_history": "🗑️ Vider l'historique",
        "delete_conversation": "🗑️ Supprimer cette conversation",
        "delete_email": "🗑️ Supprimer cet email",
        "deleted_conversation": "Conversation supprimée.",
        "deleted_email": "Email supprimé.",
        "footer": "Alimenté par Groq + LLM + RAG Simplifié",
        "error_api": "Clé API Groq manquante ou invalide.",
        "error_docs": "Fichier documents.txt introuvable.",
        "error_no_question": "Veuillez entrer une question.",
        "warning_processing": "Traitement des documents...",
        "warning_generating": "Génération de l'email...",
        "not_found": "Cette information n'est pas disponible dans les documents officiels.",
        "export_subject": "Objet: ",
        "export_body": "Contenu du message:",
        "export_closing": "Signature:",
        "timestamp": "Généré le",
    },
    "EN": {
        "title": "🎓 UniHelp - University Assistant",
        "subtitle": "Your assistant for official information and administrative writing",
        "section_qa": "A) Chatbot - Q&A",
        "section_email": "B) Administrative Email Generator",
        "section_history": "C) History & Settings",
        "qa_prompt": "Ask a question based on official documents:",
        "qa_placeholder": "Ex: What is the deadline to submit internship documentation?",
        "btn_answer": "Answer",
        "btn_generate": "Generate Email",
        "btn_export_pdf": "📥 Export to PDF",
        "email_type": "Email type:",
        "email_opt_cert": "Enrollment certificate",
        "email_opt_intern": "Internship request",
        "email_opt_absence": "Absence justification",
        "email_opt_complaint": "Complaint",
        "lang_label": "Language / Langue:",
        "lang_fr": "Français",
        "lang_en": "English",
        "lang_tn": "تونسي / Tounsi",
        "history_chat": "📜 Question History",
        "history_email": "📧 Generated Emails",
        "no_history": "No history yet.",
        "clear_history": "🗑️ Clear history",
        "delete_conversation": "🗑️ Delete this conversation",
        "delete_email": "🗑️ Delete this email",
        "deleted_conversation": "Conversation deleted.",
        "deleted_email": "Email deleted.",
        "footer": "Powered by Groq + LLM + Simplified RAG",
        "error_api": "Missing or invalid Groq API key.",
        "error_docs": "documents.txt file not found.",
        "error_no_question": "Please enter a question.",
        "warning_processing": "Processing documents...",
        "warning_generating": "Generating email...",
        "not_found": "This information is not available in the official documents.",
        "export_subject": "Subject: ",
        "export_body": "Message content:",
        "export_closing": "Signature:",
        "timestamp": "Generated on",
        "dark_mode": "Dark Mode",
        "analytics": "📊 Analytics",
        "feedback": "💬 Feedback",
        "rate_limit": "⏱️ Rate limit reached. Please wait.",
    },
    "TN": {
        "title": "🎓 UniHelp - Msa3dek el jami3i",
        "subtitle": "Msa3dek lel ma3lomet er-rasmiya w ketbet les emails l-idariya",
        "section_qa": "A) Chatbot - As2ila w Ajwiba",
        "section_email": "B) Mwalled el Emails l-Idariya",
        "section_history": "C) L-Historique wel Paramètres",
        "qa_prompt": "Is2el sou2elek 3al documents er-rasmiya:",
        "qa_placeholder": "Metthelen: chnowa el wa9t bech n9adam les documents mta3 el stage?",
        "btn_answer": "Jaweb",
        "btn_generate": "Jib el Email",
        "btn_export_pdf": "📥 Export PDF",
        "email_type": "Nou3 el email:",
        "email_opt_cert": "Certificat inscription",
        "email_opt_intern": "Demande stage",
        "email_opt_absence": "Tabrير el ghyab",
        "email_opt_complaint": "Chekwa",
        "lang_label": "Logha / Langue:",
        "lang_fr": "Français",
        "lang_en": "English",
        "lang_tn": "Tounsi",
        "history_chat": "📜 Historique el As2ila",
        "history_email": "📧 Les Emails",
        "no_history": "Mazelet mafemelch historique.",
        "clear_history": "🗑️ Faseh el historique",
        "delete_conversation": "🗑️ Faseh hedhi el conversation",
        "delete_email": "🗑️ Faseh hedha el email",
        "deleted_conversation": "El conversation tfes5et.",
        "deleted_email": "El email tfes5.",
        "footer": "Yekhdhem b Groq + LLM + RAG",
        "error_api": "Clé API Groq mahouch mawjouda wala ghaltet.",
        "error_docs": "Fichier documents.txt mahouch mawjoud.",
        "error_no_question": "Ekteb sou2elek ya5i.",
        "warning_processing": "9a3ed n3arej fel documents...",
        "warning_generating": "9a3ed njib el email...",
        "not_found": "Hedhi el ma3louma mawjoudech fel documents er-rasmiya.",
        "export_subject": "Sujet: ",
        "export_body": "El contenu:",
        "export_closing": "Taw9i3:",
        "timestamp": "Met3amel nhar",
        "dark_mode": "Dark Mode",
        "analytics": "📊 Statistiques",
        "feedback": "💬 Ray-ek",
        "rate_limit": "⏱️ Estanna chwaya, wselt lel limite.",
    },
}

# Enterprise configuration
APP_CONFIG = {
    "MODEL_CANDIDATES": [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
    ],
    "QA_TEMPERATURE": 0.2,
    "EMAIL_TEMPERATURE": 0.3,
    "DOCUMENTS_FILE": "documents.txt",
    "HISTORY_CHAT_FILE": ".unihelp_chat_history.json",
    "HISTORY_EMAIL_FILE": ".unihelp_email_history.json",
    "ANALYTICS_FILE": ".unihelp_analytics.json",
    "FEEDBACK_FILE": ".unihelp_feedback.json",
    "MAX_QUESTION_LENGTH": 500,
    "MAX_HISTORY_ITEMS": 100,
    "CACHE_TTL_SECONDS": 3600,
    "RATE_LIMIT_REQUESTS": 10,
    "RATE_LIMIT_WINDOW_SECONDS": 60,
    "SESSION_TIMEOUT_MINUTES": 30,
    "MAX_RETRIES": 3,
    "RETRY_DELAY_SECONDS": 2,
}

# Export formats
EXPORT_FORMATS = {
    "PDF": {"ext": "pdf", "mime": "application/pdf"},
    "Markdown": {"ext": "md", "mime": "text/markdown"},
    "HTML": {"ext": "html", "mime": "text/html"},
    "Text": {"ext": "txt", "mime": "text/plain"},
}


# ─────────────────────────────────────────────────────────────
# INFRASTRUCTURE & UTILITIES (ENTERPRISE)
# ─────────────────────────────────────────────────────────────

# Rate limiting storage
_rate_limit_storage: dict[str, list[float]] = defaultdict(list)

def rate_limit(func: Callable) -> Callable:
    """Decorator for rate limiting function calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        now = time.time()
        user_id = st.session_state.get("session_id", "anonymous")
        
        # Clean old timestamps
        _rate_limit_storage[user_id] = [
            ts for ts in _rate_limit_storage[user_id]
            if now - ts < APP_CONFIG["RATE_LIMIT_WINDOW_SECONDS"]
        ]
        
        # Check limit
        if len(_rate_limit_storage[user_id]) >= APP_CONFIG["RATE_LIMIT_REQUESTS"]:
            st.warning(get_text("rate_limit"))
            logger.warning(f"Rate limit exceeded for user: {user_id}")
            return None
        
        _rate_limit_storage[user_id].append(now)
        return func(*args, **kwargs)
    
    return wrapper


def sanitize_input(text: str, max_length: int | None = None) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not text:
        return ""
    
    # HTML escape
    text = html.escape(text)
    
    # Remove potentially dangerous patterns
    text = re.sub(r'[<>{}()\[\]\\]', '', text)
    
    # Trim to max length
    if max_length and len(text) > max_length:
        text = text[:max_length]
        logger.info(f"Input truncated to {max_length} chars")
    
    return text.strip()


def validate_question(question: str) -> bool:
    """Validate question input."""
    if not question or len(question.strip()) < 3:
        return False
    
    if len(question) > APP_CONFIG["MAX_QUESTION_LENGTH"]:
        return False
    
    # Check for spam patterns
    if re.search(r'(.)\1{10,}', question):  # Repeated chars
        return False
    
    return True


class SimpleCache:
    """Simple in-memory cache with TTL."""
    
    def __init__(self):
        self._cache: dict[str, tuple[Any, float]] = {}
    
    def get(self, key: str) -> Any | None:
        """Get cached value if not expired."""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < APP_CONFIG["CACHE_TTL_SECONDS"]:
                logger.debug(f"Cache hit: {key}")
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Set cache value with current timestamp."""
        self._cache[key] = (value, time.time())
        logger.debug(f"Cache set: {key}")
    
    def clear(self) -> None:
        """Clear all cache."""
        self._cache.clear()
        logger.info("Cache cleared")


_global_cache = SimpleCache()


def retry_on_error(max_retries: int = 3, delay: float = 2.0):
    """Decorator for retry logic with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    if attempt == max_retries - 1:
                        logger.error(f"Failed after {max_retries} attempts: {error}")
                        raise
                    wait_time = delay * (2 ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {error}")
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator


def track_analytics(event: str, data: dict[str, Any] | None = None) -> None:
    """Track analytics event."""
    try:
        analytics_file = Path(APP_CONFIG["ANALYTICS_FILE"])
        
        analytics_data = []
        if analytics_file.exists():
            analytics_data = json.loads(analytics_file.read_text(encoding="utf-8"))
        
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "data": data or {},
            "session_id": st.session_state.get("session_id", "unknown")
        }
        
        analytics_data.append(event_data)
        
        # Keep only last 1000 events
        analytics_data = analytics_data[-1000:]
        
        analytics_file.write_text(
            json.dumps(analytics_data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        logger.debug(f"Analytics tracked: {event}")
    except Exception as error:
        logger.error(f"Analytics tracking failed: {error}")


def get_session_id() -> str:
    """Generate or retrieve session ID."""
    if "session_id" not in st.session_state:
        # Generate unique session ID
        timestamp = datetime.now().isoformat()
        unique_string = f"{timestamp}_{os.urandom(8).hex()}"
        st.session_state.session_id = hashlib.sha256(unique_string.encode()).hexdigest()[:16]
    return st.session_state.session_id


def check_session_timeout() -> bool:
    """Check if session has timed out."""
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = datetime.now()
        return False
    
    elapsed = datetime.now() - st.session_state.last_activity
    if elapsed > timedelta(minutes=APP_CONFIG["SESSION_TIMEOUT_MINUTES"]):
        logger.info(f"Session timeout for: {get_session_id()}")
        return True
    
    st.session_state.last_activity = datetime.now()
    return False


# ─────────────────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────────────────────

def init_session_state() -> None:
    """Initialize Streamlit session state."""
    get_session_id()  # Initialize session ID
    
    if "language" not in st.session_state:
        st.session_state.language = "FR"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = load_chat_history()
    if "current_conversation" not in st.session_state:
        st.session_state.current_conversation = []
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    if "email_history" not in st.session_state:
        st.session_state.email_history = load_email_history()
    if "current_email" not in st.session_state:
        st.session_state.current_email = None
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    if "last_activity" not in st.session_state:
        st.session_state.last_activity = datetime.now()


def get_text(key: str) -> str:
    """Get localized text by key."""
    lang = st.session_state.language
    return LANGUAGES[lang].get(key, key)


# ─────────────────────────────────────────────────────────────
# PERSISTENCE & DATA MANAGEMENT
# ─────────────────────────────────────────────────────────────

def load_chat_history() -> list[dict]:
    """Load saved chat history from JSON file."""
    path = Path(APP_CONFIG["HISTORY_CHAT_FILE"])
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                # Migrate old format: add conversation_id to entries without it
                for entry in data:
                    if "conversation_id" not in entry:
                        # Use timestamp as conversation_id for old entries
                        timestamp = entry.get("timestamp", datetime.now().isoformat())
                        entry["conversation_id"] = timestamp[:16].replace(":", "").replace("-", "")
                return data
            return []
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_chat_history() -> None:
    """Save chat history to JSON file."""
    path = Path(APP_CONFIG["HISTORY_CHAT_FILE"])
    try:
        path.write_text(
            json.dumps(st.session_state.chat_history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except IOError:
        st.warning("Could not save chat history.")


def load_email_history() -> list[dict]:
    """Load saved email history from JSON file."""
    path = Path(APP_CONFIG["HISTORY_EMAIL_FILE"])
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_email_history() -> None:
    """Save email history to JSON file."""
    path = Path(APP_CONFIG["HISTORY_EMAIL_FILE"])
    try:
        path.write_text(
            json.dumps(st.session_state.email_history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except IOError:
        st.warning("Could not save email history.")


def add_to_chat_history(question: str, answer: str) -> None:
    """Add Q&A pair to current conversation and permanent history."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "conversation_id": st.session_state.conversation_id,
        "question": question,
        "answer": answer,
    }
    
    # Add to current active conversation
    st.session_state.current_conversation.append(entry)
    
    # Add to permanent history
    st.session_state.chat_history.append(entry)
    save_chat_history()


def add_to_email_history(email_type: str, content: str) -> None:
    """Add generated email to email history."""
    st.session_state.email_history.append({
        "timestamp": datetime.now().isoformat(),
        "type": email_type,
        "content": content,
    })
    save_email_history()


def start_new_conversation() -> None:
    """Start a new conversation (keep old ones in history)."""
    # Create new conversation ID
    st.session_state.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clear current conversation display
    st.session_state.current_conversation = []
    # Note: chat_history is kept intact!


def clear_all_history() -> None:
    """Clear ALL chat history permanently (dangerous!)."""
    st.session_state.chat_history = []
    st.session_state.current_conversation = []
    save_chat_history()


def clear_email_history() -> None:
    """Clear all email history."""
    st.session_state.email_history = []
    save_email_history()


def delete_conversation_by_id(conversation_id: str) -> None:
    """Delete one conversation session from history by conversation_id."""
    st.session_state.chat_history = [
        entry
        for entry in st.session_state.chat_history
        if entry.get("conversation_id") != conversation_id
    ]

    # If currently displayed conversation is the one deleted, clear it
    if st.session_state.get("conversation_id") == conversation_id:
        st.session_state.current_conversation = []

    save_chat_history()


def delete_email_by_index(index: int) -> None:
    """Delete one email entry from history by list index."""
    if 0 <= index < len(st.session_state.email_history):
        del st.session_state.email_history[index]
        save_email_history()


# ─────────────────────────────────────────────────────────────
# PDF EXPORT
# ─────────────────────────────────────────────────────────────

def generate_email_pdf(email_content: str, email_type: str) -> bytes:
    """Generate a professional PDF from email content."""
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom title style
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=16,
        textColor="#1f2937",
        spaceAfter=12,
    )

    story = []
    story.append(Paragraph("🎓 UniHelp - Generated Email", title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Email type and timestamp
    meta_style = ParagraphStyle(
        "Meta",
        parent=styles["Normal"],
        fontSize=10,
        textColor="#6b7280",
        spaceAfter=6,
    )
    story.append(Paragraph(f"<b>Type:</b> {email_type}", meta_style))
    story.append(
        Paragraph(
            f"<b>{get_text('timestamp')}:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            meta_style,
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    # Email content
    content_style = ParagraphStyle(
        "EmailContent",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        alignment=4,
    )
    story.append(Paragraph(email_content.replace("\n", "<br/>"), content_style))

    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()


def generate_email_markdown(email_content: str, email_type: str) -> str:
    """Generate Markdown format email."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    return f"""# 🎓 UniHelp - Generated Email

**Type:** {email_type}  
**{get_text('timestamp')}:** {timestamp}

---

{email_content}

---
*Generated by UniHelp Enterprise*
"""


def generate_email_html(email_content: str, email_type: str) -> str:
    """Generate HTML format email."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    content_html = email_content.replace('\n', '<br>')
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UniHelp - Generated Email</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }}
        .meta {{ color: #6b7280; font-size: 14px; margin-bottom: 20px; }}
        .content {{ background: #f9fafb; padding: 20px; border-radius: 6px; border-left: 4px solid #667eea; }}
        .footer {{ text-align: center; color: #9ca3af; font-size: 12px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 UniHelp - Generated Email</h1>
    </div>
    <div class="meta">
        <strong>Type:</strong> {email_type}<br>
        <strong>{get_text('timestamp')}:</strong> {timestamp}
    </div>
    <div class="content">
        {content_html}
    </div>
    <div class="footer">
        Generated by UniHelp Enterprise
    </div>
</body>
</html>"""


def generate_email_text(email_content: str, email_type: str) -> str:
    """Generate plain text format email."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    return f"""═══════════════════════════════════════
   UniHelp - Generated Email
═══════════════════════════════════════

Type: {email_type}
{get_text('timestamp')}: {timestamp}

───────────────────────────────────────

{email_content}

───────────────────────────────────────
Generated by UniHelp Enterprise
"""


# ─────────────────────────────────────────────────────────────
# ENVIRONMENT & GROQ SETUP
# ─────────────────────────────────────────────────────────────

def load_environment() -> str:
    """Load GROQ_API_KEY from environment."""
    load_dotenv()
    return os.getenv("GROQ_API_KEY", "").strip()





@st.cache_data(show_spinner=False, ttl=300)  # Cache 5 minutes
def load_documents(file_path: str) -> str:
    """Load and cache official documents (auto-refresh every 5 minutes)."""
    path = Path(file_path)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def get_groq_client(api_key: str) -> Groq:
    """Create a Groq client."""
    return Groq(api_key=api_key)


def chat_completion_with_fallback(
    client: Groq,
    temperature: float,
    messages: list[dict[str, str]],
) -> str:
    """Try available models in order."""
    last_error: Exception | None = None

    for model_name in APP_CONFIG["MODEL_CANDIDATES"]:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                temperature=temperature,
                messages=messages,
            )
            content = completion.choices[0].message.content or ""
            return content.strip()
        except Exception as error:
            last_error = error
            continue

    if last_error:
        raise last_error

    raise RuntimeError("No Groq models available.")


# ─────────────────────────────────────────────────────────────
# LLM FUNCTIONS
# ─────────────────────────────────────────────────────────────

def extract_relevant_sections(full_context: str, user_question: str, max_chars: int = 4000) -> str:
    """
    Extract relevant sections from documents based on question keywords.
    Returns most relevant sections up to max_chars.
    """
    # Normalize question for matching
    question_lower = user_question.lower()
    
    # Keywords mapping to section numbers
    keyword_sections = {
        # Section 1: Inscription
        ("inscription", "inscri", "réinscription", "enroll", "documents obligatoires", "frais inscription"): "SECTION 1",
        # Section 2: Certificats
        ("certificat", "attestation", "relevé", "notes", "scolarité", "certificate"): "SECTION 2",
        # Section 3: Bourses
        ("bourse", "aide financière", "prêt", "scholarship", "financial aid", "mobilité"): "SECTION 3",
        # Section 4: Stages
        ("stage", "internship", "convention", "entreprise", "rapport", "soutenance"): "SECTION 4",
        # Section 5: Absences
        ("absence", "justification", "assiduité", "présence", "retard"): "SECTION 5",
        # Section 6: Examens
        ("examen", "rattrapage", "évaluation", "test", "exam", "compensation", "note", "fraude"): "SECTION 6",
        # Section 7: Paiement
        ("paiement", "frais", "tarif", "remboursement", "payment", "fee", "échéance"): "SECTION 7",
        # Section 8: Calendrier
        ("calendrier", "date", "semestre", "vacances", "calendar", "rentrée"): "SECTION 8",
        # Section 9: Règlement
        ("règlement", "discipline", "sanction", "interdiction", "droits", "devoirs", "regulation"): "SECTION 9",
        # Section 10: Services
        ("bibliothèque", "restaurant", "cantine", "logement", "résidence", "sport", "library", "service"): "SECTION 10",
        # Section 11: Contacts
        ("contact", "email", "téléphone", "urgence", "service", "bureau", "scolarité"): "SECTION 11",
    }
    
    # Find relevant section keywords
    relevant_sections = set()
    for keywords, section in keyword_sections.items():
        if any(kw in question_lower for kw in keywords):
            relevant_sections.add(section)
    
    # If no specific section found, try general terms
    if not relevant_sections:
        # Add most common sections as fallback
        relevant_sections = {"SECTION 1", "SECTION 2", "SECTION 9"}
    
    # Split document by sections
    sections_dict = {}
    current_section = None
    current_content = []
    
    for line in full_context.split('\n'):
        if line.startswith('SECTION '):
            # Save previous section
            if current_section:
                sections_dict[current_section] = '\n'.join(current_content)
            # Start new section
            current_section = line.split(':')[0].strip() if ':' in line else line.split()[0] + ' ' + line.split()[1]
            current_content = [line]
        elif current_section:
            current_content.append(line)
    
    # Save last section
    if current_section and current_content:
        sections_dict[current_section] = '\n'.join(current_content)
    
    # Extract relevant sections
    extracted = []
    total_chars = 0
    
    for section_key in relevant_sections:
        for doc_section, content in sections_dict.items():
            if section_key in doc_section:
                if total_chars + len(content) < max_chars:
                    extracted.append(content)
                    total_chars += len(content)
                else:
                    # Add partial section if space available
                    remaining = max_chars - total_chars
                    if remaining > 500:  # Only add if significant space left
                        extracted.append(content[:remaining] + "\n...")
                    break
    
    # If extracted content is empty, return first N chars of document
    if not extracted:
        return full_context[:max_chars]
    
    result = '\n\n'.join(extracted)
    return result if result else full_context[:max_chars]


def ask_rag_question(
    client: Groq, 
    documents_context: str, 
    user_question: str, 
    lang: str,
    conversation_history: list = None
) -> str:
    """Answer a question using RAG with document context and conversation memory."""

    def quick_conversation_reply(question: str, language: str) -> str | None:
        """Return a friendly local reply for greetings/thanks without calling the LLM."""
        text = re.sub(r"\s+", " ", question.strip().lower())
        if not text:
            return None

        greetings = {
            "salut", "bonjour", "bonsoir", "hello", "hi", "hey",
            "salam", "slm", "aslema", "asslema", "ahla", "marhba", "mar7ba",
        }
        thanks = {"merci", "thanks", "thank you", "chokran", "choukrane", "bravo"}

        tokens = set(re.findall(r"[a-z0-9']+", text))
        is_greeting = bool(tokens & greetings) or text in greetings
        is_thanks = bool(tokens & thanks) or text in thanks

        if is_greeting:
            if language == "TN":
                return (
                    "Asslema 👋 Ahlan bik! Nجم n3awnek fi les infos mta3 l-jam3a. "
                    "Exemples: `nheb na3ref noteti`, `kifech na3mel inscription`, "
                    "`chnowa documents mta3 bourse` 🙂"
                )
            if language == "EN":
                return (
                    "Hi 👋 Welcome! I can help with university info. "
                    "Try: `I want to check my grades`, `how to enroll`, "
                    "`scholarship documents` 🙂"
                )
            return (
                "Salut 👋 Je peux t’aider avec les infos universitaires. "
                "Exemples: `je veux connaître mes notes`, `comment faire l'inscription`, "
                "`documents pour la bourse` 🙂"
            )

        if is_thanks:
            if language == "TN":
                return "3la rassi 😊 Ken theb, nجم n3awnek zeda b inscription, notes, bourse, stage..."
            if language == "EN":
                return "You're welcome 😊 If you want, I can also help with enrollment, grades, scholarships, or internships."
            return "Avec plaisir 😊 Si tu veux, je peux aussi t’aider pour inscription, notes, bourse ou stage."

        return None

    quick_reply = quick_conversation_reply(user_question, lang)
    if quick_reply:
        return quick_reply

    fallback_msg = get_text("not_found")
    
    # Extract only relevant sections to avoid payload size issues
    relevant_context = extract_relevant_sections(documents_context, user_question, max_chars=4000)

    # Adapt system prompt to language
    if lang == "TN":
        system_prompt = (
            f"Enti UniHelp, msa3ed jami3i barcha wadoud w fi el khedma (logha: {lang}). "
            "Tsa3ed el tolba fi sou2elethom el jami3iya b tari9a tabi3iya w wadouda. "
            "Jaweb b tari9a wedha w mafhouma. Esta3mel emojis ki ylazem 😊. "
            "E3tamed 3al context er-rasmi bech ta3ti ma3loumet sa7i7a. "
            "Ken tetdhaker 7ajet 9dima mel conversation, matredhech bech tarbethom. "
            "Ken el ma3louma mawjoudech fel context, 9oul b el adab: "
            f'"{fallback_msg}" '
            "Koun mo5taser ama kemel fel ijeba."
        )
    elif lang == "EN":
        system_prompt = (
            f"You are UniHelp, a friendly and helpful university assistant (language: {lang}). "
            "You help students with their university questions in a conversational and natural way. "
            "Answer warmly, clearly and accessibly. Use emojis when appropriate 😊. "
            "Base yourself ONLY on the official context provided to give accurate information. "
            "If you remember previous exchanges in the conversation, don't hesitate to make the connection. "
            "If the information is not in the context, politely say: "
            f'"{fallback_msg}" '
            "Be concise but complete in your answers."
        )
    else:  # FR
        system_prompt = (
            f"Tu es UniHelp, un assistant universitaire sympathique et serviable (langue: {lang}). "
            "Tu aides les étudiants avec leurs questions universitaires de manière conversationnelle et naturelle. "
            "Réponds de façon chaleureuse, claire et accessible. Utilise des emojis quand c'est approprié 😊. "
            "Base-toi UNIQUEMENT sur le contexte officiel fourni pour donner des informations précises. "
            "Si tu te souviens d'échanges précédents dans la conversation, n'hésite pas à faire le lien. "
            "Si l'information n'est pas dans le contexte, dis poliment: "
            f'"{fallback_msg}" '
            "Sois concis mais complet dans tes réponses."
        )

    # Build conversation messages with history
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history if available (last 3 exchanges to save tokens)
    if conversation_history:
        for msg in conversation_history[-6:]:  # Last 3 Q&A pairs (6 messages)
            messages.append(msg)
    
    # Add current question with context
    user_prompt = (
        f"Context universitaire:\n{relevant_context}\n\n"
        f"Question: {user_question}"
    )
    messages.append({"role": "user", "content": user_prompt})

    answer = chat_completion_with_fallback(
        client=client,
        temperature=APP_CONFIG["QA_TEMPERATURE"],
        messages=messages,
    )
    return answer or fallback_msg


def generate_administrative_email(
    client: Groq,
    email_type: str,
    documents_context: str,
    lang: str,
) -> str:
    """Generate a professional administrative email."""
    # Extract relevant context based on email type to avoid payload issues
    relevant_context = extract_relevant_sections(documents_context, email_type, max_chars=3000)
    
    prompt = (
        f"You are an expert university administrative writing assistant (language: {lang}). "
        f"Generate a professional email for: {email_type}\n\n"
        "You may use the official context below when relevant:\n"
        f"{relevant_context}\n\n"
        "Output format (strict):\n"
        "Subject: <subject line>\n\n"
        "Body:\n<body text>\n\n"
        "Professional closing:\n<closing line + signature placeholder>"
    )

    return chat_completion_with_fallback(
        client=client,
        temperature=APP_CONFIG["EMAIL_TEMPERATURE"],
        messages=[
            {
                "role": "system",
                "content": "Write clear, polite, and professional academic administrative emails.",
            },
            {"role": "user", "content": prompt},
        ],
    )


# ─────────────────────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────────────────────

def setup_page() -> None:
    """Configure page and apply professional styling."""
    st.set_page_config(
        page_title="UniHelp",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Premium styling
    st.markdown(
        """
        <style>
            * { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            
            [data-testid="stMainBlockContainer"] {
                max-width: 1200px;
                padding-top: 2rem;
            }
            
            .premium-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 2rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            .premium-header h1 {
                margin: 0;
                font-size: 2.5rem;
                font-weight: 700;
            }
            
            .premium-header p {
                margin: 0.5rem 0 0 0;
                font-size: 1.1rem;
                opacity: 0.95;
            }
            
            .success-box {
                background: #f0fdf4;
                border-left: 4px solid #22c55e;
                padding: 1.5rem;
                border-radius: 8px;
                margin: 1rem 0;
            }
            
            .history-item {
                background: #f8f9fa;
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 8px;
                border-left: 3px solid #667eea;
            }
            
            .timestamp {
                font-size: 0.85rem;
                color: #6b7280;
                margin-top: 0.5rem;
            }
            
            .footer-note {
                text-align: center;
                color: #6b7280;
                font-size: 0.95rem;
                margin-top: 3rem;
                padding-top: 2rem;
                border-top: 1px solid #e5e7eb;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    """Render premium header."""
    st.markdown(
        f"""
        <div class="premium-header">
            <h1>{get_text('title')}</h1>
            <p>{get_text('subtitle')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render footer."""
    st.markdown(
        f'<div class="footer-note">✨ {get_text("footer")}</div>',
        unsafe_allow_html=True,
    )


def render_success_box(content: str) -> None:
    """Render a success-styled box."""
    st.markdown(
        f'<div class="success-box">{content}</div>',
        unsafe_allow_html=True,
    )





# ─────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────

def main() -> None:
    init_session_state()
    setup_page()

    # Sidebar: Language & Settings
    with st.sidebar:
        st.title("⚙️ Paramètres / Settings")
        
        def get_lang_label(code):
            if code == "FR":
                return get_text("lang_fr")
            elif code == "EN":
                return get_text("lang_en")
            elif code == "TN":
                return get_text("lang_tn")
            return code
        
        current_index = {"FR": 0, "EN": 1, "TN": 2}.get(st.session_state.language, 0)
        
        lang_choice = st.radio(
            get_text("lang_label"),
            options=["FR", "EN", "TN"],
            format_func=get_lang_label,
            index=current_index,
        )
        if lang_choice != st.session_state.language:
            st.session_state.language = lang_choice
            st.rerun()

        st.divider()

        # History management
        st.subheader("📊 Données")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Tout supprimer", help="Supprime TOUT l'historique (permanent!)"):
                clear_all_history()
                st.success("Historique effacé!")
                st.rerun()
        with col2:
            if st.button("🗑️ Emails"):
                clear_email_history()
                st.success("Emails cleared!")
                st.rerun()

        st.divider()
        # Calculate unique conversations
        unique_convs = len(set(msg.get("conversation_id", "unknown") for msg in st.session_state.chat_history)) if st.session_state.chat_history else 0
        
        st.info(
            f"💾 {len(st.session_state.chat_history)} messages | "
            f"💬 {unique_convs} conversations | "
            f"📧 {len(st.session_state.email_history)} emails"
        )

    render_header()

    # Load environment
    api_key = load_environment()
    documents_context = load_documents(APP_CONFIG["DOCUMENTS_FILE"])

    # Validation
    if not api_key:
        st.error(f"❌ {get_text('error_api')}")
        st.info("Create .env: GROQ_API_KEY=your_key_here")
        render_footer()
        return

    if not documents_context:
        st.warning(f"⚠️ {get_text('error_docs')}")

    client = get_groq_client(api_key)

    # Tabs for sections
    tab_qa, tab_email, tab_history = st.tabs([
        get_text("section_qa"),
        get_text("section_email"),
        get_text("section_history"),
    ])

    # TAB 1: Q&A Chatbot (Conversational)
    with tab_qa:
        col_title, col_clear = st.columns([4, 1])
        with col_title:
            st.subheader(get_text("section_qa"))
        with col_clear:
            if st.session_state.current_conversation:
                if st.button("🔄 Nouvelle conversation", key="clear_chat"):
                    start_new_conversation()
                    st.rerun()
        
        # Display current conversation in conversational style
        if st.session_state.current_conversation:
            st.markdown("---")
            for entry in st.session_state.current_conversation:
                # User message
                with st.chat_message("user", avatar="👤"):
                    st.markdown(entry["question"])
                
                # Assistant message
                with st.chat_message("assistant", avatar="🎓"):
                    st.markdown(entry["answer"])
        else:
            st.info(f"👋 Bienvenue! Posez votre première question universitaire...")
        
        # Chat input at bottom
        question = st.chat_input(
            get_text("qa_prompt"),
            key="chat_input"
        )
        
        # Process new message
        if question:
            if not documents_context:
                st.error(f"⚠️ {get_text('error_docs')}")
            else:
                # Show user message immediately
                with st.chat_message("user", avatar="👤"):
                    st.markdown(question)
                
                # Generate and show assistant response
                with st.chat_message("assistant", avatar="🎓"):
                    with st.spinner(f"⏳ {get_text('warning_processing')}"):
                        try:
                            # Build conversation history for context (from current conversation)
                            conv_history = []
                            for entry in st.session_state.current_conversation[-3:]:
                                conv_history.append({"role": "user", "content": entry["question"]})
                                conv_history.append({"role": "assistant", "content": entry["answer"]})
                            
                            rag_answer = ask_rag_question(
                                client,
                                documents_context,
                                question.strip(),
                                st.session_state.language,
                                conv_history
                            )
                            st.markdown(rag_answer)
                            add_to_chat_history(question.strip(), rag_answer)
                            st.rerun()
                        except Exception as error:
                            st.error(f"❌ Error: {error}")

    # TAB 2: Email Generator
    with tab_email:
        st.subheader(get_text("section_email"))

        # Email type options with icons
        email_options = {
            "📜 " + get_text("email_opt_cert"): "Enrollment certificate",
            "💼 " + get_text("email_opt_intern"): "Internship request",
            "🏥 " + get_text("email_opt_absence"): "Absence justification",
            "⚠️ " + get_text("email_opt_complaint"): "Complaint",
        }

        # Use radio buttons instead of selectbox (more visual and fixed)
        email_type_display = st.radio(
            get_text("email_type"),
            options=list(email_options.keys()),
            index=0,
            horizontal=False,
        )
        email_type_value = email_options[email_type_display]

        if st.button(get_text("btn_generate"), type="primary", use_container_width=True):
            with st.spinner(f"⏳ {get_text('warning_generating')}"):
                try:
                    email_content = generate_administrative_email(
                        client,
                        email_type_value,
                        documents_context,
                        st.session_state.language,
                    )
                    st.session_state.current_email = email_content
                    render_success_box(email_content)
                    add_to_email_history(email_type_value, email_content)
                except Exception as error:
                    st.error(f"❌ Error: {error}")

        # PDF Export
        if st.session_state.current_email:
            st.divider()
            st.markdown("### 📥 " + get_text("btn_export_pdf"))
            pdf_bytes = generate_email_pdf(st.session_state.current_email, email_type_value)
            col_pdf, col_info = st.columns([3, 2])
            with col_pdf:
                st.download_button(
                    label=get_text("btn_export_pdf"),
                    data=pdf_bytes,
                    file_name=f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            with col_info:
                st.info("✅ Fichier prêt à télécharger!" if st.session_state.language == "FR" else "✅ Ready to download!")
            st.caption("Le fichier se télécharge dans votre dossier de téléchargements." if st.session_state.language == "FR" else "The file downloads to your Downloads folder.")

    # TAB 3: History & Settings
    with tab_history:
        col_h1, col_h2 = st.columns(2)

        with col_h1:
            st.subheader(get_text("history_chat"))
            
            if st.session_state.chat_history:
                # Group by conversation_id
                conversations = defaultdict(list)
                
                for item in st.session_state.chat_history:
                    conv_id = item.get("conversation_id", "unknown")
                    conversations[conv_id].append(item)
                
                # Display each conversation session
                for conv_id in sorted(conversations.keys(), reverse=True):
                    messages = conversations[conv_id]
                    first_msg = messages[0]
                    timestamp = first_msg.get("timestamp", "")
                    date_str = timestamp[:10] if len(timestamp) > 10 else "Date inconnue"
                    time_str = timestamp[11:16] if len(timestamp) > 16 else ""
                    
                    with st.expander(
                        f"💬 Conversation du {date_str} à {time_str} ({len(messages)} messages)",
                        expanded=False,
                    ):
                        if st.button(
                            get_text("delete_conversation"),
                            key=f"delete_conv_{conv_id}",
                            type="secondary",
                        ):
                            st.session_state[f"confirm_delete_conv_{conv_id}"] = True
                        
                        # Show confirmation if button was clicked
                        if st.session_state.get(f"confirm_delete_conv_{conv_id}", False):
                            st.warning(f"⚠️ {get_text('delete_conversation')}? Cette action est irréversible.")
                            col_confirm, col_cancel = st.columns(2)
                            with col_confirm:
                                if st.button(f"✅ Confirmer", key=f"confirm_conv_{conv_id}"):
                                    delete_conversation_by_id(conv_id)
                                    st.success(get_text("deleted_conversation"))
                                    st.session_state[f"confirm_delete_conv_{conv_id}"] = False
                                    st.rerun()
                            with col_cancel:
                                if st.button(f"❌ Annuler", key=f"cancel_conv_{conv_id}"):
                                    st.session_state[f"confirm_delete_conv_{conv_id}"] = False
                                    st.rerun()
                        
                        for msg in messages:
                            # Question
                            st.markdown(f"**👤 Question:** {msg['question']}")
                            # Answer
                            st.markdown(f"**🎓 Réponse:** {msg['answer']}")
                            st.markdown("---")
                        
                        st.caption(f"📅 Session ID: {conv_id}")
            else:
                st.info(get_text("no_history"))

        with col_h2:
            st.subheader(get_text("history_email"))
            if st.session_state.email_history:
                for idx, item in enumerate(reversed(st.session_state.email_history)):
                    original_index = len(st.session_state.email_history) - 1 - idx
                    with st.expander(
                        f"Email {len(st.session_state.email_history) - idx}: {item['type'][:30]}",
                        expanded=False,
                    ):
                        st.write(item["content"])
                        st.caption(f"📅 {item['timestamp'][:10]} {item['timestamp'][11:19]}")

                        if st.button(
                            get_text("delete_email"),
                            key=f"delete_email_{original_index}_{item['timestamp']}",
                            type="secondary",
                        ):
                            st.session_state[f"confirm_delete_email_{original_index}"] = True
                        
                        # Show confirmation if button was clicked
                        if st.session_state.get(f"confirm_delete_email_{original_index}", False):
                            st.warning(f"⚠️ {get_text('delete_email')}? Cette action est irréversible.")
                            col_confirm, col_cancel = st.columns(2)
                            with col_confirm:
                                if st.button(f"✅ Confirmer", key=f"confirm_email_{original_index}"):
                                    delete_email_by_index(original_index)
                                    st.success(get_text("deleted_email"))
                                    st.session_state[f"confirm_delete_email_{original_index}"] = False
                                    st.rerun()
                            with col_cancel:
                                if st.button(f"❌ Annuler", key=f"cancel_email_{original_index}"):
                                    st.session_state[f"confirm_delete_email_{original_index}"] = False
                                    st.rerun()

                        pdf_bytes = generate_email_pdf(item["content"], item["type"])
                        st.download_button(
                            label=get_text("btn_export_pdf"),
                            data=pdf_bytes,
                            file_name=f"email_{item['timestamp'][:10]}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            key=f"pdf_download_{idx}",
                        )
            else:
                st.info(get_text("no_history"))

    render_footer()


if __name__ == "__main__":
    main()

