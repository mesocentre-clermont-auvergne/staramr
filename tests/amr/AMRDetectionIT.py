from os import path

import unittest

from amr.AMRDetection import AMRDetection
from amr.blast.BlastHandler import BlastHandler
from amr.blast.pointfinder.PointfinderBlastDatabase import PointfinderBlastDatabase
from amr.blast.resfinder.ResfinderBlastDatabase import ResfinderBlastDatabase

class AMRDetectionIT(unittest.TestCase):

    def setUp(self):
        resfinder_database_dir = path.join("databases", "resfinder")
        pointfinder_database_root_dir = path.join("databases", "pointfinder")

        resfinder_database = ResfinderBlastDatabase(resfinder_database_dir)
        pointfinder_database = None
        blast_handler = BlastHandler(resfinder_database, pointfinder_database, threads=2)

        self.amr_detection = AMRDetection(resfinder_database, blast_handler, pointfinder_database)

        self.test_data_dir = path.join("tests", "data")

    def testResfinderBetaLactam(self):
        files = [path.join(self.test_data_dir, "beta-lactam-blaIMP-42.fsa")]
        self.amr_detection.run_amr_detection(files, 98, 90)

        resfinder_results = self.amr_detection.get_resfinder_results()
        self.assertEqual(len(resfinder_results.index), 1, 'Wrong number of rows in result')

        result = resfinder_results[resfinder_results['GENE'] == 'blaIMP-42']['RESFINDER_PHENOTYPE']
        self.assertEqual(result.size, 1, 'Wrong number of results detected')
        self.assertEqual(result.iloc[0], 'Beta-lactam resistance', 'Wrong phenotype')

if __name__ == '__main__':
    unittest.main()