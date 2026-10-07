#!/usr/bin/env python3
"""Read-only checks of repository files and index; never prints secret values."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.run(['git', '-C', str(ROOT), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def main():
    errors = []
    required = ['AGENT.md', 'RESEARCH_PHILOSOPHY.md', 'STATE.md',
                'LOCAL_WORKSPACE.md', 'MISSING_SOURCES.md',
                'START_RESEARCH_SESSION.md', 'papers/README.md',
                'papers/supplied/README.md', '.gitignore']
    for name in required:
        if not (ROOT / name).is_file():
            errors.append('Required file missing: ' + name)
    probe = subprocess.run(['git', '-C', str(ROOT), 'check-ignore', '--no-index',
                            '-q', 'local/research-health-probe.txt'])
    if probe.returncode != 0:
        errors.append('local/ is not ignored')
    tracked = git('ls-files', '-z').decode().split('\0')
    candidates = git('ls-files', '--cached', '--others', '--exclude-standard', '-z').decode().split('\0')
    secret = re.compile(rb'-----BEGIN (?:[A-Z ]*PRIVATE KEY)-----|\bgh[pousr]_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}')
    for name in filter(None, tracked):
        p = Path(name)
        if p.parts[0] == 'local':
            errors.append('Local file tracked or staged: ' + name)
        if p.name == '.env' or (p.name.startswith('.env.') and p.name != '.env.example') or p.name in {'id_rsa', 'id_ed25519', 'credentials.json'}:
            errors.append('Sensitive filename tracked or staged: ' + name)
        if secret.search(git('show', ':' + name)):
            errors.append('Possible credential in index: ' + name)
    for name in sorted(set(filter(None, candidates))):
        p = ROOT / name
        if p.is_symlink():
            errors.append('Review symlink manually: ' + name)
        elif p.is_file() and secret.search(p.read_bytes()):
            errors.append('Possible credential in working file: ' + name)
    state = ROOT / 'STATE.md'
    if state.exists() and (state.stat().st_size > 8192 or len(state.read_text().splitlines()) > 80):
        errors.append('STATE.md exceeds compact-state review threshold (80 lines / 8 KiB)')
    if errors:
        for error in errors:
            print('FAIL:', error)
        return 1
    print('PASS: core files and supplied-source directory exist; local/ ignored.')
    print('PASS: no local/ files or sensitive filenames in index; no recognized credential patterns.')
    print('PASS: STATE.md is compact. Secret checks are heuristic, not a guarantee.')
    print('NOTE: this does not verify PDF readability, redistribution rights, MCP access or research correctness.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, subprocess.CalledProcessError):
        print('FAIL: unable to inspect repository files or Git index')
        sys.exit(1)
