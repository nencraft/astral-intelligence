from django.test import SimpleTestCase

from .services.briefing_prompt import PROMPT_VERSION, build_briefing_prompt


class BriefingPromptTests(SimpleTestCase):
    def test_build_briefing_prompt_includes_snapshot_and_caveats(self):
        snapshot = {
            "snapshot_version": "briefing-source-v1",
            "near_earth_object": {
                "nasa_jpl_id": "3542519",
                "name": "(2010 PK9)",
            },
            "astral_score": {
                "score": 81,
                "model_version": "APS-v1",
            },
        }

        caveats = [
            "The Astral score is not an impact probability.",
        ]

        briefing_prompt = build_briefing_prompt(snapshot, caveats)

        self.assertIn("3542519", briefing_prompt)

        self.assertIn("(2010 PK9)", briefing_prompt)
        self.assertIn("APS-v1", briefing_prompt)
        self.assertIn("The Astral score is not an impact probability.", briefing_prompt)

    def test_prompt_version_is_briefing_v1(self):
        self.assertEqual(PROMPT_VERSION, "briefing-v1")

    def test_build_briefing_includes_output_and_safety_rules(self):
        prompt = build_briefing_prompt({}, [])

        self.assertIn("plain_english_summary", prompt)
        self.assertIn("technical_summary", prompt)
        self.assertIn("risk_context", prompt)
        self.assertIn("Do not claim that an Earth impact will occur.", prompt)
        self.assertIn(
            "Do not describe the Astral score as a collision or impact probability.",
            prompt,
        )
        self.assertIn("Do not include Markdown code fences.", prompt)
