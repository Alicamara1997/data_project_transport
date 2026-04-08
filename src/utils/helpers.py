"""
Utilitaires généraux pour le projet transport IDF.
"""
from datetime import datetime
import pytz

PARIS_TZ = pytz.timezone("Europe/Paris")


def now_paris() -> datetime:
    """Retourne l'heure actuelle à Paris."""
    return datetime.now(PARIS_TZ)


def format_wait(minutes: int) -> str:
    """Formate une durée d'attente en texte lisible."""
    if minutes <= 0:
        return "À quai"
    if minutes == 1:
        return "1 min"
    return f"{minutes} min"


def get_status_color(status: str) -> str:
    """Retourne la couleur hex associée à un statut."""
    colors = {
        "normal":      "#22c55e",
        "disrupted":   "#f59e0b",
        "interrupted": "#ef4444",
    }
    return colors.get(status, "#888888")


def get_status_icon(status: str) -> str:
    """Retourne l'emoji associé à un statut."""
    icons = {
        "normal":      "✅",
        "disrupted":   "⚠️",
        "interrupted": "🔴",
    }
    return icons.get(status, "❓")


def get_status_label(status: str) -> str:
    """Retourne le label FR d'un statut."""
    labels = {
        "normal":      "Trafic normal",
        "disrupted":   "Perturbé",
        "interrupted": "Interrompu",
    }
    return labels.get(status, "Inconnu")


def congestion_color(pct: float) -> str:
    """Retourne une couleur en fonction du % de congestion."""
    if pct < 30:
        return "#22c55e"
    if pct < 60:
        return "#f59e0b"
    if pct < 85:
        return "#f97316"
    return "#ef4444"


def congestion_label(pct: float) -> str:
    """Retourne un label de congestion."""
    if pct < 30:
        return "Fluide"
    if pct < 60:
        return "Chargé"
    if pct < 85:
        return "Dense"
    return "Saturé"
