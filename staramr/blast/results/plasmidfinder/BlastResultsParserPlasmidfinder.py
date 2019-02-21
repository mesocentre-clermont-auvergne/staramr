from os import path

from staramr.blast.results.BlastResultsParser import BlastResultsParser
from staramr.blast.results.plasmidfinder.PlasmidfinderHitHSP import PlasmidfinderHitHSP

"""
Class used to parse out BLAST results for Plasmidfinder.
"""

class BlastResultsParserPlasmidfinder(BlastResultsParser):
    COLUMNS = [x.strip() for x in '''
    Isolate ID
    Gene
    %Identity
    %Overlap
    HSP Length/Total Length
    Contig
    Start
    End
    Accession
    '''.strip().split('\n')]
    SORT_COLUMNS = ['Isolate ID', 'Gene']

    def __init__(self, file_blast_map, blast_database, pid_threshold, plength_threshold, report_all=False,
                 output_dir=None, genes_to_exclude=[]):
        """
        Creates a new BlastResultsParserPlasmidfinder.
        :param file_blast_map: A map/dictionary linking input files to BLAST results files.
        :param blast_database: The particular staramr.blast.AbstractBlastDatabase to use.
        :param pid_threshold: A percent identity threshold for BLAST results.
        :param plength_threshold: A percent length threshold for results.
        :param report_all: Whether or not to report all blast hits.
        :param output_dir: The directory where output files are being written.
        :param genes_to_exclude: A list of gene IDs to exclude from the results.
        """
        super().__init__(file_blast_map, blast_database, pid_threshold, plength_threshold, report_all,
                         output_dir=output_dir, genes_to_exclude=genes_to_exclude)

    def _create_hit(self, file, database_name, blast_record) -> PlasmidfinderHitHSP:
        return PlasmidfinderHitHSP(file, blast_record)

    def _get_result_rows(self, hit, database_name) -> list:
        return [[hit.get_genome_id(),
                 hit.get_amr_gene_name(),
                 hit.get_pid(),
                 hit.get_plength(),
                 str(hit.get_hsp_length()) + "/" + str(hit.get_amr_gene_length()),
                 hit.get_genome_contig_id(),
                 hit.get_genome_contig_start(),
                 hit.get_genome_contig_end(),
                 hit.get_amr_gene_accession()
                 ]]

    def _get_out_file_name(self, in_file) -> str:
        if self._output_dir:
            return path.join(self._output_dir, 'plasmidfinder_' + path.basename(in_file))
        else:
            raise Exception("output_dir is None")
