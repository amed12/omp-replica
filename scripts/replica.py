#!/usr/bin/env python3
"""Restore allowlisted, SHA-256-verified files; never replace user files."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def no_symlinks(path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError('Symlink is not an installation target: ' + str(part))


def restore(repo, home, apply=False, verify=False):
    repo = Path(repo).resolve()
    home = Path(home).expanduser().absolute()
    files = json.loads((repo / 'manifest.json').read_text())['files']
    # Canonicalize OS aliases such as /tmp -> /private/tmp, but reject a
    # symlink at the selected home itself and anywhere inside the payload.
    home = home.parent.resolve() / home.name
    no_symlinks(home)
    if not files:
        raise ValueError('Empty snapshot')
    pending = []
    conflicts = []
    missing = 0
    # Validate the entire snapshot and every destination before creating anything.
    for name, expected in sorted(files.items()):
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or not relative.parts or '\\' in name:
            raise ValueError('Unsafe snapshot path: ' + name)
        source = repo / 'payload' / name
        no_symlinks(source)
        if not source.is_file() or digest(source) != expected:
            raise ValueError('Snapshot checksum mismatch: ' + name)
        target = home / name
        no_symlinks(target)
        if target.exists():
            if not target.is_file() or digest(target) != expected:
                conflicts.append(name)
                print('CONFLICT ' + name)
            else:
                print('MATCH ' + name)
        else:
            missing += 1
            pending.append((source, target))
            print(('MISSING ' if verify else 'CREATE ') + name)
    if conflicts:
        raise ValueError('Existing files differ; back up and reconcile manually. No files written.')
    if apply:
        for source, target in pending:
            target.parent.mkdir(parents=True, exist_ok=True)
            # Exclusive create also refuses a file introduced after preflight.
            with target.open('xb') as output:
                output.write(source.read_bytes())
            target.chmod(source.stat().st_mode & 0o777)
        print('Applied {} files; existing identical files preserved.'.format(len(pending)))
    return 1 if verify and missing else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['plan', 'apply', 'verify'])
    parser.add_argument('--home', type=Path, default=Path.home(), help='Destination home (use a fresh directory for smoke verification)')
    args = parser.parse_args()
    try:
        return restore(Path(__file__).resolve().parents[1], args.home,
                       apply=args.command == 'apply', verify=args.command == 'verify')
    except (ValueError, OSError, KeyError, TypeError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
