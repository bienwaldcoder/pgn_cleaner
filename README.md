# PGN Cleaner & Merger

A Python utility designed to process chess PGN (Portable Game Notation) files. It merges multiple games into a single variation tree, removes comments, and filters out invalid or incomplete games.

## Features
* **Merge Games:** Combines all games from an input file into one master game with a nested variation tree.
* **Clean PGN:** Automatically removes all comments and annotations for a clean output.
* **Smart Filtering:** * Skips games with fewer than 2 plies.
    * Ignores games that do not start from the standard chess starting position (e.g., tactical puzzles).
    * Handles encoding issues and skips corrupted games or illegal moves.
* **Statistics:** Provides real-time feedback on the number of games processed.

## Prerequisites
You need Python installed on your system along with the `python-chess` library.

### Installation
Install the required dependency via pip:
```bash
pip install python-chess```

### Usage
Run the script from your terminal by providing the path to your PGN file:
```bash
python pgn_cleaner.py your_games.pgn```

### License
This project is licensed under the GNU General Public License v3.0 (GPLv3). See the LICENSE file for details.

### Disclaimer
This tool is intended for personal use and study. Ensure you have the rights to any PGN data you process.
