"""
Référentiel complet des lignes de transport en commun d'Île-de-France.
Données basées sur les référentiels officiels IDFM/RATP.
"""

# ─────────────────────────────────────────────
# MÉTRO (lignes 1 à 14 + GPE)
# ─────────────────────────────────────────────
METRO_LINES = {
    "1":  {"name": "Ligne 1",  "color": "#FFBE00", "terminus": ["La Défense", "Château de Vincennes"], "type": "metro", "frequency_peak": 2, "frequency_offpeak": 4},
    "2":  {"name": "Ligne 2",  "color": "#003CA6", "terminus": ["Porte Dauphine", "Nation"], "type": "metro", "frequency_peak": 3, "frequency_offpeak": 5},
    "3":  {"name": "Ligne 3",  "color": "#837902", "terminus": ["Pont de Levallois", "Gallieni"], "type": "metro", "frequency_peak": 3, "frequency_offpeak": 6},
    "3B": {"name": "Ligne 3b", "color": "#6EC4E8", "terminus": ["Gambetta", "Saint-Fargeau"], "type": "metro", "frequency_peak": 6, "frequency_offpeak": 10},
    "4":  {"name": "Ligne 4",  "color": "#CF009E", "terminus": ["Porte de Clignancourt", "Montrouge"], "type": "metro", "frequency_peak": 2, "frequency_offpeak": 5},
    "5":  {"name": "Ligne 5",  "color": "#FF7E2E", "terminus": ["Bobigny-Pablo Picasso", "Place d'Italie"], "type": "metro", "frequency_peak": 3, "frequency_offpeak": 6},
    "6":  {"name": "Ligne 6",  "color": "#6ECA97", "terminus": ["Charles de Gaulle–Étoile", "Nation"], "type": "metro", "frequency_peak": 3, "frequency_offpeak": 6},
    "7":  {"name": "Ligne 7",  "color": "#FA2D87", "terminus": ["La Courneuve", "Villejuif/Mairie d'Ivry"], "type": "metro", "frequency_peak": 3, "frequency_offpeak": 6},
    "7B": {"name": "Ligne 7b", "color": "#6ECA97", "terminus": ["Louis Blanc", "Pré-Saint-Gervais"], "type": "metro", "frequency_peak": 6, "frequency_offpeak": 10},
    "8":  {"name": "Ligne 8",  "color": "#E19BDF", "terminus": ["Balard", "Créteil-Préfecture"], "type": "metro", "frequency_peak": 3, "frequency_offpeak": 6},
    "9":  {"name": "Ligne 9",  "color": "#B6BD00", "terminus": ["Pont de Sèvres", "Mairie de Montreuil"], "type": "metro", "frequency_peak": 3, "frequency_offpeak": 5},
    "10": {"name": "Ligne 10", "color": "#C9910D", "terminus": ["Boulogne–Pont de Saint-Cloud", "Gare d'Austerlitz"], "type": "metro", "frequency_peak": 5, "frequency_offpeak": 8},
    "11": {"name": "Ligne 11", "color": "#704B1C", "terminus": ["Châtelet", "Les Lilas"], "type": "metro", "frequency_peak": 4, "frequency_offpeak": 7},
    "12": {"name": "Ligne 12", "color": "#007852", "terminus": ["Aubervilliers", "Mairie d'Issy"], "type": "metro", "frequency_peak": 3, "frequency_offpeak": 5},
    "13": {"name": "Ligne 13", "color": "#6EC4E8", "terminus": ["Asnières/Saint-Denis", "Châtillon/Montrouge"], "type": "metro", "frequency_peak": 3, "frequency_offpeak": 5},
    "14": {"name": "Ligne 14", "color": "#62259D", "terminus": ["Mairie de Saint-Ouen", "Orly Aéroport T1-T2"], "type": "metro", "frequency_peak": 2, "frequency_offpeak": 3},
}

# ─────────────────────────────────────────────
# RER
# ─────────────────────────────────────────────
RER_LINES = {
    "A": {"name": "RER A", "color": "#E2231A", "terminus": ["Cergy/Poissy", "Marne-la-Vallée/Boissy"], "type": "rer", "frequency_peak": 4, "frequency_offpeak": 8},
    "B": {"name": "RER B", "color": "#547DB2", "terminus": ["Roissy CDG/Mitry-Mory", "Robinson/Saint-Rémy"], "type": "rer", "frequency_peak": 5, "frequency_offpeak": 10},
    "C": {"name": "RER C", "color": "#FFBE00", "terminus": ["Versailles/Massy/Pontoise", "Juvisy/Dourdan/Étampes"], "type": "rer", "frequency_peak": 10, "frequency_offpeak": 15},
    "D": {"name": "RER D", "color": "#00843D", "terminus": ["Creil/Orry-la-Ville", "Melun/Malesherbes/Corbeil"], "type": "rer", "frequency_peak": 10, "frequency_offpeak": 15},
    "E": {"name": "RER E", "color": "#C04E9E", "terminus": ["Mantes-la-Jolie", "Tournan/Chelles-Gournay"], "type": "rer", "frequency_peak": 8, "frequency_offpeak": 12},
}

# ─────────────────────────────────────────────
# TRANSILIEN
# ─────────────────────────────────────────────
TRANSILIEN_LINES = {
    "H": {"name": "Transilien H", "color": "#8D5E2A", "terminus": ["Gare du Nord", "Pontoise/Luzarches/Creil"], "type": "transilien", "frequency_peak": 10, "frequency_offpeak": 20},
    "J": {"name": "Transilien J", "color": "#B4C9E8", "terminus": ["Gare Saint-Lazare", "Mantes/Ermont-Eaubonne/Vernon"], "type": "transilien", "frequency_peak": 10, "frequency_offpeak": 20},
    "K": {"name": "Transilien K", "color": "#B4C9E8", "terminus": ["Gare du Nord", "Crépy-en-Valois"], "type": "transilien", "frequency_peak": 30, "frequency_offpeak": 60},
    "L": {"name": "Transilien L", "color": "#B4C9E8", "terminus": ["Gare Saint-Lazare", "Versailles/Saint-Nom/Cergy"], "type": "transilien", "frequency_peak": 10, "frequency_offpeak": 20},
    "N": {"name": "Transilien N", "color": "#B4C9E8", "terminus": ["Gare Montparnasse", "Rambouillet/Mantes"], "type": "transilien", "frequency_peak": 15, "frequency_offpeak": 30},
    "P": {"name": "Transilien P", "color": "#B4C9E8", "terminus": ["Gare de l'Est", "Provins/Coulommiers/Château-Thierry"], "type": "transilien", "frequency_peak": 15, "frequency_offpeak": 30},
    "R": {"name": "Transilien R", "color": "#B4C9E8", "terminus": ["Gare de Lyon", "Montereau/Montargis"], "type": "transilien", "frequency_peak": 15, "frequency_offpeak": 30},
    "U": {"name": "Transilien U", "color": "#B4C9E8", "terminus": ["La Défense", "Versailles-Chantiers"], "type": "transilien", "frequency_peak": 15, "frequency_offpeak": 30},
}

# ─────────────────────────────────────────────
# TRAMWAY
# ─────────────────────────────────────────────
TRAM_LINES = {
    "T1":  {"name": "Tram T1",  "color": "#009EB3", "terminus": ["Saint-Denis Université", "Noisy-le-Sec"], "type": "tram", "frequency_peak": 4, "frequency_offpeak": 6},
    "T2":  {"name": "Tram T2",  "color": "#009EB3", "terminus": ["La Défense", "Versailles-Chantiers"], "type": "tram", "frequency_peak": 5, "frequency_offpeak": 8},
    "T3A": {"name": "Tram T3a", "color": "#009EB3", "terminus": ["Pont du Garigliano", "Porte de Vincennes"], "type": "tram", "frequency_peak": 5, "frequency_offpeak": 8},
    "T3B": {"name": "Tram T3b", "color": "#009EB3", "terminus": ["Porte de Vincennes", "Porte de la Chapelle"], "type": "tram", "frequency_peak": 5, "frequency_offpeak": 8},
    "T4":  {"name": "Tram T4",  "color": "#E05206", "terminus": ["Bondy", "Montfermeil"], "type": "tram", "frequency_peak": 6, "frequency_offpeak": 10},
    "T5":  {"name": "Tram T5",  "color": "#009EB3", "terminus": ["Saint-Denis Université", "Garges-Sarcelles"], "type": "tram", "frequency_peak": 6, "frequency_offpeak": 10},
    "T6":  {"name": "Tram T6",  "color": "#009EB3", "terminus": ["Châtillon-Montrouge", "Vélizy-Viroflay"], "type": "tram", "frequency_peak": 6, "frequency_offpeak": 10},
    "T7":  {"name": "Tram T7",  "color": "#009EB3", "terminus": ["Villejuif Louis Aragon", "Athis-Mons"], "type": "tram", "frequency_peak": 6, "frequency_offpeak": 10},
    "T8":  {"name": "Tram T8",  "color": "#009EB3", "terminus": ["Rosa Parks", "Saint-Denis"], "type": "tram", "frequency_peak": 6, "frequency_offpeak": 10},
    "T9":  {"name": "Tram T9",  "color": "#009EB3", "terminus": ["Porte de Choisy", "Orly"], "type": "tram", "frequency_peak": 6, "frequency_offpeak": 10},
    "T10": {"name": "Tram T10", "color": "#009EB3", "terminus": ["Antony", "Les Baconnets"], "type": "tram", "frequency_peak": 8, "frequency_offpeak": 12},
    "T11": {"name": "Tram T11", "color": "#E05206", "terminus": ["Le Bourget", "Épinay-Villetaneuse"], "type": "tram", "frequency_peak": 8, "frequency_offpeak": 12},
    "T13": {"name": "Tram T13", "color": "#009EB3", "terminus": ["Saint-Germain-en-Laye", "Versailles-Rive-Droite"], "type": "tram", "frequency_peak": 15, "frequency_offpeak": 20},
}

# ─────────────────────────────────────────────
# PRINCIPALES LIGNES BUS (Paris intra-muros)
# ─────────────────────────────────────────────
BUS_LINES = {
    "21":  {"name": "Bus 21",  "color": "#82C8E6", "terminus": ["Gare Saint-Lazare", "Stade Charléty"], "type": "bus", "frequency_peak": 5, "frequency_offpeak": 10},
    "26":  {"name": "Bus 26",  "color": "#82C8E6", "terminus": ["Gare Saint-Lazare", "Cours de Vincennes"], "type": "bus", "frequency_peak": 5, "frequency_offpeak": 10},
    "29":  {"name": "Bus 29",  "color": "#82C8E6", "terminus": ["Opéra", "Gare de Lyon"], "type": "bus", "frequency_peak": 5, "frequency_offpeak": 10},
    "38":  {"name": "Bus 38",  "color": "#82C8E6", "terminus": ["Gare du Nord", "Stade Charléty"], "type": "bus", "frequency_peak": 5, "frequency_offpeak": 10},
    "42":  {"name": "Bus 42",  "color": "#82C8E6", "terminus": ["Gare du Nord", "Bobigny"], "type": "bus", "frequency_peak": 6, "frequency_offpeak": 12},
    "63":  {"name": "Bus 63",  "color": "#82C8E6", "terminus": ["Porte de la Muette", "Gare de Lyon"], "type": "bus", "frequency_peak": 5, "frequency_offpeak": 10},
    "69":  {"name": "Bus 69",  "color": "#82C8E6", "terminus": ["Champ de Mars", "Gambetta"], "type": "bus", "frequency_peak": 7, "frequency_offpeak": 12},
    "73":  {"name": "Bus 73",  "color": "#82C8E6", "terminus": ["La Défense", "Musée d'Orsay"], "type": "bus", "frequency_peak": 6, "frequency_offpeak": 10},
    "91":  {"name": "Bus 91",  "color": "#82C8E6", "terminus": ["Gare Montparnasse", "Gare de Bercy"], "type": "bus", "frequency_peak": 6, "frequency_offpeak": 12},
    "95":  {"name": "Bus 95",  "color": "#82C8E6", "terminus": ["Montrouge", "Île-Saint-Denis"], "type": "bus", "frequency_peak": 5, "frequency_offpeak": 10},
    "N01": {"name": "Noctilien N01", "color": "#003082", "terminus": ["Gare de l'Est", "Clichy"], "type": "bus", "frequency_peak": 30, "frequency_offpeak": 30},
    "N02": {"name": "Noctilien N02", "color": "#003082", "terminus": ["Gare de l'Est", "Saint-Germain-en-Laye"], "type": "bus", "frequency_peak": 30, "frequency_offpeak": 30},
}

# ─────────────────────────────────────────────
# RÉFÉRENTIEL COMPLET
# ─────────────────────────────────────────────
ALL_LINES = {}
ALL_LINES.update({f"metro_{k}": v for k, v in METRO_LINES.items()})
ALL_LINES.update({f"rer_{k}": v for k, v in RER_LINES.items()})
ALL_LINES.update({f"transilien_{k}": v for k, v in TRANSILIEN_LINES.items()})
ALL_LINES.update({f"tram_{k}": v for k, v in TRAM_LINES.items()})
ALL_LINES.update({f"bus_{k}": v for k, v in BUS_LINES.items()})

TRANSPORT_TYPES = {
    "metro": {"label": "🚇 Métro", "icon": "🚇", "lines": METRO_LINES},
    "rer": {"label": "🚆 RER", "icon": "🚆", "lines": RER_LINES},
    "transilien": {"label": "🚉 Transilien", "icon": "🚉", "lines": TRANSILIEN_LINES},
    "tram": {"label": "🚊 Tramway", "icon": "🚊", "lines": TRAM_LINES},
    "bus": {"label": "🚌 Bus", "icon": "🚌", "lines": BUS_LINES},
}

# Principaux arrêts par ligne (échantillon représentatif)
MAIN_STOPS = {
    "metro_1":  ["La Défense", "Esplanade de La Défense", "Pont de Neuilly", "Les Sablons", "Porte Maillot", "Argentine", "Charles de Gaulle-Étoile", "George V", "Franklin D. Roosevelt", "Champs-Élysées-Clemenceau", "Invalides", "Concorde", "Tuileries", "Palais Royal", "Louvre-Rivoli", "Châtelet", "Hôtel de Ville", "Saint-Paul", "Bastille", "Gare de Lyon", "Nation", "Château de Vincennes"],
    "metro_4":  ["Porte de Clignancourt", "Simplon", "Marcadet-Poissonniers", "Château Rouge", "Barbès-Rochechouart", "Gare du Nord", "Gare de l'Est", "Strasbourg-Saint-Denis", "Réaumur-Sébastopol", "Étienne Marcel", "Les Halles", "Châtelet", "Cité", "Saint-Michel", "Odéon", "Saint-Germain-des-Prés", "Saint-Sulpice", "Saint-Placide", "Montparnasse-Bienvenüe", "Alésia", "Mouton-Duvernet", "Montrouge"],
    "metro_14": ["Mairie de Saint-Ouen", "Saint-Ouen", "Clichy-Saint-Ouen", "Pont Cardinet", "Saint-Lazare", "Madeleine", "Pyramides", "Châtelet", "Gare de Lyon", "Bercy", "Cour Saint-Émilion", "Bibliothèque François Mitterrand", "Olympiades", "Aéroport d'Orly T1-T2"],
    "rer_a":    ["Cergy Le Haut", "Cergy-Préfecture", "Conflans-Fin d'Oise", "Saint-Germain-en-Laye", "Poissy", "La Verrière", "Mantes-la-Jolie", "Nanterre-Préfecture", "La Défense", "Charles de Gaulle-Étoile", "Auber", "Châtelet–Les Halles", "Gare de Lyon", "Nation", "Vincennes", "Marne-la-Vallée–Chessy"],
    "rer_b":    ["Roissy-CDG T2", "Roissy-CDG T1", "Le Blanc-Mesnil", "Drancy", "La Courneuve", "Gare du Nord", "Châtelet–Les Halles", "Saint-Michel-Notre-Dame", "Denfert-Rochereau", "Laplace", "Arcueil-Cachan", "Bourg-la-Reine", "Robinson", "Massy-Palaiseau", "Saint-Rémy-lès-Chevreuse"],
    "tram_T3A": ["Pont du Garigliano", "Balard", "Georges Brassens", "Brancion", "Porte de Vanves", "Didot", "Porte d'Orléans", "Alésia-Rémi Dumoncel", "Montsouris", "Cité Universitaire", "Porte de Gentilly", "Kremlin-Bicêtre", "Villejuif-Louis Aragon", "Porte de Choisy", "Porte d'Ivry", "Pierre et Marie Curie", "Bibliothèque F. Mitterrand", "Porte de Vincennes"],
}

# Coordonnées des principales stations Paris (lat, lon)
STATION_COORDS = {
    "Châtelet":                  (48.8594, 2.3470),
    "Gare du Nord":              (48.8809, 2.3553),
    "Gare de Lyon":              (48.8449, 2.3733),
    "Gare de l'Est":             (48.8765, 2.3585),
    "Gare Montparnasse":         (48.8440, 2.3210),
    "Saint-Lazare":              (48.8754, 2.3247),
    "La Défense":                (48.8923, 2.2359),
    "Nation":                    (48.8487, 2.3961),
    "Bastille":                  (48.8533, 2.3696),
    "Opéra":                     (48.8719, 2.3317),
    "Charles de Gaulle-Étoile":  (48.8739, 2.2950),
    "Denfert-Rochereau":         (48.8338, 2.3326),
    "Bibliothèque F. Mitterrand":(48.8295, 2.3751),
    "Porte Maillot":             (48.8792, 2.2827),
    "Vincennes":                 (48.8481, 2.4390),
    "Marne-la-Vallée–Chessy":   (48.8730, 2.7808),
    "Versailles-Chantiers":      (48.7847, 2.1377),
    "Roissy-CDG T2":             (49.0042, 2.5715),
    "Orly Aéroport T1-T2":       (48.7262, 2.3652),
    "Robinson":                  (48.7762, 2.2930),
    "Cergy Le Haut":             (49.0500, 2.0650),
}
