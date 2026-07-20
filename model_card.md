# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**IKnowYou**

---

## 2. Intended Use  

This is a classroom exploration built for the ai110 Module 3 assignment — it is not intended for real users. Its purpose is to simulate, at a small scale, how a content-based music recommender turns song attributes and a stated "taste profile" into a ranked list of suggestions, so the underlying mechanics (scoring, ranking, explanation) can be inspected and reasoned about.

It generates a top-`k` ranked list of songs from the 18-song catalog in `data/songs.csv`, along with a short explanation string per recommendation (e.g. "Matches favorite genre 'lofi'; Energy is close to target"). It assumes the user has already stated explicit preferences up front via a `UserProfile` — `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic` — rather than inferring preferences from listening history or behavior. There is no collaborative-filtering component and no concept of other users; each recommendation is generated purely from one profile against the static catalog.

---

## 3. How the Model Works  

Each song has a `genre`, `mood`, `energy` (0–1), `tempo_bpm`, `valence`, `danceability`, and `acousticness` (0–1). A user's taste profile states a favorite genre, a favorite mood, a target energy level, and whether they like acoustic music. Of these song attributes, only `genre`, `mood`, `energy`, and `acousticness` are actually used for scoring — `tempo_bpm`, `valence`, and `danceability` are stored on each song but currently ignored, because the `UserProfile` has no corresponding preference for them.

To score a song, the model adds up four ingredients, each counted equally:

- A full point if the song's genre exactly matches the user's favorite genre, otherwise nothing.
- A full point if the song's mood exactly matches the user's favorite mood, otherwise nothing.
- A partial point based on how close the song's energy is to the user's target energy — the closer, the more points, with no points lost for an exact match and points lost gradually as the gap grows.
- A partial point based on acousticness — if the user likes acoustic music, a more acoustic song scores higher; if not, a less acoustic song scores higher.

The four points are added together into one total score. Songs are then sorted from highest to lowest score, and the top few are returned as the recommendations, each with a plain-language explanation of which ingredients contributed.

This is the starter logic as implemented — the genre and mood matching is a strict yes/no match rather than a graded similarity (e.g., "indie pop" gets no credit toward a "pop" preference, even though it's a close relative).

---

## 4. Data  

The catalog (`data/songs.csv`) contains 18 songs. Each song lists an id, title, artist, genre, mood, energy, tempo (BPM), valence, danceability, and acousticness.

Genres repeat unevenly: `lofi` (3 songs), `pop` (2 songs), and one song each in `rock`, `ambient`, `jazz`, `synthwave`, `indie pop`, `folk`, `hip hop`, `r&b`, `metal`, `reggae`, `edm`, `classical`, and `blues` (15 distinct genres total).

Moods are similarly uneven: `chill` (3 songs), `happy` and `intense` (2 songs each), and one song each in `relaxed`, `moody`, `focused`, `nostalgic`, `triumphant`, `romantic`, `anxious`, `playful`, `euphoric`, `melancholy`, and `longing` (14 distinct moods total).

No data was added to or removed from the starter catalog. Because most genres and moods appear only once, the catalog can't really represent within-genre or within-mood variety (e.g., there's only one `hip hop` song, so the model can't distinguish "the right kind of hip hop" from "hip hop in general"). There's also no listening-history, popularity, or lyrical/language data — the dataset only captures audio-feature-style attributes and single-label genre/mood tags.

---

## 5. Strengths  

The scoring works most cleanly for profiles where all four preference terms (genre, mood, energy, acousticness) point in the same direction — e.g. the default lofi/chill profile, where the catalog's three `lofi`/`chill` songs (Library Rain, Midnight Coding, Focus Flow) score highest and stay clustered at the top for a sensible reason (agreement across all four terms), not because one term is dominating by accident.

The energy-similarity term (inverse distance rather than exact match) does what it's meant to do: it rewards near-misses instead of penalizing them the same as far misses, which is visible in the adversarial "genre not in catalog" test, where songs with close energy and mood match still surfaced sensibly even with zero genre credit.

---

## 6. Limitations and Bias 
- genre_similarity and mood_similarity are binary (1.0 or 0.0) — a song in the user's favorite genre gets a full point no matter how well it otherwise fits, while every other genre gets zero credit regardless of similarity. Since recommend_songs re-ranks by this score every call, users are pushed deeper into their stated genre/mood with each recommendation cycle and rarely see adjacent genres that might overlap in energy/valence/acousticness. This is the single biggest bubble driver — there's no notion of genre adjacency (e.g., "indie folk" vs "folk").
- The system does not consider tempo_bpm, valence, or danceability. Specifically, because the `UserProfile` class only had a `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`, I decided to keep the system within those confines. Also, the system doesn't have previous usage information that could make for more effective recommendation strategies. 

---

## 7. Evaluation  

I ran `src/main.py` against eight user profiles: four intended as plausible real-world profiles (default lofi/chill, hip hop, classical, pop) and four adversarial profiles specifically designed to stress-test the additive scoring model (contradictory energy/mood, genre not in catalog, high-energy acoustic, all-mismatch — see `src/main.py` and README "Adversarial Profiles"). For each, I checked that `recommend_songs` still returned `k` results with coherent explanations, even when every term mismatched (the all-mismatch case), and that `genre_similarity` correctly degraded to 0.0 for every song rather than erroring when the favorite genre wasn't in the catalog.

I also ran a small weight-sensitivity experiment (doubling the energy weight, halving the genre weight) across all eight profiles and recorded how the top-3 rankings shifted — documented in README "Experiments I Tried."

What surprised me was how much the acoustic_bonus term alone could carry a recommendation to the top of the list — in several adversarial profiles (e.g. "contradictory energy/mood," "genre not in catalog"), the top-ranked songs won mostly on high acousticness rather than genre or mood match, showing that with all weights equal, a single continuous term can dominate over two binary terms when both binary terms return 0.

---

## 8. Future Work  

The clearest next improvement would be replacing the binary genre and mood matching with a graded similarity scale (e.g. a genre-adjacency table or embedding-based distance) instead of exact-match-or-nothing. Right now "indie pop" gets the same score (0.0) against a "pop" preference as "metal" does, even though one is clearly a closer relative — this is the main driver of the genre bubble noted in Section 6. A graded scale would let adjacent genres/moods earn partial credit, which should reduce over-narrowing across repeated recommendation cycles without requiring collaborative or usage-history data.

---

## 9. Personal Reflection  

Building this gave me a much better under-the-hood sense of how a recommender like Spotify's actually works. I like the idea of mixing content-based filtering (matching songs to stated attributes, like this project does) with collaborative filtering (recommending based on what similar users liked) — Spotify does both, which is part of why it's able to suggest things I wouldn't have picked myself but end up enjoying, since I like to explore outside what I normally listen to. Working through this project's additive scoring model made concrete for me why a purely content-based system (like this one) tends to narrow toward exactly what you already said you like, and helped me understand at a much more concrete level how bandit algorithms and collaborative filtering complement content-based scoring to produce the kind of exploratory recommendations I notice and appreciate in Spotify.
