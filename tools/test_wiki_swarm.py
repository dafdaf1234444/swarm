#!/usr/bin/env python3
"""Regression tests for wiki_swarm generic invocation handling."""

import io
import unittest
from unittest.mock import patch

import wiki_swarm


class TestWikiSwarm(unittest.TestCase):
    def test_generic_invocation_variants(self):
        self.assertTrue(wiki_swarm.is_generic_invocation("swarm"))
        self.assertTrue(wiki_swarm.is_generic_invocation("wiki swarm"))
        self.assertTrue(wiki_swarm.is_generic_invocation("swarm the wiki swarm"))
        self.assertTrue(wiki_swarm.is_generic_invocation("Swarm, the wiki swarm!"))

    def test_main_uses_auto_for_generic_phrase(self):
        with patch.object(
            wiki_swarm,
            "choose_auto_topic",
            return_value=("Swarm intelligence", "auto(default)"),
        ) as choose_auto, patch.object(
            wiki_swarm,
            "swarm_topic",
            return_value=("Swarm intelligence", []),
        ) as swarm_topic, patch.object(
            wiki_swarm, "render_markdown", return_value="report\n"
        ), patch("sys.stdout", new_callable=io.StringIO):
            rc = wiki_swarm.main(["swarm", "the", "wiki", "swarm"])

        self.assertEqual(rc, 0)
        choose_auto.assert_called_once()
        swarm_topic.assert_called_once_with("Swarm intelligence", 1, 5, "en")

    def test_main_keeps_manual_topic_when_specific(self):
        with patch.object(wiki_swarm, "choose_auto_topic") as choose_auto, patch.object(
            wiki_swarm,
            "swarm_topic",
            return_value=("Swarm intelligence", []),
        ) as swarm_topic, patch.object(
            wiki_swarm, "render_markdown", return_value="report\n"
        ), patch("sys.stdout", new_callable=io.StringIO):
            rc = wiki_swarm.main(["Swarm intelligence"])

        self.assertEqual(rc, 0)
        choose_auto.assert_not_called()
        swarm_topic.assert_called_once_with("Swarm intelligence", 1, 5, "en")


if __name__ == "__main__":
    unittest.main()
