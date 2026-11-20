"""Build reproducible Phase4.9 Lite from committed source; never package private data."""
import argparse, hashlib, io, json, subprocess, tarfile, zipfile
from pathlib import Path

EDITION = 'ICARUS_Phase4_9_Living_Specimens_Lite'
RUNTIME_COMMIT = 'd2bf219e9bbbedf22c145fd38b7129c9e4bfc410'
NEW = ['web/specimen-life.js', 'web/specimen-art.js', 'web/specimen-ui.js']
DOCS = ['README_PHASE49.md', 'PHASE49_ARCHITECTURE.md', 'PHASE49_VALIDATION.md',
        'PHASE49_SECURITY_REVIEW.md', 'PHASE49_LIVING_SPECIMENS_PLAN.md']

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    project = Path(__file__).resolve().parent
    repo = project.parent
    git = lambda *args: subprocess.check_output(['git', *args], cwd=repo)
    commit = git('rev-parse', 'HEAD').decode().strip()
    baseline = repo / 'downloads/phase48c-routing/UMBRA_Phase4_8C_Headphone_Routing_Checkpoint_Lite.zip'
    with zipfile.ZipFile(baseline) as z:
        old = json.loads(z.read(next(n for n in z.namelist() if n.endswith('/BUILD_MANIFEST.json'))))
    runtime = sorted(set(old['runtime_files']) | set(NEW))
    files = sorted((set(old['files']) | set(NEW) | set(DOCS)) - {'BUILD_MANIFEST.json'})
    # Only exact retained source paths enter the tar/ZIP. No recursive private directories.
    with tarfile.open(fileobj=io.BytesIO(git('archive', commit, *['ICARUS/' + n for n in files]))) as tar:
        payloads = {m.name.removeprefix('ICARUS/'): tar.extractfile(m).read()
                    for m in tar.getmembers() if m.isfile()}
    assert set(payloads) == set(files)
    hashes = {n: digest(payloads[n]) for n in files}
    runtime_hashes = {n: hashes[n] for n in runtime}
    scope = json.loads(git('show', commit + ':ICARUS/reports/phase49/runtime_scope.json'))
    assert runtime_hashes == scope['runtime_files'], 'Committed runtime differs from tested freeze'
    for n in runtime:
        if any(token in n for token in ['audio', 'sound', 'anomal', 'arcade']):
            assert runtime_hashes[n] == old['runtime_files'][n], 'Protected existing subsystem changed'
    manifest = {'edition': EDITION, 'source_repository': 'thekiddam-code/munza69',
                'source_commit': commit, 'runtime_commit': RUNTIME_COMMIT,
                'runtime_files': runtime_hashes, 'files': hashes,
                'audio_runtime_unchanged': True, 'physical_devices_tested': False,
                'actual_current_user_voyage_available': False, 'final_release_ready': False,
                'policy': 'Every retained file is byte-identical to source_commit. All runtime dependencies retained; tests, reports, developer tools, packaging scripts and private saves/media/sounds/credentials excluded. Older builds require a pre4.9 backup in a separate browser profile; no downgrade converter.'}
    payloads['BUILD_MANIFEST.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    a.output.mkdir(parents=True, exist_ok=True)
    out = a.output / (EDITION + '.zip')
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for n in sorted(payloads):
            info = zipfile.ZipInfo(EDITION + '/' + n, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, payloads[n], compresslevel=9)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == {EDITION + '/' + n for n in payloads}
        assert all(digest(z.read(EDITION + '/' + n)) == h for n, h in hashes.items())
    sha = digest(out.read_bytes())
    (a.output / 'SHA256SUMS.txt').write_text(sha + '  ' + out.name + '\n')
    result = {'zip': out.name, 'sha256': sha, 'bytes': out.stat().st_size,
              'source_commit': commit, 'runtime_commit': RUNTIME_COMMIT,
              'runtime_files': len(runtime), 'files_including_manifest': len(payloads),
              'crc_and_source_hashes_passed': True, 'deterministic_zip_metadata': True,
              'audio_unchanged': True, 'private_inputs_packaged': False}
    (a.output / 'package_verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
