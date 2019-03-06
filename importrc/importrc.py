import argparse
import sys
from zipfile import ZipFile
import os
import shutil
from glob import glob

import wget


class Importer:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='One command to import your dotfiles from GitHub'
        )
        self.parser.add_argument(
            'username',
            default='',
            help='GitHub username to import from'
        )
        self.parser.add_argument(
            '-m', '--merge',
            dest='merge',
            action='store_true',
            help='Merge directories (will overwrite files)'
        )

    def __call__(self, args=None):
        if args is None:
            args = sys.argv[1:]
        try:
            return self.main(self.parser.parse_args(args)) or 0
        except argparse.ArgumentError as e:
            # argparse errors are already nicely formatted, print to stderr and
            # exit with code 2
            raise e
        except Exception as e:
            raise
            # Output anything else nicely formatted on stderr and exit code 1
            self.parser.exit(1, '{prog}: error: {message}\n'.format(
                prog=self.parser.prog, message=e)
            )

    def main(self, args):
        if not args.username:
            print('No username specified')
            exit(1)
        if args.merge:
            print('Merge not supported yet')
        zipfile = self.download_zip(args.username)
        self.copy_files_to_homedir(zipfile)

    def download_zip(self, username):
        url = 'https://github.com/{}/importrc/archive/master.zip'.format(
            username
        )
        return wget.download(url, out='/tmp', bar=None)

    def copy_files_to_homedir(self, zipfile):
        with ZipFile(zipfile) as zf:
            zf.extractall(path='/tmp')
        os.remove(zipfile)
        files = (glob('/tmp/importrc-master/*') +
                 glob('/tmp/importrc-master/.*'))
        homedir = os.path.expanduser('~')
        for f in files:
            filename = f.split('/')[-1]
            new = os.path.join(homedir, filename)
            try:
                os.renames(f, new)
                print('Copied {}'.format(filename))
            except OSError:
                print('Skipping {} - use with --merge to overwrite'.format(
                    filename)
                )
        try:
            shutil.rmtree('/tmp/importrc-master/')
        except FileNotFoundError:
            pass



main = Importer()
