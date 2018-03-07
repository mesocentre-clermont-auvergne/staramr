import argparse
import sys
from os import path, mkdir

from staramr.SubCommand import SubCommand
from staramr.blast.BlastHandler import BlastHandler
from staramr.blast.pointfinder.PointfinderBlastDatabase import PointfinderBlastDatabase
from staramr.blast.resfinder.ResfinderBlastDatabase import ResfinderBlastDatabase
from staramr.databases.AMRDatabaseHandler import AMRDatabaseHandler
from staramr.exceptions.CommandParseException import CommandParseException

"""
Class for searching for AMR resistance genes.
"""


class Search(SubCommand):

    def __init__(self, amr_detection_factory, subparser, script_dir):
        """
        Creates a new Search sub-command instance.
        :param amr_detection_factory: A factory of type staramr.detection.AMRDetectionFactory for building necessary objects for AMR detection.
        :param subparser: The subparser to use.  Generated from argparse.ArgumentParser.add_subparsers().
        :param script_dir: The directory containing the main application script.
        """
        super().__init__(subparser, script_dir)
        self._amr_detection_factory = amr_detection_factory

    def _setup_args(self, arg_parser):
        arg_parser = self._subparser.add_parser('search', help='Search for AMR genes')

        self._default_database_dir = AMRDatabaseHandler.get_default_database_directory(self._script_dir)

        arg_parser.add_argument('--threads', action='store', dest='threads', type=int,
                                help='The number of threads to use [1].',
                                default=1, required=False)
        arg_parser.add_argument('--pid-threshold', action='store', dest='pid_threshold', type=float,
                                help='The percent identity threshold [98.0].', default=98.0, required=False)
        arg_parser.add_argument('--percent-length-overlap', action='store', dest='plength_threshold', type=float,
                                help='The percent length overlap [60.0].', default=60.0, required=False)
        arg_parser.add_argument('--pointfinder-organism', action='store', dest='pointfinder_organism', type=str,
                                help='The organism to use for pointfinder {' + ', '.join(
                                    PointfinderBlastDatabase.get_available_organisms()) + '} [None].', default=None,
                                required=False)
        arg_parser.add_argument('--include-negatives', action='store_true', dest='include_negatives',
                                help='Inclue negative results (those sensitive to antimicrobials) [False].',
                                required=False)
        arg_parser.add_argument('--database', action='store', dest='database', type=str,
                                help='The directory containing the resfinder/pointfinder databases [' + self._default_database_dir + '].',
                                default=self._default_database_dir, required=False)
        arg_parser.add_argument('--output-dir', action='store', dest='output_dir', type=str,
                                help="The output directory for results.  If unset prints all results to stdout.",
                                default=None, required=False)
        arg_parser.add_argument('files', nargs=argparse.REMAINDER)

        return arg_parser

    def _print_dataframe_to_file(self, dataframe, file=None):
        file_handle = sys.stdout

        if dataframe is not None:
            if file:
                file_handle = open(file, 'w')

            dataframe.to_csv(file_handle, sep="\t", float_format="%0.2f")

            if file:
                file_handle.close()

    def run(self, args):
        if (len(args.files) == 0):
            raise CommandParseException("Must pass a fasta file to process", self._root_arg_parser)

        if args.output_dir:
            if path.exists(args.output_dir):
                raise CommandParseException("Output directory [" + args.output_dir + "] already exists",
                                            self._root_arg_parser)
            else:
                mkdir(args.output_dir)

        if not path.isdir(args.database):
            raise CommandParseException("Database directory [" + args.database + "] does not exist")

        resfinder_database_dir = path.join(args.database, 'resfinder')
        pointfinder_database_root_dir = path.join(args.database, 'pointfinder')

        resfinder_database = ResfinderBlastDatabase(resfinder_database_dir)
        if (args.pointfinder_organism):
            if args.pointfinder_organism not in PointfinderBlastDatabase.get_available_organisms():
                raise CommandParseException("The only Pointfinder organism(s) currently supported are " + str(
                    PointfinderBlastDatabase.get_available_organisms()), self._root_arg_parser)
            pointfinder_database = PointfinderBlastDatabase(pointfinder_database_root_dir,
                                                            args.pointfinder_organism)
        else:
            pointfinder_database = None
        blast_handler = BlastHandler(resfinder_database, pointfinder_database, threads=args.threads)

        amr_detection = self._amr_detection_factory.build(resfinder_database, blast_handler, pointfinder_database,
                                                          args.include_negatives)
        amr_detection.run_amr_detection(args.files, args.pid_threshold, args.plength_threshold)

        if args.output_dir:
            self._print_dataframe_to_file(amr_detection.get_resfinder_results(),
                                          path.join(args.output_dir, "results_tab.tsv"))
            self._print_dataframe_to_file(amr_detection.get_pointfinder_results(),
                                          path.join(args.output_dir, "results_tab.pointfinder.tsv"))
            self._print_dataframe_to_file(amr_detection.get_summary_results(),
                                          path.join(args.output_dir, "summary.tsv"))
        else:
            self._print_dataframe_to_file(amr_detection.get_resfinder_results())
            self._print_dataframe_to_file(amr_detection.get_pointfinder_results())
            self._print_dataframe_to_file(amr_detection.get_summary_results())
