"""Regression coverage for the human-readable scenario corpus projections."""
import pathlib
import shutil
import subprocess
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


class CorpusPagesProjectionTest(unittest.TestCase):
    def test_every_corpus_pattern_has_a_catalogue_target(self):
        catalogue = yaml.safe_load((ROOT / "method/scenario-patterns.yaml").read_text())
        ids = [pattern["id"] for pattern in catalogue["patterns"]]
        self.assertEqual(len(ids), len(set(ids)), "Pattern IDs must be unique")
        used = set()
        for path in (ROOT / "corpora").glob("*.yaml"):
            data = yaml.safe_load(path.read_text())
            if not isinstance(data, dict) or "corpus" not in data:
                continue
            for scenario in data["corpus"].get("scenarios", []):
                used.update(scenario.get("scenario_patterns", []))
        self.assertTrue(used)
        self.assertFalse(used - set(ids), f"Broken pattern references: {sorted(used - set(ids))}")

    @unittest.skipUnless(shutil.which("ruby"), "Ruby is required for projection execution")
    def test_projection_exposes_readable_fields_and_pattern_anchors(self):
        script = r"""
require "yaml"
module Jekyll
  class Page; end
  class Generator
    def self.safe(_arg); end
    def self.priority(_arg); end
  end
end
load ARGV.fetch(0)
root = ARGV.fetch(1)
renderer = RahpPagesProjection::Generator.allocate
site = Struct.new(:source).new(root)
catalogue = YAML.safe_load(File.read(File.join(root, "method/scenario-patterns.yaml")), aliases: true)
pattern_page = renderer.send(:scenario_patterns_summary, catalogue).join("\n")
catalogue.fetch("patterns").each do |pattern|
  id = pattern.fetch("id")
  raise "missing pattern anchor #{id}" unless pattern_page.include?("<a id=\"#{id.downcase}\"></a>")
  raise "missing pattern description #{id}" unless pattern_page.include?(pattern.fetch("description").gsub("\n", " "))
end
Dir.glob(File.join(root, "corpora", "*.yaml")).each do |file|
  parsed = YAML.safe_load(File.read(file), aliases: true)
  next unless parsed.is_a?(Hash) && parsed["corpus"].is_a?(Hash)
  corpus = parsed.fetch("corpus")
  page = renderer.send(:corpus_summary, site, corpus).join("\n")
  corpus.fetch("scenarios").each do |scenario|
    raise "missing goal #{scenario['id']}" unless page.include?(scenario.fetch("primary_goal"))
    if scenario["source_anchor"]
      raise "missing source #{scenario['id']}" unless page.include?(scenario.fetch("source_anchor"))
    end
    Array(scenario["scenario_patterns"]).each do |id|
      raise "missing pattern link #{id}" unless page.include?("](/method/scenario-patterns/##{id.downcase})")
    end
  end
  if corpus["depends_on"]
    corpus["depends_on"].each do |dependency|
      id = dependency.is_a?(Hash) ? dependency.fetch("corpus_id") : dependency
      raise "missing dependency #{id}" unless page.include?("[#{id}](/corpora/")
    end
  end
  if corpus["evidence_grade"]
    raise "missing evidence grade" unless page.include?(corpus["evidence_grade"])
  else
    raise "invented evidence grade" unless page.include?("Not declared")
  end
end
pinned = {"source_repository" => "trustoverip/dtgwg-trust-tasks-tf", "source_commit" => "4937c70df95e56ed6404b8c004106ecb121a23cf"}
raise "missing pinned link" unless renderer.send(:source_anchor_link, pinned, "SPEC.md#482-audience-binding").include?("/blob/4937c70df95e56ed6404b8c004106ecb121a23cf/SPEC.md#482-audience-binding")
raise "prose fabricated as link" if renderer.send(:source_anchor_link, pinned, "Trust Tasks §4.9 + CredSpec").include?("](")
raise "symbolic pin fabricated as link" if renderer.send(:source_anchor_link, pinned.merge("source_commit" => "derived-from-pinned-dependencies"), "SPEC.md#x").include?("](")
"""
        result = subprocess.run(
            ["ruby", "-e", script, str(ROOT / "_plugins/structured_data_pages.rb"), str(ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
