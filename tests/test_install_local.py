"""Exercise fresh installs, backup updates, and failure recovery without user state."""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


PACKAGE = Path(__file__).resolve().parents[1] / "blog-erh-v2-0-0"
SPEC = importlib.util.spec_from_file_location("installer", PACKAGE / "scripts/install_local.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = tempfile.TemporaryDirectory(prefix="erh-install-test-")
        self.addCleanup(self.sandbox.cleanup)
        self.root = Path(self.sandbox.name).resolve()
        self.source = self.root / "download" / installer.NAME
        shutil.copytree(PACKAGE, self.source, ignore=installer.IGNORE)
        self.skills = self.root / "codex" / "skills"

    def test_fresh_install_excludes_caches_and_preserves_other_skills(self):
        other = self.skills / "other-skill"
        other.mkdir(parents=True)
        (other / "keep.txt").write_text("unchanged")
        cache = self.source / "scripts" / "__pycache__"
        cache.mkdir()
        (cache / "junk.pyc").write_bytes(b"cache")
        (self.source / "._SKILL.md").write_bytes(b"network drive metadata")
        target, backup = installer.install(self.source, self.skills)
        self.assertIsNone(backup)
        self.assertTrue((target / "SKILL.md").is_file())
        self.assertFalse((target / "scripts" / "__pycache__").exists())
        self.assertFalse((target / "._SKILL.md").exists())
        self.assertEqual((other / "keep.txt").read_text(), "unchanged")

    def test_update_requires_replace_and_retains_complete_previous_copy(self):
        target, _ = installer.install(self.source, self.skills)
        (target / "local-note.txt").write_text("operator edits")
        with self.assertRaises(FileExistsError):
            installer.install(self.source, self.skills)
        self.assertEqual((target / "local-note.txt").read_text(), "operator edits")
        updated, backup = installer.install(self.source, self.skills, replace=True)
        self.assertEqual(updated, target)
        self.assertEqual(backup.parent, self.skills.parent / "skill-backups")
        self.assertEqual((backup / "local-note.txt").read_text(), "operator edits")
        self.assertFalse((updated / "local-note.txt").exists())

    def test_invalid_download_leaves_installed_copy_intact(self):
        target, _ = installer.install(self.source, self.skills)
        (target / "local-note.txt").write_text("keep")
        (self.source / "requirements.txt").unlink()
        with self.assertRaises(subprocess.CalledProcessError):
            installer.install(self.source, self.skills, replace=True)
        self.assertEqual((target / "local-note.txt").read_text(), "keep")
        self.assertFalse((self.skills.parent / "skill-backups").exists())

    def test_activation_failure_restores_previous_version(self):
        target, _ = installer.install(self.source, self.skills)
        (target / "local-note.txt").write_text("restore me")
        original_rename = Path.rename

        def fail_activation(path, destination):
            if path.parent.name.startswith(".erh-install-"):
                raise OSError("simulated activation failure")
            return original_rename(path, destination)

        with patch.object(Path, "rename", fail_activation):
            with self.assertRaisesRegex(OSError, "simulated"):
                installer.install(self.source, self.skills, replace=True)
        self.assertEqual((target / "local-note.txt").read_text(), "restore me")

    def test_running_installed_script_is_a_noop(self):
        target, _ = installer.install(self.source, self.skills)
        result, backup = installer.install(target, self.skills, replace=True)
        self.assertEqual(result, target)
        self.assertIsNone(backup)
        self.assertFalse((self.skills.parent / "skill-backups").exists())

    def test_reinstalling_identical_package_does_not_create_backup(self):
        target, _ = installer.install(self.source, self.skills)
        result, backup = installer.install(self.source, self.skills, replace=True)
        self.assertEqual(result, target)
        self.assertIsNone(backup)
        self.assertFalse((self.skills.parent / "skill-backups").exists())


if __name__ == "__main__":
    unittest.main()
