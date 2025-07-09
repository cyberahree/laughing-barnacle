# laughing-barnacle
glorified grep &amp; regex

a simple script for finding flag-like strings in files, particularly useful for challenges where you have no idea what the flag format is (literally never)
- this script follows the format of prefix{flag_content}, however can be changed by updating the regex pattern used within
- utilises chunks to process large files in a more efficient manner (1MB at any time)
- clears duplicate matches
- flag size limiting
- exportable results

this uses no additional dependencies beyond python's standard library

## valid matches
- `flag{this_is_a_flag}`
- `CTF{example_flag_here}`
- `challenge{s0m3_t3xt}`
- `someCTF{flag_content}`
- `-{!g0#AѰn6@tXe'z[8ȏ&|@kl 5 lXoLWb}`

## usage
```bash
python bruteflag.py <file_path> [options]
```

options:
- `--output <filename>`: Save results to a specified file (optional)
- `--flag-max-length <number>`: Maximum length of flag-like strings to consider (default: 64)

examples:
```bash
# Basic scan
python bruteflag.py flags.txt

# Scan with custom length limit
python bruteflag.py flags.txt --flag-max-length 100

# Scan and save results to file
python bruteflag.py flags.txt --output results.txt

# Scan with custom length and output file
python bruteflag.py flags.txt --flag-max-length 128 --output my_flags.txt
```
