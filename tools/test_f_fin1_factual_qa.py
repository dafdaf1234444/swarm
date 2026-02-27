#!/usr/bin/env python3
"""Regression tests for F-FIN1 factual-QA diversification harness."""

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import f_fin1_factual_qa as mod


class TestFFIN1FactualQA(unittest.TestCase):
    def test_normalize_strips_accents(self):
        self.assertEqual(mod._normalize("Brasilia"), mod._normalize("Brasília"))

    def test_majority_vote_uses_mode(self):
        self.assertEqual(mod._majority_vote(["Paris", "Paris", "Lyon"]), "Paris")

    def test_majority_vote_tie_breaks_first_seen(self):
        self.assertEqual(mod._majority_vote(["Rome", "Paris"]), "Rome")

    def test_correctness_match(self):
        self.assertTrue(mod._is_correct("Capital of India", "New Delhi is the capital of India.", "New Delhi"))
        self.assertFalse(mod._is_correct("Delhi Sultanate", "A medieval empire.", "New Delhi"))

    def test_extract_capital_answer_patterns(self):
        a = mod._extract_capital_answer("The capital of India is New Delhi.", "India")
        b = mod._extract_capital_answer("Tokyo is the capital city of Japan.", "Japan")
        self.assertEqual(mod._normalize(a), mod._normalize("New Delhi"))
        self.assertEqual(mod._normalize(b), mod._normalize("Tokyo"))

    def test_extract_capital_answer_handles_capital_and_largest_city(self):
        summary = "Paris is the capital and most populous city of France."
        answer = mod._extract_capital_answer(summary, "France")
        self.assertEqual(mod._normalize(answer), mod._normalize("Paris"))

    @mock.patch.object(mod, "_resolve_summary")
    @mock.patch.object(mod, "_resolve_title")
    def test_predict_capital_uses_fallback_queries(self, mock_resolve_title, mock_resolve_summary):
        def fake_resolve(query: str, _lang: str, _cache: dict[str, str]) -> str:
            if query == "France capital city":
                return "Paris"
            return "France"

        def fake_summary(title: str, _lang: str, _cache: dict[str, str]) -> str:
            if title == "Paris":
                return "Paris is the capital and most populous city of France."
            return "France is a country in Europe."

        mock_resolve_title.side_effect = fake_resolve
        mock_resolve_summary.side_effect = fake_summary

        answer, resolved_chain = mod._predict_capital(
            country="France",
            query="Frnace capital",
            lang="en",
            resolve_cache={},
            summary_cache={},
        )
        self.assertEqual(mod._normalize(answer), mod._normalize("Paris"))
        self.assertIn("Paris", resolved_chain)


if __name__ == "__main__":
    unittest.main()
