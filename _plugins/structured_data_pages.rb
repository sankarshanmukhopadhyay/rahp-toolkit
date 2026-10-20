# frozen_string_literal: true

require "yaml"
require "json"
require_relative "corpus_evidence_links"

module RahpPagesProjection
  STRUCTURED_ROOTS = %w[corpora method data build/derived build/jsonld examples archive/historical-builds].freeze
  STRUCTURED_FILES = %w[instances/cawg/mandate-readiness.yaml instances/cawg/watch/issues.yaml instances/dtg/watch/issues.yaml].freeze
  STRUCTURED_EXTENSIONS = %w[.yaml .yml .json .jsonld].freeze
  MARKDOWN_ROOTS = %w[examples build archive].freeze
  TOP_LEVEL_MARKDOWN = %w[README.md ADOPTION.md QUICKSTART.md CONTRIBUTING.md ROADMAP.md CHANGELOG.md].freeze

  class ProjectionPage < Jekyll::Page
    def initialize(site, output_route, title, body, source_path = nil, directory_index: true)
      @site = site
      @base = site.source
      normalized = output_route.sub(%r{^/}, "").sub(%r{/$}, "")
      if directory_index
        @dir = normalized
        @name = "index.md"
        permalink = "/#{@dir}/"
      else
        @dir = File.dirname(normalized)
        @dir = "" if @dir == "."
        @name = File.basename(normalized).sub(/\.html\z/i, ".md")
        permalink = "/#{normalized}"
      end
      process(@name)
      self.data = {
        "layout" => "default",
        "title" => title,
        "has_toc" => true,
        "nav_exclude" => true,
        "permalink" => permalink
      }
      self.data["source_path"] = source_path if source_path
      self.content = body
    end
  end

  class Generator < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      rendered_routes = []
      structured_files(site).each do |path|
        relative = relative_path(site, path)
        raw = File.read(path)
        parsed = parse_structured(path, raw)
        next if parsed.nil?
        title = structured_title(relative, parsed)
        route = human_route(relative)
        site.pages << ProjectionPage.new(site, route, title, structured_body(site, relative, parsed, raw), relative)
        rendered_routes << "/#{route}/"
      end

      markdown_files(site).each do |path|
        raw = File.read(path)
        next if raw.start_with?("---\n") # already a normal Jekyll page
        relative = relative_path(site, path)
        route, directory_index = markdown_route(relative)
        site.pages << ProjectionPage.new(site, route, markdown_title(relative, raw), markdown_body(site, relative, raw), relative, directory_index: directory_index)
        rendered_routes << (directory_index ? "/#{route}/" : "/#{route}")
      end

      # Structured repository files remain static and machine-readable at their
      # canonical .yaml/.json paths. Human-readable projections are emitted on
      # clean directory routes so GitHub Pages serves them as HTML.
      Jekyll.logger.info "RAHP Pages projection:", "rendered #{rendered_routes.length} human-readable routes"
    end

    private

    def structured_files(site)
      rooted = STRUCTURED_ROOTS.flat_map do |root|
        absolute_root = File.join(site.source, root)
        next [] unless Dir.exist?(absolute_root)
        Dir.glob(File.join(absolute_root, "**", "*")).select do |path|
          File.file?(path) && STRUCTURED_EXTENSIONS.include?(File.extname(path).downcase)
        end
      end
      exact = STRUCTURED_FILES.map { |path| File.join(site.source, path) }.select { |path| File.file?(path) }
      (rooted + exact).uniq
    end

    def markdown_files(site)
      paths = TOP_LEVEL_MARKDOWN.map { |name| File.join(site.source, name) }.select { |path| File.file?(path) }
      MARKDOWN_ROOTS.each do |root|
        absolute_root = File.join(site.source, root)
        next unless Dir.exist?(absolute_root)
        paths.concat(Dir.glob(File.join(absolute_root, "**", "*.md")).select { |path| File.file?(path) })
      end
      paths.uniq
    end

    def relative_path(site, path)
      path.delete_prefix(site.source + File::SEPARATOR)
    end

    def human_route(relative)
      ext = File.extname(relative)
      STRUCTURED_EXTENSIONS.include?(ext.downcase) ? relative.delete_suffix(ext) : relative.sub(/\.md\z/i, "")
    end

    # Preserve Markdown-relative link semantics. A source such as
    # examples/x/SECURITY_REVIEW.md commonly links to sibling findings.yaml.
    # Rendering it as SECURITY_REVIEW/index.html changes the relative base and
    # breaks those links. README files are directory indexes; all other
    # Markdown projections stay in their source directory as *.html.
    def markdown_route(relative)
      if File.basename(relative).casecmp("README.md").zero?
        [File.dirname(relative).sub(%r{^\.$}, ""), true]
      else
        [relative.sub(/\.md\z/i, ".html"), false]
      end
    end

    def parse_structured(path, raw)
      case File.extname(path).downcase
      when ".yaml", ".yml"
        YAML.safe_load(raw, aliases: true)
      when ".json", ".jsonld"
        JSON.parse(raw)
      end
    rescue StandardError => e
      Jekyll.logger.warn "RAHP Pages projection:", "skipping #{path}: #{e.message}"
      nil
    end

    def structured_title(path, parsed)
      if parsed.is_a?(Hash) && parsed["corpus"].is_a?(Hash)
        parsed["corpus"]["title"] || File.basename(path)
      else
        File.basename(path)
      end
    end

    def markdown_title(path, raw)
      heading = raw.each_line.find { |line| line.start_with?("# ") }
      heading ? heading.sub(/^#\s+/, "").strip : File.basename(path)
    end

    def source_button(site, path)
      "[View canonical source on GitHub](https://github.com/#{site.config['repository']}/blob/main/#{path}){: .btn .btn-primary }"
    end

    def markdown_body(site, path, raw)
      <<~MD
        > This GitHub Pages view renders the repository Markdown at `#{path}`. The GitHub repository remains the canonical source.

        #{source_button(site, path)}

        #{raw}
      MD
    end

    def structured_body(site, path, parsed, raw)
      lines = []
      lines << "# #{structured_title(path, parsed)}"
      lines << ""
      if path.start_with?("archive/")
        lines << "> **Historical artefact.** This page renders retained RAHP history for research and provenance. It is not a current normative or canonical RAHP source. Current material is under `data/`, `method/`, `corpora/`, and `docs/`."
      else
        lines << "> This is a human-readable GitHub Pages projection of the canonical structured source at `#{path}`. The repository source remains the authoritative machine-readable record."
      end
      lines << ""
      lines << source_button(site, path)
      lines << ""
      if parsed.is_a?(Hash) && parsed["corpus"].is_a?(Hash)
        lines.concat(corpus_summary(site, parsed["corpus"]))
      elsif parsed.is_a?(Hash) && parsed["record_type"] == "scenario_pattern" && parsed["patterns"].is_a?(Array)
        lines.concat(scenario_patterns_summary(parsed))
      elsif path.start_with?("method/catalogue/") && parsed.is_a?(Hash) && parsed["records"].is_a?(Array)
        lines.concat(catalogue_summary(parsed))
      elsif parsed.is_a?(Hash) && parsed["review"].is_a?(Hash)
        lines.concat(review_summary(parsed["review"]))
      elsif path.end_with?("persona.jsonld") && parsed.is_a?(Hash)
        lines.concat(persona_summary(parsed))
      elsif parsed.is_a?(Hash) && parsed["@graph"].is_a?(Array)
        lines.concat(jsonld_graph_summary(parsed))
      else
        lines.concat(generic_summary(parsed))
      end
      lines << ""
      lines << "## Canonical source"
      lines << ""
      language = File.extname(path).sub(".", "")
      language = "yaml" if %w[yaml yml].include?(language)
      lines << "```#{language}"
      lines << raw.rstrip
      lines << "```"
      lines.join("\n")
    end


    def corpus_routes(site)
      @corpus_routes ||= Dir.glob(File.join(site.source, "corpora", "*.yaml")).each_with_object({}) do |file, routes|
        begin
          data = YAML.safe_load(File.read(file), aliases: true)
          id = data.is_a?(Hash) && data.dig("corpus", "id")
          routes[id] = "/corpora/#{File.basename(file, '.yaml')}/" if id
        rescue StandardError
          # Invalid sources are diagnosed by repository validators.
        end
      end
    end

    def source_anchor_link(corpus, anchor)
      value = anchor.to_s
      repo = corpus["source_repository"].to_s
      sha = corpus["source_commit"].to_s
      if repo.match?(%r{\A[\w.-]+/[\w.-]+\z}) && sha.match?(/\A[0-9a-fA-F]{7,40}\z/) &&
         value.match?(%r{\A[\w./-]+(?:#[\w.-]+)?\z}) && !value.split("/").include?("..")
        "[#{escape_cell(value)}](https://github.com/#{repo}/blob/#{sha}/#{value})"
      else
        escape_cell(value)
      end
    end

    def site_route(site, path)
      baseurl = site.respond_to?(:config) ? site.config.fetch("baseurl", "").to_s : ""
      "#{baseurl.sub(%r{/$}, "")}#{path}"
    end

    def corpus_summary(site, corpus)
      scenarios = Array(corpus["scenarios"])
      out = ["## Corpus metadata", "", "| Field | Value |", "|---|---|"]
      %w[id source_repository source_path source_commit adapter_version description evidence_grade provenance_status provenance_note assurance_catalogue].each do |key|
        out << "| `#{key}` | #{escape_cell(format_value(corpus[key]))} |" if corpus.key?(key)
      end
      out << "| `evidence_grade` | Not declared |" unless corpus.key?("evidence_grade")
      if corpus.key?("depends_on")
        links = Array(corpus["depends_on"]).map do |dependency|
          id = dependency.is_a?(Hash) ? dependency["corpus_id"] : dependency
          route = corpus_routes(site)[id]
          label = escape_cell(id || format_value(dependency))
          route ? "[#{label}](#{site_route(site, route)})" : label
        end
        out << "| `depends_on` | #{links.join(', ')} |"
      end
      # Review citations are opt-in and exact-version only. No review link
      # establishes execution, PASS, or a person/harm mapping.
      references = CorpusEvidenceLinks.for_corpus(
        (@review_citations ||= CorpusEvidenceLinks.collect(site.source)), corpus
      )
      out << "| \`qualified_review_references\` | #{references.length} |"
      out << "| `scenario_count` | #{scenarios.length} |"
      if corpus["coverage"].is_a?(Hash) && !corpus["coverage"].empty?
        out += ["", "### Coverage", "", "| Dimension | Value |", "|---|---|"]
        corpus["coverage"].each { |key, value| out << "| #{escape_cell(key)} | #{escape_cell(format_value(value))} |" }
      end
      unless scenarios.empty?
        out += ["", "## Scenarios", "", "| ID | Title | Goal | Source | Domain | Pressure | Priority | RAHP patterns |", "|---|---|---|---|---|---|---|---|"]
        scenarios.each do |scenario|
          patterns = Array(scenario["scenario_patterns"]).map { |id| "[`#{escape_cell(id)}`](#{site_route(site, "/method/scenario-patterns/##{id.to_s.downcase}")})" }.join(", ")
          source = scenario.key?("source_anchor") ? source_anchor_link(corpus, scenario["source_anchor"]) : "Not declared"
          goal = scenario.key?("primary_goal") ? escape_cell(scenario["primary_goal"]) : "Not declared"
          out << "| `#{escape_cell(scenario['id'])}` | #{escape_cell(scenario['title'])} | #{goal} | #{source} | #{escape_cell(scenario['domain'])} | #{escape_cell(scenario['primary_pressure'])} | #{escape_cell(scenario['priority'])} | #{patterns} |"
        end
        details = scenarios.select { |scenario| %w[dependencies portable_assurance core_predicates].any? { |key| scenario.key?(key) } }
        unless details.empty?
          out += ["", "### Additional scenario fields", ""]
          details.each do |scenario|
            out += ["#### #{escape_cell(scenario['id'])}", ""]
            %w[dependencies portable_assurance core_predicates].each do |key|
              out << "- **#{key.tr('_', ' ')}:** #{escape_cell(format_value(scenario[key]))}" if scenario.key?(key)
            end
            out << ""
          end
        end
      end
      out += ["", "## Review evidence links", "",
              "A reference below establishes only that a review explicitly cites the same corpus scenario at the declared source revision; it does not establish a passing test or a harm finding.", ""]
      if references.empty?
        out << "**No linked review evidence identified.** This does not mean the scenario has not been tested."
      else
        out += ["| Scenario | Review | Evidence reference |", "|---|---|---|"]
        references.each do |ref|
          path = ref["review_path"]
          route = human_route(path)
          url = site_route(site, "/#{route}/")
          # All indexed review sources are structured documents with clean Pages routes.
          out << "| \`#{escape_cell(ref['scenario_id'])}\` | [#{escape_cell(ref['review_id'])}](#{url}) | \`#{escape_cell(ref['evidence_path'])}\` |"
        end
      end
      out += ["", "**People and harms:** Corpus scenarios and people-linked \`SC-*\` scenarios are distinct namespaces. No persona is inferred from an \`SP-*\` pattern. Declared \`portable_assurance.harm_patterns\` values are catalogue references, not demonstrated harm to a particular person.", ""]
      out
    end

    def scenario_patterns_summary(parsed)
      patterns = parsed["patterns"].select { |p| p.is_a?(Hash) }
      out = ["## Scenario patterns", "", "These #{patterns.length} patterns describe reusable testing pressures, not observed failures.", "", "| ID | Name | Category | Description |", "|---|---|---|---|"]
      patterns.each do |pattern|
        id = pattern["id"].to_s
        next unless id.match?(/\ASP-[A-Za-z0-9-]+\z/)
        out << "| [`#{id}`](##{id.downcase}) | #{escape_cell(pattern['name'])} | #{escape_cell(pattern['category'])} | #{escape_cell(pattern['description'])} |"
      end
      out << ""
      patterns.each do |pattern|
        id = pattern["id"].to_s
        next unless id.match?(/\ASP-[A-Za-z0-9-]+\z/)
        out += ["<a id=\"#{id.downcase}\"></a>", "", "### #{id}: #{escape_cell(pattern['name'])}", "", "**Category:** #{escape_cell(pattern['category'])}", "", escape_cell(pattern["description"]), ""]
      end
      out
    end

    def catalogue_summary(parsed)
      records = Array(parsed["records"]).select { |item| item.is_a?(Hash) }
      record_type = parsed["record_type"] || "pattern"
      out = [
        "## Catalogue metadata",
        "",
        "| Field | Value |",
        "|---|---|",
        "| Catalogue version | `#{escape_cell(parsed['catalogue_version'])}` |",
        "| Record type | `#{escape_cell(record_type)}` |",
        "| Record count | #{records.length} |",
        ""
      ]

      unless records.empty?
        out += [
          "## Pattern index",
          "",
          "| ID | Name | Family / function | Primary relationship |",
          "|---|---|---|---|"
        ]
        records.each do |record|
          family = record["family"] || record["control_function"] || record["assurance_level"] || record["privacy_classification"] || record["protected_interest"]
          relation = Array(record["harm_patterns"] || record["risk_patterns"] || record["control_patterns"] || record["evidence_patterns"] || record["guardrail_patterns"]).first(4).map { |v| "`#{v}`" }.join(", ")
          out << "| `#{escape_cell(record['id'])}` | #{escape_cell(record['name'])} | #{escape_cell(family)} | #{relation} |"
        end
      end
      out
    end

    def review_summary(review)
      target = review["target"].is_a?(Hash) ? review["target"] : {}
      findings = Array(review["findings"]).select { |item| item.is_a?(Hash) }
      summary = review["summary"].is_a?(Hash) ? review["summary"] : {}

      out = [
        "## Review metadata",
        "",
        "| Field | Value |",
        "|---|---|",
        "| Review ID | `#{escape_cell(review['id'])}` |",
        "| Status | #{escape_cell(review['status'])} |",
        "| Title | #{escape_cell(review['title'])} |",
        "| Reviewed on | #{escape_cell(review['reviewed_on'])} |",
        "| Target repository | `#{escape_cell(target['repository'])}` |",
        "| Target version | #{escape_cell(target['version'])} |",
        "| Target commit | `#{escape_cell(target['commit'])}` |",
        "| Finding count | #{findings.length} |",
        ""
      ]

      if summary["overall_assessment"]
        out += ["## Overall assessment", "", format_value(summary["overall_assessment"]), ""]
      end

      unless findings.empty?
        out += [
          "## Finding index",
          "",
          "| ID | Finding | Severity | Status | Primary disposition |",
          "|---|---|---|---|---|"
        ]
        findings.each do |finding|
          out << "| `#{escape_cell(finding['id'])}` | #{escape_cell(finding['title'])} | #{escape_cell(finding['severity'])} | #{escape_cell(finding['status'])} | #{escape_cell(finding['primary_disposition'])} |"
        end
      end
      out
    end

    def persona_summary(parsed)
      personas = Array(parsed["@graph"]).select { |item| item.is_a?(Hash) }
      out = ["## Historical personas", "", "This historical persona set contains **#{personas.length}** records. Each section below is a reader-oriented projection of the retained JSON-LD; the complete source remains available at the bottom of this page.", ""]
      personas.each do |persona|
        id = persona["@id"].to_s.split("/").last
        name = persona["name"] || id
        role = persona["role"]
        out << "### #{id}: #{name}"
        out << ""
        out << "**Role:** #{escape_cell(role)}" if role
        out << ""
        out << "> #{persona['quote']}" if persona["quote"]
        out << "" if persona["quote"]
        %w[type adversarial safeguarding safeguarding_note co_persona].each do |key|
          next unless persona.key?(key)
          out << "- **#{key.tr('_', ' ').capitalize}:** #{format_value(persona[key])}"
        end
        context = persona["context"]
        if context.is_a?(Hash) && !context.empty?
          out += ["", "#### Context", ""]
          context.each { |key, value| out << "- **#{key.tr('_', ' ').capitalize}:** #{format_value(value)}" }
        end
        %w[lifecycle_phases goals needs frustrations risk_context exploits inclusion_drivers exclusion_risks].each do |key|
          values = persona[key]
          next unless values.is_a?(Array) && !values.empty?
          out += ["", "#### #{key.tr('_', ' ').split.map(&:capitalize).join(' ')}", ""]
          values.each { |value| out << "- #{format_value(value)}" }
        end
        evidence = persona["evidence"]
        if evidence.is_a?(Array) && !evidence.empty?
          out += ["", "#### Evidence", ""]
          evidence.each do |entry|
            if entry.is_a?(Hash)
              claim = entry["claim"] || "Evidence item"
              source = entry["source"]
              url = entry["url"]
              suffix = source ? " — #{source}" : ""
              suffix += url ? " ([source](#{url}))" : ""
              out << "- #{claim}#{suffix}"
            else
              out << "- #{format_value(entry)}"
            end
          end
        end
        out << ""
      end
      out
    end

    def jsonld_graph_summary(parsed)
      entries = Array(parsed["@graph"]).select { |item| item.is_a?(Hash) }
      out = ["## Historical record overview", "", "This JSON-LD graph contains **#{entries.length}** records.", ""]
      unless entries.empty?
        out += ["| ID | Type | Name / title |", "|---|---|---|"]
        entries.each do |entry|
          id = entry["@id"].to_s.split("/").last
          type = entry["@type"]
          label = entry["name"] || entry["title"] || entry["label"] || entry["description"]
          out << "| `#{escape_cell(id)}` | #{escape_cell(type)} | #{escape_cell(label)} |"
        end
      end
      out
    end

    def format_value(value)
      case value
      when Array
        value.map { |v| format_value(v) }.join(", ")
      when Hash
        value.map { |k, v| "#{k}: #{format_value(v)}" }.join("; ")
      when TrueClass, FalseClass
        value ? "yes" : "no"
      else
        value.to_s.gsub("
", " ")
      end
    end

    def generic_summary(parsed)
      out = ["## Structured-data overview", ""]
      case parsed
      when Hash
        out << "Top-level keys: #{parsed.keys.map { |k| "`#{k}`" }.join(', ')}."
      when Array
        out << "This record contains **#{parsed.length}** top-level entries."
      else
        out << "This structured record is rendered below exactly as stored."
      end
      out
    end

    def escape_cell(value)
      value.to_s.gsub("|", "\\|").gsub("\n", " ")
    end
  end
end
