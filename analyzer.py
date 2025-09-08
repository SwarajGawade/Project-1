#!/usr/bin/env python3
"""
Password Strength Analyzer & Custom Wordlist Generator
- analyze: score a password using zxcvbn
- gen-wordlist: generate attack-style wordlists from user-provided hints
"""
import argparse, itertools, re, sys, getpass, datetime
from typing import Iterable, List, Set
try:
    from zxcvbn import zxcvbn
except Exception as e:
    print("[-] zxcvbn is required. Install with: pip install zxcvbn", file=sys.stderr)
    raise

LEET_MAP = {
    "a":"4", "b":"8", "e":"3", "g":"9", "i":"1", "l":"1", "o":"0", "s":"5", "t":"7", "z":"2"
}

COMMON_SUFFIXES = ["!", "@", "#", "$", "123", "1234", "12345", "1", "01", "007", "2024", "2025"]
COMMON_PREFIXES = ["!", "@", "#", "$"]

def l33tify(word: str) -> Set[str]:
    word = word.lower()
    variants = {word}
    # per-character replacement
    chars = list(word)
    options = []
    for c in chars:
        repl = LEET_MAP.get(c, None)
        if repl:
            options.append([c, repl])
        else:
            options.append([c])
    # combine choices
    for combo in itertools.product(*options):
        variants.add("".join(combo))
    # case variants
    variants |= {word.capitalize(), word.upper(), word.title()}
    return variants

def year_range(start:int=1990, end:int=datetime.datetime.now().year+1) -> List[str]:
    return [str(y) for y in range(start, end+1)]

def split_tokens(s: str) -> List[str]:
    parts = re.split(r"[,\s/_\-\.]+", s.strip())
    return [p for p in parts if p]

def mix(words: Iterable[str]) -> Set[str]:
    words = [w for w in words if w]
    out = set()
    # single words with l33t
    for w in words:
        out |= l33tify(w)
    # combos 2
    for a, b in itertools.permutations(words, 2):
        out.add(a+b); out.add(b+a)
    # add separators
    seps = ["", ".", "_", "-", "@"]
    for a, b in itertools.permutations(words, 2):
        for s in seps:
            out.add(a+s+b)
    return out

def sprinkle(words: Iterable[str]) -> Set[str]:
    out = set()
    for w in words:
        for suf in COMMON_SUFFIXES:
            out.add(w + suf)
        for pre in COMMON_PREFIXES:
            out.add(pre + w)
    return out

def gen_wordlist(name:str="", pet:str="", dob:str="", keywords:str="", extra_years:str="") -> List[str]:
    tokens = []
    tokens += split_tokens(name)
    tokens += split_tokens(pet)
    tokens += split_tokens(keywords)
    # derive from dob
    dob = dob.strip()
    if dob:
        ds = re.split(r"[^\d]", dob)
        ds = [d for d in ds if d]
        tokens += ds
        # common year parts like 1999, 99
        for d in ds:
            if len(d) == 4:
                tokens.append(d[-2:])
    # base pool
    base = set(tokens)
    # add year range
    years = set(year_range(1990, datetime.datetime.now().year+1))
    if extra_years:
        for y in split_tokens(extra_years):
            if y.isdigit():
                years.add(y)
    # combinations
    pool = mix(base)
    pool |= sprinkle(pool)
    # append years
    with_years = set(pool)
    for w in list(pool):
        for y in sorted(years):
            with_years.add(f"{w}{y}")
            with_years.add(f"{y}{w}")
    # ensure minimal essentials
    with_years |= base
    return sorted(with_years)

def cmd_analyze():
    print("[*] Password will be read securely (no echo).")
    pwd = getpass.getpass("Enter password: ")
    result = zxcvbn(pwd)
    print("\n=== Analysis ===")
    print(f"Score (0-4): {result['score']}")
    try:
        crack = result.get('crack_times_display', {})
        if crack:
            for k, v in crack.items():
                print(f"{k}: {v}")
    except Exception:
        pass
    fb = result.get("feedback", {})
    warn = fb.get("warning")
    sugg = fb.get("suggestions", [])
    if warn:
        print(f"\nWarning: {warn}")
    if sugg:
        print("Suggestions:")
        for s in sugg:
            print(f"- {s}")

def cmd_gen(args):
    words = gen_wordlist(args.name, args.pet, args.dob, args.keywords, args.years)
    # cap size
    if args.max and len(words) > args.max:
        words = words[:args.max]
    with open(args.output, "w", encoding="utf-8") as f:
        for w in words:
            f.write(w + "\n")
    print(f"[+] Generated {len(words)} words -> {args.output}")

def main():
    p = argparse.ArgumentParser(description="Password Strength Analyzer & Wordlist Generator")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze", help="Analyze a password using zxcvbn")
    a.set_defaults(func=lambda args: cmd_analyze())

    g = sub.add_parser("gen-wordlist", help="Generate a custom wordlist based on hints")
    g.add_argument("--name", default="", help="Name(s) or nickname(s)")
    g.add_argument("--pet", default="", help="Pet name(s)")
    g.add_argument("--dob", default="", help="Date of birth like 2001-10-25 or 25/10/2001")
    g.add_argument("--keywords", default="", help="Comma/space separated keywords (company, team, etc.)")
    g.add_argument("--years", default="", help="Extra years to include (e.g., 1995,2000,2025)")
    g.add_argument("--max", type=int, default=50000, help="Cap the wordlist size (default 50k)")
    g.add_argument("-o", "--output", default="wordlist.txt", help="Output file path")
    g.set_defaults(func=cmd_gen)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
