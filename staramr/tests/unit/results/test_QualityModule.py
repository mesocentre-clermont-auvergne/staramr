import logging
import unittest

import pandas as pd
from os import path

from staramr.results.QualityModule import QualityModule

logger = logging.getLogger('QualityModuleTest')


class QualityModuleTest(unittest.TestCase):

    def setUp(self):
        self.genome_size_lower_bound = 4000000
        self.genome_size_upper_bound = 6000000
        self.minimum_N50_value = 10000
        self.minimum_contig_length = 1000
        self.unacceptable_num_contigs = 3
        self.test_data_dir = path.join(path.dirname(__file__), '..', 'data')

    def testN50ExactlyMinimumValue(self):
        file = path.join(self.test_data_dir, "test-N50-Exactly-Minimum-Value.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-N50-Exactly-Minimum-Value', quality_module.index[0], 'File name not equal')
        self.assertEqual(10000, quality_module['N50 value'].iloc[0], 'N50 vlaue not equal')
        self.assertEqual('Failed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('Genome length is not within the acceptable length range. N50 value is not greater than the specified minimum value. ', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')

    def testN50OneBPLargerThanMinimumValue(self):
        file = path.join(self.test_data_dir, "test-N50-One-BP-Larger-Than-Minimum-Value.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-N50-One-BP-Larger-Than-Minimum-Value', quality_module.index[0], 'File name not equal')
        self.assertEqual(10001, quality_module['N50 value'].iloc[0], 'N50 vlaue not equal')
        self.assertEqual('Failed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('Genome length is not within the acceptable length range. ', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')

    def testN50SmallerThanMinimumValue(self):
        file = path.join(self.test_data_dir, "test-N50-Smaller-Than-Minimum-Value.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-N50-Smaller-Than-Minimum-Value', quality_module.index[0], 'File name not equal')
        self.assertEqual(100, quality_module['N50 value'].iloc[0], 'N50 vlaue not equal')
        self.assertEqual('Failed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('Genome length is not within the acceptable length range. N50 value is not greater than the specified minimum value. Number of Contigs with a length less than the minimum length exceeds the acceptable number. ', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')

    def testN50MuchLargerThanMinimumValue(self):
        file = path.join(self.test_data_dir, "test-N50-Much-Larger-Than-Minimum-Value.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-N50-Much-Larger-Than-Minimum-Value', quality_module.index[0], 'File name not equal')
        self.assertEqual(100000, quality_module['N50 value'].iloc[0], 'N50 vlaue not equal')
        self.assertEqual('Failed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('Genome length is not within the acceptable length range. ', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')

    def testN50Calculation(self):
        #tests to make sure N50 contig length +all contig lengths greater than it >= half of genome length, here we are testing the = part
        file = path.join(self.test_data_dir, "test-N50-Calculation.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-N50-Calculation', quality_module.index[0], 'File name not equal')
        self.assertEqual(10002, quality_module['N50 value'].iloc[0], 'N50 vlaue not equal')
        self.assertEqual('Failed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('Genome length is not within the acceptable length range. ', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')

    def testN50UnaffectedByEmptyContigs(self):
        file = path.join(self.test_data_dir, "test-N50-Unaffected-By-Empty-Contigs.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-N50-Unaffected-By-Empty-Contigs', quality_module.index[0], 'File name not equal')
        self.assertEqual(10001, quality_module['N50 value'].iloc[0], 'N50 vlaue not equal')
        self.assertEqual('Failed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('Genome length is not within the acceptable length range. ', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')

    def testGenomeSizeExactlyMinimum(self):
        file = path.join(self.test_data_dir, "test-Genome-Size-Exactly-Minimum.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-Genome-Size-Exactly-Minimum', quality_module.index[0], 'File name not equal')
        self.assertEqual(4000000, quality_module['Genome Length'].iloc[0], 'Genome length not equal')
        self.assertEqual('Passed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')

    def testGenomeSizeExactlyMaximum(self):
        file = path.join(self.test_data_dir, "test-Genome-Size-Exactly-Maximum.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-Genome-Size-Exactly-Maximum', quality_module.index[0], 'File name not equal')
        self.assertEqual(6000000, quality_module['Genome Length'].iloc[0], 'Genome length not equal')
        self.assertEqual('Passed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')

    def testGenomeSizeWithinAcceptedRange(self):
        file = path.join(self.test_data_dir, "test-Genome-Size-Within-Accepted-Range.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-Genome-Size-Within-Accepted-Range', quality_module.index[0], 'File name not equal')
        self.assertEqual(5000000, quality_module['Genome Length'].iloc[0], 'Genome length not equal')
        self.assertEqual('Passed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')

    def testGenomeSizeSmallerThanMinimum(self):
        file = path.join(self.test_data_dir, "test-Genome-Size-Smaller-Than-Minimum.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-Genome-Size-Smaller-Than-Minimum', quality_module.index[0], 'File name not equal')
        self.assertEqual(2000000, quality_module['Genome Length'].iloc[0], 'Genome length not equal')
        self.assertEqual('Failed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('Genome length is not within the acceptable length range. ', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')

    def testGenomeSizeLargerThanMaximum(self):
        file = path.join(self.test_data_dir, "test-Genome-Size-Larger-Than-Maximum.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-Genome-Size-Larger-Than-Maximum', quality_module.index[0], 'File name not equal')
        self.assertEqual(7000000, quality_module['Genome Length'].iloc[0], 'Genome length not equal')
        self.assertEqual('Failed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('Genome length is not within the acceptable length range. ', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')

    def testGenomeSizeUnaffectedByEmptyContigs(self):
        file = path.join(self.test_data_dir, "test-Genome-Size-Unaffected-By-Empty-Contigs.fasta")
        files = [file]
        quality_module = QualityModule(files,self.genome_size_lower_bound,self.genome_size_upper_bound,self.minimum_N50_value,self.minimum_contig_length,self.unacceptable_num_contigs)
        quality_module=quality_module._create_quality_module_dataframe()
        self.assertEqual(1, len(quality_module.index), 'Invalid number of rows in results')
        self.assertEqual('test-Genome-Size-Unaffected-By-Empty-Contigs', quality_module.index[0], 'File name not equal')
        self.assertEqual(6000000, quality_module['Genome Length'].iloc[0], 'Genome length not equal')
        self.assertEqual('Passed', quality_module['Quality Module'].iloc[0], 'Quality result not equal')
        self.assertEqual('', quality_module['Quality Module Feedback'].iloc[0], 'Quality feedback not equal')