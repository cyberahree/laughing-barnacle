from pathlib import Path

import argparse
import re

PATTERN = re.compile(r"[a-zA-Z0-9!?_-]+\{.*\}")
# r"^[a-zA-Z0-9!?_-]+\{.*\}$"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def find_objects(file: Path, flag_limit: int, chunk_size: int = 1024 * 1024) -> list[str]:
    matches = []
    buffer = ""
    
    with file.open("r", encoding="utf-8", errors="ignore") as f:
        while True:
            chunk = f.read(chunk_size)

            if not chunk:
                break
            
            text = buffer + chunk

            chunk_matches = PATTERN.findall(text)
            matches.extend(chunk_matches)
            
            # keep the last 1000 characters as buffer for next iteration
            # to handle patterns that might span across chunks
            if len(text) > 1000:
                buffer = text[-1000:]
            else:
                buffer = text
        
        if buffer:
            final_matches = PATTERN.findall(buffer)
            matches.extend(final_matches)

    unique_matches = []

    for match in matches:
        match = match.strip()

        size = len(match)

        if size > flag_limit:
            print(f"{bcolors.WARNING}Skipping {match} (length: {size}, exceeds limit: {flag_limit}){bcolors.ENDC}")
            continue

        if PATTERN.match(match) and match not in unique_matches:
            unique_matches.append(match)

    return unique_matches

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find flag-like strings in a provided file")
    parser.add_argument("file", type=Path, help="The file to search")
    parser.add_argument("--output", type=str, help="Output file to save results (optional)", default=None)
    parser.add_argument("--flag-max-length", type=int, default=64, help="Maximum length of flag-like strings to consider (default: 64)")

    args = parser.parse_args()

    objects = find_objects(args.file, args.flag_max_length)

    if not objects:
        print(f"{bcolors.FAIL}No flag-like strings found in {args.file}{bcolors.ENDC}")
        exit()

    colors = [bcolors.OKGREEN, bcolors.OKBLUE, bcolors.OKCYAN, bcolors.WARNING, bcolors.HEADER]
    
    for i, obj in enumerate(objects):
        color = colors[i % len(colors)]
        print(f"{color}{obj}{bcolors.ENDC}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            for obj in objects:
                f.write(f"{obj}\n")

        print(f"{bcolors.OKGREEN}Results saved to {args.output}{bcolors.ENDC} ({len(objects)} results)")
