# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

**Song features used:** `genre`, `mood`, `energy`, and `acousticness`. These four were chosen because each has a directly corresponding preference on `UserProfile` — `tempo_bpm`, `valence`, and `danceability` are stored on `Song` but not currently used for scoring, since there's no matching user preference for them yet.

**UserProfile stores:** `favorite_genre`, `favorite_mood`, `target_energy` (a float the recommender compares songs against), and `likes_acoustic` (a boolean).

**Taste profile used for testing:**

```
favorite_genre: lofi
favorite_mood: chill
target_energy: 0.35
likes_acoustic: true
```

All four preferences point the same direction (calm, low-energy, acoustic-leaning), so the ranking it produces reflects genuine agreement across genre, mood, energy, and acousticness rather than one mismatched term accidentally dominating the score.

**How the score is computed:** `score_song` uses an additive model — a weighted sum of four similarity terms, one per feature, each weighted equally (weight = 1):

```
score = genre_similarity + mood_similarity + energy_similarity + acoustic_bonus
```

- **Genre similarity** — binary match: `1.0` if `song.genre == user.favorite_genre`, else `0.0`.
- **Mood similarity** — binary match: `1.0` if `song.mood == user.favorite_mood`, else `0.0`.
- **Energy similarity** — inverse distance: `1 - abs(song.energy - user.target_energy)`. Since both values are on a 0–1 scale, this rewards songs whose energy is close to the user's target and penalizes songs that are far from it, rather than requiring an exact match.
- **Acoustic bonus** — a conditional term based on `likes_acoustic`: if the user likes acoustic music, the bonus favors higher `acousticness`; if not, it favors lower `acousticness`.

Binary match was chosen over a hand-curated similarity table for genre/mood: it avoids maintaining and re-justifying pairwise (or cluster) values every time a new genre or mood is added to `data/songs.csv`, at the cost of not distinguishing "close but not exact" matches (e.g. `indie pop` scores the same as `rock` against a `pop`-loving user — both get `0.0`).

**Choosing recommendations:** the scoring rule and ranking rule are kept separate. `score_song` computes one score per song; `recommend_songs` (and `Recommender.recommend`) then sorts all songs by that score in descending order and returns the top `k`.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Loaded songs: 18

Top recommendations:

Library Rain - Score: 3.86
Because: Matches favorite genre 'lofi'; Matches favorite mood 'chill'; Energy is close to target; High acousticness matches preference for acoustic music

Midnight Coding - Score: 3.64
Because: Matches favorite genre 'lofi'; Matches favorite mood 'chill'; Energy is close to target; High acousticness matches preference for acoustic music

Spacewalk Thoughts - Score: 2.85
Because: Matches favorite mood 'chill'; Energy is close to target; High acousticness matches preference for acoustic music

Focus Flow - Score: 2.73
Because: Matches favorite genre 'lofi'; Energy is close to target; High acousticness matches preference for acoustic music

Coffee Shop Stories - Score: 1.87
Because: Energy is close to target; High acousticness matches preference for acoustic music
```


---

## Adversarial Profiles
```
Loaded songs: 18

=== Contradictory energy/mood ===

Top recommendations:

Library Rain - Score: 2.31
Because: Matches favorite genre 'lofi'; High acousticness matches preference for acoustic music

Focus Flow - Score: 2.28
Because: Matches favorite genre 'lofi'; High acousticness matches preference for acoustic music

Midnight Coding - Score: 2.23
Because: Matches favorite genre 'lofi'; High acousticness matches preference for acoustic music

Coffee Shop Stories - Score: 1.36
Because: High acousticness matches preference for acoustic music

Spacewalk Thoughts - Score: 1.30
Because: High acousticness matches preference for acoustic music


=== Genre not in catalog ===

Top recommendations:

Midnight Coding - Score: 2.21
Because: Matches favorite mood 'chill'; Energy is close to target

Library Rain - Score: 1.99
Because: Matches favorite mood 'chill'; Energy is close to target

Spacewalk Thoughts - Score: 1.86
Because: Matches favorite mood 'chill'

Velvet Whisper - Score: 1.65
Because: Energy is close to target; Low acousticness matches preference for non-acoustic music

Concrete Kingdom - Score: 1.62
Because: Low acousticness matches preference for non-acoustic music


=== High-energy acoustic ===

Top recommendations:

Library Rain - Score: 2.26
Because: Matches favorite mood 'chill'; High acousticness matches preference for acoustic music

Spacewalk Thoughts - Score: 2.25
Because: Matches favorite mood 'chill'; High acousticness matches preference for acoustic music

Etude for Rain - Score: 2.25
Because: Matches favorite genre 'classical'; High acousticness matches preference for acoustic music

Midnight Coding - Score: 2.18
Because: Matches favorite mood 'chill'; High acousticness matches preference for acoustic music

Coffee Shop Stories - Score: 1.31
Because: High acousticness matches preference for acoustic music


=== All-mismatch ===

Top recommendations:

Velvet Whisper - Score: 1.65
Because: Energy is close to target; Low acousticness matches preference for non-acoustic music

Concrete Kingdom - Score: 1.62
Because: Low acousticness matches preference for non-acoustic music

Warehouse Pulse - Score: 1.57
Because: Low acousticness matches preference for non-acoustic music

Night Drive Loop - Score: 1.53
Because: Low acousticness matches preference for non-acoustic music

Gym Hero - Score: 1.52
Because: Low acousticness matches preference for non-acoustic music
```

## Experiments I Tried

The only experiemnt I tried was doubling the importance of energy and halfing the importance of genre. I created a temporary branch and ran main.py on all profiles. Here's a side by side comparison of the baseline and changed weights:

| Profile | Baseline top 3 (weights = 1) | Energy x2 / Genre x0.5 top 3 | What changed |
|---|---|---|---|
| Default (lofi/chill) | Library Rain, Midnight Coding, Spacewalk Thoughts | Library Rain, Midnight Coding, Spacewalk Thoughts | Same order — all four terms already agreed, so re-weighting just changed the scores, not the ranking. |
| Hip hop | Concrete Kingdom (genre match), Gym Hero, Storm Runner | Gym Hero, Storm Runner, Concrete Kingdom (genre match) | The genre match dropped from 1st to 3rd — mood + close energy now outweighs an exact genre match. |
| Classical | Etude for Rain (genre match), Storm Runner, Gym Hero | Storm Runner, Gym Hero, Etude for Rain (genre match) | Same effect: genre match fell from 1st to 3rd, edged out by songs with closer energy. |
| Pop | Gym Hero (genre match), Sunrise City (genre match), Midnight Coding | Midnight Coding, Library Rain, Spacewalk Thoughts | Both genre matches fell out of the top 3 entirely; energy-close songs took over. |
| Contradictory energy/mood | Library Rain (genre match), Focus Flow (genre match), Midnight Coding (genre match) | Focus Flow (genre match), Library Rain (genre match), Midnight Coding (genre match) | Top 3 stayed genre matches (lofi still had reasonable energy fit), but 4th/5th place swapped in higher-energy songs (Storm Runner, Rooftop Lights) that weren't close before. |
| Genre not in catalog | Midnight Coding, Library Rain, Spacewalk Thoughts | Midnight Coding, Library Rain, Spacewalk Thoughts | No change to top 3 — genre_similarity is 0 for every song here either way, so only the (irrelevant) genre weight changed, not the ranking. |
| High-energy acoustic | Library Rain, Spacewalk Thoughts, Etude for Rain (genre match) | Library Rain, Midnight Coding, Spacewalk Thoughts | Etude for Rain (the one genre match) dropped out of the top 3, replaced by a closer-energy song. |
| All-mismatch | Velvet Whisper, Concrete Kingdom, Warehouse Pulse | Velvet Whisper, Sunset Skank, Crossroads Blues | Genre is 0 for every song regardless of weight, so the reshuffle here is purely from the doubled energy term rewarding closer energy matches more strongly. |

**Takeaway:** halving the genre weight and doubling the energy weight consistently demotes exact genre matches whenever a non-matching song has closer energy — genre stops being able to "win" on its own and has to be backed up by energy or mood agreement. Profiles where genre never matched anything in the catalog (Genre not in catalog, All-mismatch) show that the genre weight change itself did nothing there; any reshuffling in those cases came entirely from the energy weight.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---





