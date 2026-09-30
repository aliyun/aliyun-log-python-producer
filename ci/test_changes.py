import unittest

from changes import needs_build


class BuildChangesTest(unittest.TestCase):
    def test_documentation_only_skips_builds(self):
        self.assertFalse(needs_build(["README.md", "docs/platforms.md", "docs/credentials_cn.md"]))

    def test_code_dependency_and_workflow_changes_build(self):
        for path in ("src/lib.rs", "python/aliyun_log_producer/producer.py", "tests/test_credentials.py",
                     "ci/platforms.py", ".github/workflows/python.yml", "Cargo.toml", "Cargo.lock", "pyproject.toml"):
            with self.subTest(path=path):
                self.assertTrue(needs_build(["README.md", path]))
