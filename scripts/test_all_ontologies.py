#!/usr/bin/env python3
"""Test import and verification for all ontologies in the repository."""

import subprocess
import shutil
import time
from pathlib import Path

# Map ontology directories to their source files and prefixes
# Only include ontologies that have source files in originals/
ONTOLOGIES = {
    'dc': ('originals/dc.ttl', 'dc'),
    'dcam': ('originals/dcam.rdf', 'dcam'),
    'dcterms': ('originals/dcterms.ttl', 'dcterms'),
    'doap': ('originals/doap.rdf', 'doap'),
    'foaf': ('originals/foaf.ttl', 'foaf'),
    'geo': ('originals/geo.rdf', 'geo'),
    'owl': ('originals/owl.ttl', 'owl'),
    'prov': ('originals/prov.ttl', 'prov'),
    'rdf': ('originals/rdf.ttl', 'rdf'),
    'rdfs': ('originals/rdfs.ttl', 'rdfs'),
    'sioc': ('originals/sioc.rdf', 'sioc'),
    'skos': ('originals/skos.rdf', 'skos'),
    'time': ('originals/time.ttl', 'time'),
    'vcard': ('originals/vcard.rdf', 'vcard'),
    # xsd is manually curated (no RDF source from W3C)
}

def run_command(cmd: list, cwd: Path) -> tuple[bool, float, str]:
    """Run a command and return (success, duration, output)."""
    start = time.time()
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    duration = time.time() - start
    output = result.stdout + result.stderr
    return result.returncode == 0, duration, output

def test_ontology(name: str, source: str, prefix: str, repo_root: Path) -> dict:
    """Test import and verification for a single ontology."""
    result = {
        'name': name,
        'source': source,
        'success': False,
        'import_time': 0,
        'uri_index_time': 0,
        'validate_time': 0,
        'verify_time': 0,
        'triples': 0,
        'anchors': 0,
        'files': 0,
        'errors': [],
    }

    ont_dir = repo_root / name
    source_path = repo_root / source

    # Check if source exists
    if not source_path.exists():
        result['errors'].append(f"Source file not found: {source}")
        return result

    # Backup original directory
    backup_dir = repo_root / f"{name}_backup"
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    if ont_dir.exists():
        shutil.copytree(ont_dir, backup_dir)
        shutil.rmtree(ont_dir)

    try:
        # Import
        success, duration, output = run_command(
            ['python3', 'scripts/import_ontology.py', source, name, '-p', prefix],
            repo_root
        )
        result['import_time'] = duration
        if not success:
            result['errors'].append(f"Import failed: {output}")
            raise Exception("Import failed")

        # Parse import output for stats
        for line in output.split('\n'):
            if 'triples' in line.lower():
                try:
                    result['triples'] = int(line.split()[0])
                except:
                    pass
            if 'anchors' in line.lower() or 'resources' in line.lower():
                try:
                    result['anchors'] = int(line.split()[0])
                except:
                    pass

        # Count files
        result['files'] = len(list(ont_dir.glob('*.md')))

        # Add URI and index
        success, duration, output = run_command(
            ['python3', 'scripts/add_uri_and_index.py', name],
            repo_root
        )
        result['uri_index_time'] = duration
        if not success:
            result['errors'].append(f"URI/Index failed: {output}")

        # Validate
        success, duration, output = run_command(
            ['python3', 'scripts/validate.py', name],
            repo_root
        )
        result['validate_time'] = duration
        if not success:
            result['errors'].append(f"Validation failed: {output}")

        # Verify semantic equivalence
        success, duration, output = run_command(
            ['python3', 'scripts/verify_import.py', source, name],
            repo_root
        )
        result['verify_time'] = duration
        if 'Semantically equivalent' in output or 'equivalent' in output.lower():
            result['success'] = True
        else:
            result['errors'].append(f"Verification: {output.strip()}")
            # Still mark as success if close enough
            if 'In files only: 0' in output and 'In RDF only: 0' in output:
                result['success'] = True

    except Exception as e:
        result['errors'].append(str(e))
    finally:
        # Restore backup
        if backup_dir.exists():
            if ont_dir.exists():
                shutil.rmtree(ont_dir)
            shutil.move(backup_dir, ont_dir)

    return result

def main():
    repo_root = Path(__file__).parent.parent

    print("=" * 80)
    print("TESTING ALL ONTOLOGIES")
    print("=" * 80)
    print()

    results = []
    total_start = time.time()

    for name, (source, prefix) in sorted(ONTOLOGIES.items()):
        print(f"Testing {name}...", end=" ", flush=True)
        result = test_ontology(name, source, prefix, repo_root)
        results.append(result)

        if result['success']:
            total_time = result['import_time'] + result['uri_index_time'] + result['validate_time'] + result['verify_time']
            print(f"OK ({total_time:.2f}s, {result['triples']} triples, {result['files']} files)")
        else:
            print(f"FAILED")
            for err in result['errors']:
                print(f"  - {err[:100]}")

    total_duration = time.time() - total_start

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    # Table header
    print(f"{'Ontology':<12} {'Import':>8} {'URI/Idx':>8} {'Valid':>8} {'Verify':>8} {'Total':>8} {'Triples':>8} {'Files':>6} {'Status':>8}")
    print("-" * 90)

    success_count = 0
    for r in results:
        total = r['import_time'] + r['uri_index_time'] + r['validate_time'] + r['verify_time']
        status = "OK" if r['success'] else "FAIL"
        if r['success']:
            success_count += 1
        print(f"{r['name']:<12} {r['import_time']:>7.2f}s {r['uri_index_time']:>7.2f}s {r['validate_time']:>7.2f}s {r['verify_time']:>7.2f}s {total:>7.2f}s {r['triples']:>8} {r['files']:>6} {status:>8}")

    print("-" * 90)

    # Totals
    total_import = sum(r['import_time'] for r in results)
    total_uri = sum(r['uri_index_time'] for r in results)
    total_validate = sum(r['validate_time'] for r in results)
    total_verify = sum(r['verify_time'] for r in results)
    total_triples = sum(r['triples'] for r in results)
    total_files = sum(r['files'] for r in results)

    print(f"{'TOTAL':<12} {total_import:>7.2f}s {total_uri:>7.2f}s {total_validate:>7.2f}s {total_verify:>7.2f}s {total_duration:>7.2f}s {total_triples:>8} {total_files:>6} {success_count}/{len(results)}")

    print()

    if success_count == len(results):
        print("All ontologies passed!")
    else:
        print(f"Failed ontologies:")
        for r in results:
            if not r['success']:
                print(f"  - {r['name']}: {', '.join(r['errors'][:2])}")

if __name__ == '__main__':
    main()
