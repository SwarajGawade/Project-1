# Password Strength Analyzer & Custom Wordlist Generator

A beginner-friendly **Python CLI** that:
- Analyzes password strength with **zxcvbn** (score 0–4, crack-time estimates, feedback).
- Generates a **custom attack-style wordlist** using names, pets, DOB, and keywords (with leetspeak, year appends, and combos).

## ✨ Features
- `analyze` subcommand: secure password prompt (no echo), detailed feedback.
- `gen-wordlist` subcommand: builds smart permutations and appends common years/suffixes.
- Output capped with `--max` to avoid huge files.

## 🧰 Requirements
```bash
python3 -m pip install zxcvbn nltk
```

> NLTK is listed for the original brief but is **not required** by this implementation. You can remove it from requirements if you like.

## 🚀 Usage
Clone/extract this folder, then:
```bash
python3 analyzer.py analyze

python3 analyzer.py gen-wordlist \
  --name "swaraj" \
  --pet "tiger" \
  --dob "2001-10-25" \
  --keywords "india,football,linux" \
  --years "2018,2024,2025" \
  --max 30000 \
  -o wordlist.txt
```

- `analyze` prints score and suggestions.
- `gen-wordlist` writes `wordlist.txt` with smart variants.

## 📂 Deliverables
- `analyzer.py` (CLI).
- Generated `wordlist.txt` (exportable for cracking tools).

## 🧪 Demo
```bash
# Strength check
python3 analyzer.py analyze

# Wordlist generation
python3 analyzer.py gen-wordlist --name "alex" --pet "milo" --dob "1999-07-01" -o mylist.txt
head mylist.txt
wc -l mylist.txt
```

