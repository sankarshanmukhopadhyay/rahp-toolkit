# frozen_string_literal: true

require "json"
require "yaml"
require_relative "../_plugins/corpus_evidence_links"

root = File.expand_path("..", __dir__)
references = CorpusEvidenceLinks.collect(root)
corpora = Dir.glob(File.join(root, "corpora", "*.yaml")).sort.filter_map do |path|
  data = YAML.safe_load(File.read(path), aliases: true)
  next unless data.is_a?(Hash) && data["corpus"].is_a?(Hash)
  corpus = data.fetch("corpus")
  eligible = CorpusEvidenceLinks.for_corpus(references, corpus)
  { "corpus" => corpus["id"], "source_commit" => corpus["source_commit"],
    "scenario_count" => Array(corpus["scenarios"]).length,
    "qualified_references" => eligible.length,
    "review_paths" => eligible.map { |ref| ref["review_path"] }.uniq.sort }
end
result = { "contract" => "rahp-corpus-review-reference/v1",
  "scope" => "explicit, source-revision-qualified citations; not execution/PASS or people-harm mapping",
  "corpora" => corpora,
  "total_qualified_references" => corpora.sum { |c| c["qualified_references"] } }
puts JSON.pretty_generate(result)
