import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('replica', Path(__file__).parents[1] / 'scripts/replica.py')
replica = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replica)


class RestoreSafety(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.repo = self.root / 'repo'
        self.home = self.root / 'home'
        self.repo.mkdir()
        self.home.mkdir()
        self.add_file('.omp/agent/config.yml', b'theme: dark\n')

    def add_file(self, name, data):
        path = self.repo / 'payload' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        manifest = self.repo / 'manifest.json'
        content = json.loads(manifest.read_text()) if manifest.exists() else {'files': {}}
        content['files'][name] = hashlib.sha256(data).hexdigest()
        manifest.write_text(json.dumps(content))

    def test_restore_is_byte_exact_and_repeatable(self):
        replica.restore(self.repo, self.home, apply=True)
        target = self.home / '.omp/agent/config.yml'
        self.assertEqual(target.read_bytes(), b'theme: dark\n')
        replica.restore(self.repo, self.home, apply=True)
        self.assertEqual(replica.restore(self.repo, self.home, verify=True), 0)

    def test_conflict_prevents_all_writes(self):
        self.add_file('.agents/skills/example/SKILL.md', b'skill')
        target = self.home / '.omp/agent/config.yml'
        target.parent.mkdir(parents=True)
        target.write_bytes(b'existing user config')
        with self.assertRaises(ValueError):
            replica.restore(self.repo, self.home, apply=True)
        self.assertEqual(target.read_bytes(), b'existing user config')
        self.assertFalse((self.home / '.agents').exists())

    def test_plan_does_not_create_directories(self):
        replica.restore(self.repo, self.home)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_tampered_snapshot_prevents_writes(self):
        (self.repo / 'payload/.omp/agent/config.yml').write_bytes(b'tampered')
        with self.assertRaises(ValueError):
            replica.restore(self.repo, self.home, apply=True)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_symlink_parent_cannot_escape_target_home(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (self.home / '.omp').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            replica.restore(self.repo, self.home, apply=True)
        self.assertEqual(list(outside.iterdir()), [])

    def test_manifest_cannot_escape_home(self):
        manifest = self.repo / 'manifest.json'
        manifest.write_text(json.dumps({'files': {'../escape': '0' * 64}}))
        with self.assertRaises(ValueError):
            replica.restore(self.repo, self.home, apply=True)
        self.assertFalse((self.root / 'escape').exists())

    def test_verify_detects_missing_files(self):
        self.assertEqual(replica.restore(self.repo, self.home, verify=True), 1)


if __name__ == '__main__':
    unittest.main()
