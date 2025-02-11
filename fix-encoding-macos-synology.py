#!/usr/bin/env python3
import os
import unicodedata
import sys
import argparse

def remove_accents(input_str):
    return ''.join(c for c in unicodedata.normalize('NFKD', input_str) if unicodedata.category(c) != 'Mn')


def check_and_fix_normalization(folder_path, fix=False):
    """
    Scans a folder for filenames with inconsistent NFC/NFD normalization and optionally fixes them.

    :param folder_path: Path to the folder to scan.
    :param fix: Boolean flag to fix filenames if inconsistencies are found.
    """
    print(f"Scanning folder: {folder_path}")
    problematic_files = []

    for root, dirs, files in os.walk(folder_path):
        for name in files + dirs:
            full_path = os.path.join(root, name)
            nfc_name = unicodedata.normalize('NFC', name)
            ascii_name = remove_accents(name)
            ascii_name = ascii_name.encode('ascii', 'ignore').decode()  # Ensure it's pure ASCII
            if name != nfc_name:
                problematic_files.append(full_path)
                if fix:
                    new_path = os.path.join(root, ascii_name)
                    try:
                        os.rename(full_path, new_path)
                        print(f"Fixed: {full_path} -> {new_path}")
                    except OSError as e:
                        print(f"Error renaming {full_path}: {e}")

    if not problematic_files:
        print("No problematic filenames detected.")
    else:
        print("\n\n----\nSummary of problematic files:")
        print("\n".join(problematic_files))
        print(f"\n\n{len(problematic_files)} filenames detected\n")
        if not fix:
            print("\nRun the script with the --fix flag to correct these filenames.")
        else:
            print("\nAll inconsistencies fixed.")


def main():
    parser = argparse.ArgumentParser(description="Check and optionally fix NFC/NFD normalization issues in filenames.")
    parser.add_argument("folder", type=str, help="Path to the folder to scan")
    parser.add_argument("--fix", action="store_true", help="Fix filenames with inconsistent normalization")
    args = parser.parse_args()

    check_and_fix_normalization(args.folder, args.fix)

if __name__ == "__main__":
    main()
