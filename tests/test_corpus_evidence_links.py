"""Evidence-qualified reverse links reject ambiguous or ungrounded matches."""
import pathlib, shutil, subprocess, unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]

@unittest.skipUnless(shutil.which("ruby"), "Ruby needed")
class CorpusEvidenceLinksTests(unittest.TestCase):
    def test_strict_contract_and_projection(self):
        script=r'''
require "tmpdir"
require "fileutils"
require "yaml"
module Jekyll
 class Page; end
 class Generator
  def self.safe(x); end
  def self.priority(x); end
 end
end
load ARGV.fetch(1)
Dir.mktmpdir do |tmp|
 FileUtils.mkdir_p(File.join(tmp,"examples","review"))
 review={"review"=>{"id"=>"SR-DEMO","corpus_scenario_references"=>[
   {"corpus_id"=>"CORPUS-TRUST-TASKS","scenario_id"=>"TT-002","source_commit"=>"a"*40,"evidence_path"=>"findings/0/evidence/0"},
   {"corpus_id"=>"CORPUS-TRUST-TASKS","scenario_id"=>"SEC-TT-002","source_commit"=>"a"*40,"evidence_path"=>"findings/0/evidence/0"},
   {"corpus_id"=>"CORPUS-TRUST-TASKS","scenario_id"=>"TT-002","source_commit"=>"b"*40,"evidence_path"=>"findings/0/evidence/0"},
   {"corpus_id"=>"WRONG-CORPUS","scenario_id"=>"TT-002","source_commit"=>"a"*40,"evidence_path"=>"findings/0/evidence/0"},
   {"corpus_id"=>"CORPUS-TRUST-TASKS","scenario_id"=>"TT-002","source_commit"=>"a"*40,"evidence_path"=>"findings/5/evidence/0"}],
   "findings"=>[{"evidence"=>[{"observation"=>"example"}]}]}}
 File.write(File.join(tmp,"examples","review","pressure-test.yaml"),YAML.dump(review))
 corpus={"id"=>"CORPUS-TRUST-TASKS","source_commit"=>"a"*40,"scenarios"=>[{"id"=>"TT-002","title"=>"replay","primary_goal"=>"audience","priority"=>"P0","scenario_patterns"=>[]}]}
 refs=CorpusEvidenceLinks.collect(tmp)
 chosen=CorpusEvidenceLinks.for_corpus(refs,corpus)
 raise "expected one exact citation, got #{chosen.inspect}" unless chosen.size==1
 raise "no symbolic pin rejection" unless CorpusEvidenceLinks.for_corpus(refs, corpus.merge("source_commit"=>"archive-snapshot")).empty?
 gen=RahpPagesProjection::Generator.allocate
 site=Struct.new(:source,:config).new(tmp,{"baseurl"=>"/rahp-toolkit"})
 page=gen.send(:corpus_summary,site,corpus).join("\n")
 raise "missing site link" unless page.include?("/rahp-toolkit/examples/review/pressure-test/")
 raise "missing caveat" unless page.include?("does not establish a passing test")
 empty=gen.send(:corpus_summary,site,corpus.merge("source_commit"=>"c"*40)).join("\n")
 raise "missing honest no-evidence statement" unless empty.include?("No linked review evidence identified")
end
'''
        result=subprocess.run(["ruby","-e",script,str(ROOT/"_plugins/corpus_evidence_links.rb"),str(ROOT/"_plugins/structured_data_pages.rb")],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

if __name__=="__main__": unittest.main()
