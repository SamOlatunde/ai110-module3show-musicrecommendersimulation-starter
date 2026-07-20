import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

  
class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.

    Args:
        csv_path: Path to a CSV file with columns matching the Song fields
            (id, title, artist, genre, mood, energy, tempo_bpm, valence,
            danceability, acousticness).

    Returns:
        A list of dictionaries, one per row, with numeric fields converted
        to int/float.

    Raises:
        ValueError: If a row is missing a required column or a numeric
            field cannot be parsed.
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Uses an additive model: score = genre_similarity + mood_similarity +
    energy_similarity + acoustic_bonus, each weighted equally (weight = 1).
    See README.md "How The System Works" for the rationale behind each term.

    Args:
        user_prefs: Dict with keys favorite_genre, favorite_mood,
            target_energy, likes_acoustic.
        song: Dict with keys genre, mood, energy, acousticness.

    Returns:
        A tuple of (total score, list of human-readable reason strings for
        each term that contributed positively).

    Required by recommend_songs() and src/main.py
    """
    reasons = []

    genre_similarity = 1.0 if song["genre"] == user_prefs["favorite_genre"] else 0.0
    if genre_similarity:
        reasons.append(f"Matches favorite genre '{user_prefs['favorite_genre']}'")

    mood_similarity = 1.0 if song["mood"] == user_prefs["favorite_mood"] else 0.0
    if mood_similarity:
        reasons.append(f"Matches favorite mood '{user_prefs['favorite_mood']}'")

    energy_similarity = 1 - abs(song["energy"] - user_prefs["target_energy"])
    if energy_similarity >= 0.8:
        reasons.append("Energy is close to target")

    if user_prefs["likes_acoustic"]:
        acoustic_bonus = song["acousticness"]
        if acoustic_bonus >= 0.5:
            reasons.append("High acousticness matches preference for acoustic music")
    else:
        acoustic_bonus = 1 - song["acousticness"]
        if acoustic_bonus >= 0.5:
            reasons.append("Low acousticness matches preference for non-acoustic music")

    score = genre_similarity + mood_similarity + energy_similarity + acoustic_bonus
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.

    Scores every song with score_song, then ranks by score descending
    and returns the top k.

    Args:
        user_prefs: Dict of user preferences (see score_song).
        songs: List of song dicts (see score_song).
        k: Maximum number of recommendations to return.

    Returns:
        A list of (song_dict, score, explanation) tuples, ordered from
        highest score to lowest, truncated to k entries.

    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    ranked = sorted(scored, key=lambda entry: entry[1], reverse=True)
    return ranked[:k]
