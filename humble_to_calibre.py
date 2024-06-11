#!/usr/bin/env python3
import shutil
import argparse
from pathlib import Path

DEFAUT_DIRS = {
    Path.home() / 'Downloads' / 'Books',
    Path.home() / 'Downloads' / 'Humble Bundle',
    Path.home() / 'Downloads' / 'humblebundle',
}

BOOK_EXTENSIONS = {
    '.pdf',
    '.epub',
    '.mobi',
    '.azw3',
    '.rtf',
}


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
                    prog='Humble Organizer',
                    description='Program that takes a list of directories, searches for books in those directories, and tries to put files of the same book that are in different formats into the same directory.',
                    epilog='Text at the bottom of help')
    
    parser.add_argument('directories', metavar='dirs', type=str, nargs='*', help='Directories to search for books')

    return parser.parse_args()

def main():
    args = parse_args()

    dirs = DEFAUT_DIRS | set(map(lambda x: Path(x), args.directories))
    dirs = set([d for d in dirs if d.is_dir()])

    for folder in dirs:
        books = {}

        for f in folder.iterdir():
            if f.is_dir() or f.suffix not in BOOK_EXTENSIONS:
                continue
            
            book_name = f.stem

            if book_name in books:
                books[book_name].append(f)
            else:
                books[book_name] = [ f ]
        
        for book_name in books:
            d = folder.joinpath(book_name)
            d.mkdir(exist_ok=True)
            print(f"Created {d}")
        
        for book_name,book_files in books.items():
            for book_file in book_files:
                dst = folder.joinpath(book_name, book_file.name)
                shutil.move(book_file, dst)
                print(f"Moved {book_file} to {dst}")

if __name__ == '__main__':
    main()
