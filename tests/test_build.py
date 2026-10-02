import gzip, json, os, unittest

DIST = os.environ.get("SDEPIPE_DIST", "dist")


def load():
    for fn in os.listdir(DIST):
        if fn.startswith("dataset-") and fn.endswith(".json.gz"):
            return json.load(gzip.open(os.path.join(DIST, fn)))
    raise unittest.SkipTest("no dataset built")


class TestDataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ds = load()

    def test_rifter(self):
        t = self.ds["types"]["587"]
        self.assertEqual(t["name"], "Rifter")
        self.assertEqual(t["category"], 6)
        self.assertIn("9", t["attrs"])  # structure hp

    def test_skill_effects_have_modifiers(self):
        gunnery = self.ds["types"]["3300"]
        effs = [self.ds["effects"][str(e)] for e, _ in gunnery["effects"]]
        self.assertTrue(any(e["mods"] for e in effs))

    def test_operator_codes(self):
        ops = {m[4] for e in self.ds["effects"].values() for m in e["mods"]}
        self.assertTrue(ops <= {-1, 0, 1, 2, 3, 4, 5, 6, 7, 9}, ops)

    def test_warfare_buffs(self):
        self.assertIn("10", self.ds["dbuffs"])


if __name__ == "__main__":
    unittest.main()
