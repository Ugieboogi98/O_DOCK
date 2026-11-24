import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / 'import_bundle.py'
spec = importlib.util.spec_from_file_location('bundle_runner', PATH)
module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class BundleCommands(unittest.TestCase):
    def test_all_makers_use_the_same_runtime_and_input_parent(self):
        for name in module.BUNDLES:
            command = module.command_for(name, 'validate', 'test', Path('/project'))
            self.assertIn('--validate-only', command)
            self.assertIn('--no-deps', command)
            self.assertIn('scripts.' + module.BUNDLES[name].module, command)
            self.assertIn('/data/imports/' + module.BUNDLES[name].directory, command)
            self.assertIn('/project/backups/imports/' + name + ':/reports', command)
            self.assertNotIn('--commit', command)

    def test_commit_missing_is_explicit_and_furyu_only(self):
        command = module.command_for('furyu', 'commit-missing', 'test')
        self.assertIn('--commit', command)
        self.assertIn('--allow-missing-images', command)
        with self.assertRaises(ValueError):
            module.command_for('taito', 'commit-missing', 'test')

    def test_dry_run_does_not_invoke_docker(self):
        with patch.object(sys, 'argv', ['import_bundle', 'taito', '--dry-run']), \
             patch.object(module.subprocess, 'run') as run, \
             patch.object(module.subprocess, 'Popen') as popen, \
             patch('builtins.print'):
            module.main()
        run.assert_not_called()
        popen.assert_not_called()


if __name__ == '__main__':
    unittest.main()
