import importlib.util, json, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).parents[1]

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

cmp=load_module(ROOT/"tools"/"compare_execution_benchmarks.py","cmpbench")
val=load_module(ROOT/"tools"/"validate.py","rahpvalidate")

class PerformancePolicyTests(unittest.TestCase):
    def sample(self,seconds=10.0,digest="a"):
        return {"contract":"rahp-execution-benchmark-v1","profile":"core-validation","profile_exit_code":0,
                "wall_seconds":seconds,"semantic_reference_digests":{"x":digest}}
    def test_small_noise_does_not_fail(self):
        self.assertEqual(cmp.compare(self.sample(10),self.sample(11.2))["status"],"pass")
    def test_meaningful_regression_fails(self):
        self.assertEqual(cmp.compare(self.sample(10),self.sample(13))["status"],"fail")
    def test_semantic_digest_change_is_hard_failure(self):
        r=cmp.compare(self.sample(10,"a"),self.sample(9,"b")); self.assertEqual(r["reason"],"semantic-reference-digest-mismatch")
    def test_validation_yaml_cache_eliminates_duplicate_parse(self):
        val.load_yaml.cache_clear()
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"x.yaml"; p.write_text("a: 1\n",encoding="utf-8")
            self.assertEqual(val.load_yaml(p),{"a":1}); self.assertEqual(val.load_yaml(p),{"a":1})
            info=val.load_yaml.cache_info()
            self.assertEqual(info.misses,1); self.assertEqual(info.hits,1)

if __name__=="__main__": unittest.main()
