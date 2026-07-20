"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    }

    hip_hop_prefs = {
        "favorite_genre": "hip hop",
        "favorite_mood": "intense",
        "target_energy": 0.75,
        "likes_acoustic": False,
    }

    classical_prefs = {
        "favorite_genre": "classical",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": True,
    }

    pop_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "chill",
        "target_energy": 0.4,
        "likes_acoustic": False,
    }

    # Adversarial / edge-case profiles: designed to probe whether the
    # additive scoring model behaves sensibly when preferences conflict
    # with each other or with the song catalog, rather than to represent
    # a plausible real user.
    # Tests whether a binary mood match can outweigh a large energy
    # mismatch (or vice versa) when the two terms disagree.
    contradictory_energy_mood_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "sad",
        "target_energy": 0.9,
        "likes_acoustic": True,
    }

    # Tests that genre_similarity degrades to 0.0 for every song (rather
    # than erroring) when favorite_genre matches nothing in the catalog.
    genre_not_in_catalog_prefs = {
        "favorite_genre": "reggaeton",
        "favorite_mood": "chill",
        "target_energy": 0.5,
        "likes_acoustic": False,
    }

    # Tests the rare real-world combo of high target_energy with
    # likes_acoustic=True, where the acoustic bonus and energy term
    # tend to reward opposite kinds of songs.
    high_energy_acoustic_prefs = {
        "favorite_genre": "classical",
        "favorite_mood": "chill",
        "target_energy": 0.95,
        "likes_acoustic": True,
    }

    # Tests the floor: every term mismatches every song, so this checks
    # that recommend_songs still returns k results with coherent (empty)
    # explanations instead of failing.
    all_mismatch_prefs = {
        "favorite_genre": "reggaeton",
        "favorite_mood": "furious",
        "target_energy": 0.5,
        "likes_acoustic": False,
    }

    profiles = [
        ("Default (lofi/chill)", user_prefs),
        ("Hip hop", hip_hop_prefs),
        ("Classical", classical_prefs),
        ("Pop", pop_prefs),
        ("Contradictory energy/mood", contradictory_energy_mood_prefs),
        ("Genre not in catalog", genre_not_in_catalog_prefs),
        ("High-energy acoustic", high_energy_acoustic_prefs),
        ("All-mismatch", all_mismatch_prefs),
    ]

    for label, prefs in profiles:
        recommendations = recommend_songs(prefs, songs, k=5)

        print(f"\n=== {label} ===")
        print("\nTop recommendations:\n")
        for rec in recommendations:
            # You decide the structure of each returned item.
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
