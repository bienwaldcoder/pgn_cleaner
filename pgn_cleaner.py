"""
Copyright (c) 2024 BienwaldCoder

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
"""

import os
import chess.pgn
import sys

def process_pgn(input_filename):
    """
    Reads a PGN file, cleans it, and asks for merge and comment preferences.
    """
    # 1. Ask for merge mode
    mode = input("Do you want to merge the games into one tree? (y/n): ").lower()
    do_merge = mode == 'y'

    # 2. Ask for comments (only if not merging)
    keep_comments = False
    if not do_merge:
        comm_mode = input("Do you want to keep comments and annotations? (y/n): ").lower()
        keep_comments = comm_mode == 'y'

    # Generate output filename
    base, ext = os.path.splitext(os.path.basename(input_filename))
    suffix = "_merged" if do_merge else "_cleaned"
    output_filename = f"{base}{suffix}.pgn"

    games_processed = 0

    print(f"Processing: {input_filename}")
    print(f"Mode: {'Merge' if do_merge else 'Clean Only'}")
    print(f"Keep Comments: {keep_comments if not do_merge else 'False (Auto-removed for Merge)'}")

    master_game = None
    if do_merge:
        master_game = chess.pgn.Game()
        master_game.headers["Event"] = "Merged Games"
        master_game.headers["White"] = "Various"
        master_game.headers["Black"] = "Various"
        master_game.headers["Result"] = "*"

    try:
        with open(input_filename, "r", encoding="utf-8", errors="replace") as pgn_file:
            out_file = open(output_filename, "w", encoding="utf-8") if not do_merge else None

            while True:
                try:
                    game = chess.pgn.read_game(pgn_file)
                except ValueError:
                    continue

                if game is None:
                    break

                # Filter: Ignore games with fewer than 2 plies or errors
                if game.errors or game.end().ply() < 2:
                    continue

                # Filter: Only starting position
                if game.board().fen() != chess.STARTING_FEN:
                    continue

                if do_merge:
                    # MERGE LOGIC
                    node = master_game
                    for move_node in game.mainline():
                        move = move_node.move
                        if node.has_variation(move):
                            node = node.variation(move)
                        else:
                            node = node.add_variation(move)
                else:
                    # CLEAN LOGIC
                    exporter = chess.pgn.FileExporter(
                        out_file,
                        headers=True,
                        variations=True,
                        comments=keep_comments
                    )
                    game.accept(exporter)
                    out_file.write("\n\n")

                games_processed += 1
                if games_processed % 100 == 0:
                    print(f"  {games_processed} games processed...", end='\r')

        if do_merge:
            print(f"\nWriting merged game tree...")
            with open(output_filename, "w", encoding="utf-8") as out_file_merge:
                exporter = chess.pgn.FileExporter(out_file_merge, headers=True, variations=True, comments=False)
                master_game.accept(exporter)
        elif out_file:
            out_file.close()

        print(f"\nSuccess! {games_processed} games processed.")
        print(f"File saved to: {os.path.abspath(output_filename)}")

    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pgn_cleaner.py <file.pgn>")
    else:
        input_file = sys.argv[1]
        process_pgn(input_file)
