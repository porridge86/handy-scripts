# Overview

This project provides a simple Bash script to automatically create empty `.md` files based on a list of names stored in a text file (`timeplan.txt`).
Each line in the text file will be used as the filename.

## Motivation

I created this script because I wanted a simple way to automatically generate empty `.md` files from a list of names stored in a text file.
Instead of manually creating each file, the script reads the list and produces all the files in one step.
This saves time and ensures consistency in file naming.

## Requirements

- `timeplan.txt` containing the list of names (one per line).

## Folder Structure

The script and the text file should be placed in the same folder for simplicity:

```
project/
├── make_md_files.sh
└── timeplan.txt
```

- `make_md_files.sh` → The Bash script that reads the text file and creates .md files.
- timeplan.txt → The list of names (each line will become a filename).

## Usage

1. Save the Bash script as `make_md_files.sh` in the same folder as `timeplan.txt`.
2. Make the script executable;`chmod +x make_md_files.sh`
3. Run the script: `./make_md_files.sh`

## Example

If timeplan.txt contains:

```
01-01 Forelesning-01
01-02 Forelesning-02
01-03 Øving
```

After running the script, the folder will contain:

```
01-01 Forelesning-01.md
01-02 Forelesning-02.md
01-03 Øving.md
```
