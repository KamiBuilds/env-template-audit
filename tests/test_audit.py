import unittest

from env_template_audit import audit_text


class AuditTextTests(unittest.TestCase):
    def test_reports_keys_missing_from_environment(self):
        report = audit_text("API_URL=\nTOKEN=\n", "API_URL=https://example.test\n")

        self.assertEqual(report.missing, ("TOKEN",))

    def test_reports_keys_not_declared_by_template(self):
        report = audit_text("API_URL=\n", "API_URL=x\nDEBUG=true\n")

        self.assertEqual(report.extra, ("DEBUG",))

    def test_reports_duplicate_environment_keys(self):
        report = audit_text("API_URL=\n", "API_URL=first\nexport API_URL=second\n")

        self.assertEqual(report.env_duplicates, ("API_URL",))


if __name__ == "__main__":
    unittest.main()
