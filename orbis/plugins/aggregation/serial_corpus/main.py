import glob
import os
from orbis import app


class SerialCorpus(object):

    def __init__(self, rucksack, path=None):
        super(SerialCorpus, self).__init__()
        self.rucksack = rucksack
        if not path:
            self.corpus_path = self.rucksack.open['config']['corpus_path']
        else:
            self.corpus_path = path

    def run(self):
        corpus = {}
<<<<<<< HEAD
        corpus_path = os.path.abspath(os.path.join(self.rucksack.open['config']['corpus_path'], '*.txt'))
        for file_dir in glob.glob(corpus_path):
=======

        for file_dir in glob.glob(os.path.abspath(os.path.join(self.corpus_path, '*.txt'))):
>>>>>>> dev/master
            try:
                file_number = file_dir.split('/')[-1].split('.')[0]
                with open(file_dir) as open_file:
                    corpus[file_number] = open_file.read()
            except Exception as exception:
                app.logger.error(f"Corpus file empty: {file_dir} ({exception})")
        return corpus
