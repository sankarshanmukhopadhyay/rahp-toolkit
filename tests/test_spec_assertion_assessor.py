import sys
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))

from text_assertion_probe import execute
from evidence_assertion_assessor import assess

class SpecAssertionAssessorTests(unittest.TestCase):
    def test_bounded_pass_and_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'spec.md').write_text('Clients MUST use context-bound tokens.\n',encoding='utf-8')
            probe={'requirements':[{'id':'ER-1','paths':['*.md'],'assertions':[{'id':'bounded','pattern':'MUST use context-bound tokens','expected_present':True}]}]}
            evidence=execute(probe,root)
            surfaces=evidence['requirements']['ER-1']['surfaces']
            result='SATISFIED' if all(v['classification']=='satisfied' for v in surfaces.values()) else 'ABSENT'
            ledger={'requirements':[{'requirement_id':'ER-1','attempt_state':'EXECUTED','result':result}]}
            self.assertEqual(assess({'requirement_ids':['ER-1']},ledger)['outcome'],'PASS')
            (root/'spec.md').write_text('Clients may use tokens.\n',encoding='utf-8')
            evidence=execute(probe,root); surfaces=evidence['requirements']['ER-1']['surfaces']; result='SATISFIED' if all(v['classification']=='satisfied' for v in surfaces.values()) else 'ABSENT'
            ledger={'requirements':[{'requirement_id':'ER-1','attempt_state':'EXECUTED','result':result}]}
            self.assertEqual(assess({'requirement_ids':['ER-1']},ledger)['outcome'],'FAIL')

    def test_missing_evidence_is_indeterminate(self):
        self.assertEqual(assess({'requirement_ids':['ER-1']},{'requirements':[]})['outcome'],'INDETERMINATE')

if __name__=='__main__': unittest.main()
