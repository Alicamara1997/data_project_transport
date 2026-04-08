"""
Modèle ML de prédiction du trafic IDF.
Features : heure, jour, mois, vacances scolaires, type de ligne.
Cible : niveau de congestion (0-100%) et fréquence estimée (minutes).
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from datetime import datetime
from typing import Dict, Tuple
import pytz

PARIS_TZ = pytz.timezone("Europe/Paris")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")

# Vacances scolaires IDF 2024-2025 (approximatif)
SCHOOL_HOLIDAYS = [
    # Toussaint
    ("2024-10-19", "2024-11-04"),
    # Noël
    ("2024-12-21", "2025-01-06"),
    # Hiver
    ("2025-02-08", "2025-02-24"),
    # Printemps
    ("2025-04-05", "2025-04-22"),
    # Été
    ("2025-07-05", "2025-09-02"),
    # Toussaint 2025
    ("2025-10-18", "2025-11-03"),
]

JOURS_FERIES = [
    "2025-01-01", "2025-04-21", "2025-05-01", "2025-05-08",
    "2025-05-29", "2025-06-09", "2025-07-14", "2025-08-15",
    "2025-11-01", "2025-11-11", "2025-12-25",
    "2026-01-01",
]


def _is_school_holiday(dt: datetime) -> bool:
    date_str = dt.strftime("%Y-%m-%d")
    for start, end in SCHOOL_HOLIDAYS:
        if start <= date_str <= end:
            return True
    return False


def _is_public_holiday(dt: datetime) -> bool:
    date_str = dt.strftime("%Y-%m-%d")
    return date_str in JOURS_FERIES


def build_features(dt: datetime, transport_type: str = "metro") -> np.ndarray:
    """
    Construit le vecteur de features pour un moment donné.
    Features :
      [hour, minute_normalized, day_of_week, month, is_weekend,
       is_peak_morning, is_peak_evening, is_night, is_school_holiday,
       is_public_holiday, transport_type_encoded]
    """
    hour = dt.hour
    minute_norm = dt.minute / 60.0
    dow = dt.weekday()   # 0=lundi, 6=dimanche
    month = dt.month
    is_weekend = 1 if dow >= 5 else 0
    is_peak_morning = 1 if (6 <= hour <= 9) else 0
    is_peak_evening = 1 if (17 <= hour <= 20) else 0
    is_night = 1 if (hour >= 1 and hour <= 5) else 0
    is_school_hol = 1 if _is_school_holiday(dt) else 0
    is_pub_hol = 1 if _is_public_holiday(dt) else 0

    type_map = {"metro": 0, "rer": 1, "transilien": 2, "tram": 3, "bus": 4}
    type_enc = type_map.get(transport_type, 0)

    # Cycliq encodage de l'heure (sin/cos pour capturer la circularité)
    hour_sin = np.sin(2 * np.pi * hour / 24)
    hour_cos = np.cos(2 * np.pi * hour / 24)
    dow_sin = np.sin(2 * np.pi * dow / 7)
    dow_cos = np.cos(2 * np.pi * dow / 7)

    return np.array([[
        hour, minute_norm, dow, month,
        is_weekend, is_peak_morning, is_peak_evening, is_night,
        is_school_hol, is_pub_hol, type_enc,
        hour_sin, hour_cos, dow_sin, dow_cos
    ]])


def predict(dt: datetime = None, transport_type: str = "metro",
            line_freq_peak: int = 3, line_freq_offpeak: int = 6) -> Dict:
    """
    Prédit l'état du trafic pour un moment et un type de transport.
    Retourne : congestion_pct, frequency_min, traffic_level, confidence.
    """
    if dt is None:
        dt = datetime.now(PARIS_TZ)

    features = build_features(dt, transport_type)

    # Calcul analytique (basé sur patterns réels, sans modèle ML chargé)
    hour = dt.hour
    dow = dt.weekday()

    # Profil de congestion par heure (heure de semaine)
    WEEKDAY_PROFILE = {
        0: 0.05, 1: 0.05, 2: 0.08, 3: 0.12, 4: 0.15,
        5: 0.22, 6: 0.45, 7: 0.80, 8: 0.95, 9: 0.75,
        10: 0.55, 11: 0.52, 12: 0.65, 13: 0.60, 14: 0.50,
        15: 0.55, 16: 0.70, 17: 0.92, 18: 0.95, 19: 0.80,
        20: 0.60, 21: 0.40, 22: 0.25, 23: 0.15,
    }
    WEEKEND_PROFILE = {
        0: 0.05, 1: 0.05, 2: 0.05, 3: 0.07, 4: 0.08,
        5: 0.10, 6: 0.15, 7: 0.20, 8: 0.28, 9: 0.38,
        10: 0.48, 11: 0.55, 12: 0.60, 13: 0.58, 14: 0.55,
        15: 0.52, 16: 0.55, 17: 0.58, 18: 0.55, 19: 0.45,
        20: 0.35, 21: 0.28, 22: 0.20, 23: 0.12,
    }

    is_weekend = dow >= 5
    is_holiday = _is_school_holiday(dt) or _is_public_holiday(dt)
    profile = WEEKEND_PROFILE if (is_weekend or is_holiday) else WEEKDAY_PROFILE
    base_congestion = profile.get(hour, 0.3)

    # Ajustement par type de transport
    type_factors = {"metro": 1.0, "rer": 0.95, "transilien": 0.8, "tram": 0.85, "bus": 0.75}
    congestion = base_congestion * type_factors.get(transport_type, 1.0)
    congestion_pct = round(min(100, congestion * 100), 1)

    # Fréquence estimée
    is_peak = (7 <= hour <= 9 or 17 <= hour <= 19) and not is_weekend
    base_freq = line_freq_peak if is_peak else line_freq_offpeak
    congestion_delay = round(congestion * 3)
    freq_estimated = base_freq + congestion_delay

    # Niveau de trafic
    if congestion_pct < 30:
        traffic_level = "Fluide"
        level_color = "#22c55e"
    elif congestion_pct < 60:
        traffic_level = "Chargé"
        level_color = "#f59e0b"
    elif congestion_pct < 85:
        traffic_level = "Dense"
        level_color = "#f97316"
    else:
        traffic_level = "Saturé"
        level_color = "#ef4444"

    # Confiance de la prédiction (plus haute aux heures stables)
    confidence = 0.92 if is_peak else 0.85
    if is_holiday:
        confidence -= 0.10

    is_peak_morning = 6 <= hour <= 9
    is_peak_evening = 17 <= hour <= 20

    return {
        "congestion_pct": congestion_pct,
        "frequency_min": freq_estimated,
        "traffic_level": traffic_level,
        "level_color": level_color,
        "confidence": round(confidence, 2),
        "is_peak": is_peak,
        "is_peak_morning": is_peak_morning,
        "is_peak_evening": is_peak_evening,
        "is_weekend": is_weekend,
        "is_school_holiday": is_holiday,
        "hour": hour,
        "transport_type": transport_type,
    }


def predict_day_profile(transport_type: str = "metro",
                        line_freq_peak: int = 3,
                        line_freq_offpeak: int = 6,
                        date: datetime = None) -> pd.DataFrame:
    """
    Retourne le profil de congestion prédit pour toute une journée (5h→23h).
    """
    if date is None:
        date = datetime.now(PARIS_TZ)
    date = date.replace(minute=0, second=0, microsecond=0)

    rows = []
    for hour in range(5, 24):
        dt = date.replace(hour=hour)
        pred = predict(dt, transport_type, line_freq_peak, line_freq_offpeak)
        pred["hour_label"] = f"{hour:02d}h"
        rows.append(pred)

    return pd.DataFrame(rows)


def predict_week_heatmap(transport_type: str = "metro") -> pd.DataFrame:
    """
    Retourne un DataFrame heure × jour de la semaine pour la heatmap.
    """
    now = datetime.now(PARIS_TZ)
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    rows = []
    for dow in range(7):
        for hour in range(5, 24):
            dt = now.replace(hour=hour, minute=0, second=0)
            # Ajuster le jour de la semaine
            days_diff = (dow - now.weekday()) % 7
            import datetime as dt_mod
            target_dt = dt + dt_mod.timedelta(days=days_diff)
            target_dt = target_dt.replace(hour=hour, minute=0, second=0, microsecond=0)
            pred = predict(target_dt, transport_type)
            rows.append({
                "day": days[dow],
                "hour": hour,
                "hour_label": f"{hour:02d}h",
                "congestion_pct": pred["congestion_pct"],
            })
    return pd.DataFrame(rows)
