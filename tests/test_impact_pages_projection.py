"""Rendered pilot pages must expose status and negative outcome under GitHub Pages baseurl."""
import pathlib
import shutil
import subprocess
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]

@unittest.skipUnless(shutil.which("ruby"),"Ruby required")
class ImpactProjectionTests(unittest.TestCase):
    def test_both_corpus_projections_and_negative_dispositions(self):
        script=r'''
require "yaml"
module Jekyll
 class Page; end
 class Generator
  def self.safe(x); end
  def self.priority(x); end
 end
end
load ARGV.fetch(0)
root=ARGV.fetch(1)
site=Struct.new(:source,:config).new(root,{"baseurl"=>"/rahp-toolkit"})
gen=RahpPagesProjection::Generator.allocate
["trust-tasks", "trust-tasks-credspec-composed"].each do |name|
  corpus=YAML.safe_load(File.read(File.join(root,"corpora","#{name}.yaml")),aliases:true).fetch("corpus")
  html=gen.send(:corpus_summary,site,corpus).join("\n")
  raise "missing pathway heading" unless html.include?("Potential people-impact pathways")
  raise "missing negative status" unless html.include?("Not established")
  raise "missing provisional status" unless html.include?("Provisional")
  raise "missing safety distinction" unless html.include?("not harm severity")
  raise "missing reader guide route" unless html.include?("/rahp-toolkit/docs/reading-scenario-corpus.html")
  raise "missing reviewer route" unless html.include?("/rahp-toolkit/docs/people-impact-qualification-acceptance.html")
  raise "misleading safety claim" if html.include?("independently certified safe")
end
'''
        p=subprocess.run(["ruby","-e",script,str(ROOT/"_plugins/structured_data_pages.rb"),str(ROOT)],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)

if __name__=="__main__":unittest.main()
