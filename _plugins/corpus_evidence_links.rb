# frozen_string_literal: true

require "yaml"
require "json"
require "date"

# A review reference is evidence of a citation, not evidence of a passed test.
# Never match a substring, inherited pattern, similarly named finding, or
# a review of a different revision.
module CorpusEvidenceLinks
  ROOTS = ["examples", "instances"].freeze
  FIELDS = %w[corpus_id scenario_id source_commit].freeze
  MAX_FILES = 20000

  def self.review_files(root)
    files = ROOTS.flat_map do |dir|
      Dir.glob(File.join(root, dir, "**", "*")).select do |file|
        File.file?(file) && %w[.yaml .yml .json].include?(File.extname(file))
      end
    end
    raise "Unbounded review inventory" if files.size > MAX_FILES
    files.sort
  end

  def self.parse(file)
    case File.extname(file)
    when ".json" then JSON.parse(File.read(file))
    else YAML.safe_load(File.read(file), permitted_classes: [Date, Time], aliases: true)
    end
  rescue StandardError
    nil # This document cannot establish a link.
  end

  def self.review_record?(data)
    data.is_a?(Hash) && data["review"].is_a?(Hash) &&
      data["review"]["id"].is_a?(String) && !data["review"]["id"].empty?
  end

  def self.evidence_exists?(review, path)
    path.split("/").reduce(review) do |node, segment|
      if node.is_a?(Hash) then node[segment]
      elsif node.is_a?(Array) && segment.match?(/\A\d+\z/) then node[segment.to_i]
      else nil end
    end != nil
  end

  def self.collect(root)
    review_files(root).flat_map do |file|
      data = parse(file)
      next [] unless review_record?(data)
      review = data.fetch("review")
      # Only explicitly declared, version-qualified, review-level citations.
      references = review["corpus_scenario_references"]
      next [] unless references.is_a?(Array)
      relative = file.delete_prefix(root + File::SEPARATOR)
      references.filter_map do |ref|
        next unless ref.is_a?(Hash) && FIELDS.all? { |key| ref[key].is_a?(String) && !ref[key].empty? }
        next unless ref["source_commit"].match?(/\A[0-9a-f]{40}\z/i)
        next unless ref["evidence_path"].is_a?(String) && !ref["evidence_path"].empty?
        # Evidence path must point to retained material inside this review.
        evidence = ref["evidence_path"]
        next unless evidence.match?(/\A(?:findings|summary|method|scope)(?:\/[A-Za-z0-9_-]+)+\z/)
        next unless evidence_exists?(review, evidence)
        { "corpus_id" => ref["corpus_id"], "scenario_id" => ref["scenario_id"],
          "source_commit" => ref["source_commit"], "review_id" => review["id"],
          "review_path" => relative, "evidence_path" => evidence }
      end
    end
  end

  def self.for_corpus(references, corpus)
    return [] unless corpus["source_commit"].to_s.match?(/\A[0-9a-f]{40}\z/i)
    ids = Array(corpus["scenarios"]).map { |s| s["id"] }.compact
    references.select do |ref|
      ref["corpus_id"] == corpus["id"] &&
        ref["source_commit"].casecmp?(corpus["source_commit"]) &&
        ids.include?(ref["scenario_id"])
    end.uniq { |ref| [ref["review_path"], ref["review_id"], ref["scenario_id"], ref["evidence_path"]] }
  end
end
