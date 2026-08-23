import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "account_recovery_tracker.py"
spec = importlib.util.spec_from_file_location("tracker", MODULE_PATH)
tracker = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(tracker)


class AccountRecoveryTrackerTests(unittest.TestCase):
    def test_lifecycle_keeps_only_non_sensitive_operational_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "recovery.json"
            self.assertEqual(tracker.main(["init", "--account", "@mayatasanchess", "--file", str(path)]), 0)
            self.assertEqual(
                tracker.main(["set", "--file", str(path), "--step", "official_flow_started", "--status", "done"]),
                0,
            )
            self.assertEqual(
                tracker.main(
                    [
                        "log", "--file", str(path), "--event", "alerta de alteração recebido",
                        "--source", "e-mail", "--action", "iniciado fluxo oficial", "--result", "pendente",
                    ]
                ),
                0,
            )
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(data["steps"]["official_flow_started"])
            self.assertEqual(data["events"][0]["source"], "e-mail")

    def test_secret_like_log_is_rejected(self):
        with self.assertRaises(ValueError):
            tracker.reject_sensitive("senha: nao-compartilhe", "Evento")

    def test_invalid_account_is_rejected(self):
        with self.assertRaises(ValueError):
            tracker.new_tracker("mayatasanchess", "Instagram")


if __name__ == "__main__":
    unittest.main()
