"""
Client API pour l'API PRIM d'Île-de-France Mobilités.
Mode SIMULATION si aucune clé API n'est fournie.
"""

import os
import random
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

IDFM_API_KEY = os.getenv("IDFM_API_KEY", "").strip()
BASE_URL = "https://prim.iledefrance-mobilites.fr/marketplace"

SIMULATION_MODE = not bool(IDFM_API_KEY)


class PRIMClient:
    """
    Client REST pour l'API PRIM (SIRI Lite).
    En l'absence de clé API, retourne des données simulées réalistes.
    """
    def __init__(self):
        self.api_key = IDFM_API_KEY
        self.simulation = SIMULATION_MODE
        self.session = requests.Session()
        if not self.simulation:
            self.session.headers.update({
                "apikey": self.api_key,
                "Accept": "application/json"
            })

    def is_simulation(self) -> bool:
        return self.simulation

    # ── Stop Monitoring ──────────────────────────────────────────────────────

    def get_stop_monitoring(self, monitoring_ref: str) -> dict | None:
        """
        Récupère les prochains passages à un arrêt donné (SIRI Lite).
        Args:
            monitoring_ref: Identifiant de l'arrêt (ex: 'STIF:StopArea:SP:50000')
        """
        if self.simulation:
            return None  # Géré par data_collector
        url = f"{BASE_URL}/stop-monitoring"
        params = {"MonitoringRef": monitoring_ref}
        try:
            resp = self.session.get(url, params=params, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            print(f"[API ERROR] stop-monitoring: {e}")
            return None

    # ── General Message (Alertes) ─────────────────────────────────────────────

    def get_general_messages(self, line_ref: str = None) -> dict | None:
        """
        Récupère les alertes trafic en cours.
        Args:
            line_ref: Optionnel – filtrer par ligne
        """
        if self.simulation:
            return None
        url = f"{BASE_URL}/general-message"
        params = {}
        if line_ref:
            params["LineRef"] = line_ref
        try:
            resp = self.session.get(url, params=params, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            print(f"[API ERROR] general-message: {e}")
            return None

    # ── Line Timetable ────────────────────────────────────────────────────────

    def get_line_timetable(self, line_ref: str, stop_ref: str) -> dict | None:
        """
        Récupère les horaires théoriques d'une ligne pour un arrêt.
        """
        if self.simulation:
            return None
        url = f"{BASE_URL}/line-timetable"
        params = {"LineRef": line_ref, "MonitoringRef": stop_ref}
        try:
            resp = self.session.get(url, params=params, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            print(f"[API ERROR] line-timetable: {e}")
            return None

    # ── GTFS-RT ───────────────────────────────────────────────────────────────

    def get_gtfs_rt_trip_updates(self) -> bytes | None:
        """
        Récupère le flux GTFS-RT Trip Updates (binaire protobuf).
        Nécessite la lib gtfs-realtime-bindings pour le parser.
        """
        if self.simulation:
            return None
        url = f"{BASE_URL}/gtfs-rt"
        try:
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
            return resp.content
        except requests.RequestException as e:
            print(f"[API ERROR] gtfs-rt: {e}")
            return None
