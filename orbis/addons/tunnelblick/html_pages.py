import os
from palettable.tableau import Tableau_20
from operator import itemgetter

from orbis import app
from orbis.lib import files
from orbis.core.rucksack import Rucksack
from orbis.plugins.aggregation.serial_corpus import Module as SerialCorpus
from orbis.plugins.aggregation.gold_gs import Module as GoldGS
from .html_templates import html_body


class HTMLPages(object):

    def __init__(self, corpus_name, corpus_path):
        super(HTMLPages, self).__init__()
        self.rucksack = Rucksack()

        self.corpus_name = corpus_name
        self.corpus_path = corpus_path
        self.data = self.rucksack.open['data']

        self.text_path = os.path.join(self.corpus_path, "corpus/")
        self.gold_path = os.path.join(self.corpus_path, "gold/")
        self.rucksack.pack_corpus(SerialCorpus(self.rucksack, path=self.text_path).run())
        self.rucksack.pack_gold(GoldGS(self.rucksack, path=self.gold_path).run())

        self.folder = os.path.join(app.paths.output_path, "tunnelblick", corpus_name)
        self.queue = self.rucksack.get_keys()

    def _get_keys(self, item):
        keys = set()
        for entity in item['gold']:
            keys.add(entity['key'])
        return keys

    def _get_sf_colors(self, keys):

        sf_colors = {}
        colour_idx = 0
        for sf in keys:
            sf_colors[sf] = Tableau_20.hex_colors[colour_idx]
            colour_idx = 0 if colour_idx == 19 else colour_idx + 1
        return sf_colors

    def _get_gold_entities(self, item, sf_colors, gold_html):

        gold_entities = []
        if len(item['gold']) > 0:
            last_start = int(len(item['corpus']))
            last_end = int(len(item['corpus']))
            # last_word = ""

            for entity in sorted(item['gold'], key=itemgetter("end"), reverse=True):

                start_tag = '<abbr title="{}" style="background-color:{};">'.format(entity['key'], sf_colors[entity['key']])
                end_tag = '</abbr>'

                if int(entity['start']) <= int(last_start):
                    if int(entity['start']) < int(last_end):
                        entity_start = int(entity['start'])
                    else:
                        entity_start = False
                else:
                    entity_start = False

                if int(entity['end']) < int(last_end):
                    if int(entity['end']) < int(last_start):
                        entity_end = int(entity['end'])
                    else:
                        entity_end = False
                else:
                    entity_end = False

                if isinstance(entity_start, int) and entity_end:
                    gold_html = gold_html[:int(entity['end'])] + end_tag + gold_html[int(entity['end']):]
                    gold_html = gold_html[:int(entity['start'])] + start_tag + gold_html[int(entity['start']):]
                else:
                    if len(entity['key']) > 0:
                        overlap_warning = '<abbr title="{}" style="background-color:{};"><b>&#x22C2;</b></abbr>'.format(entity['key'], sf_colors[entity['key']])
                        gold_html = gold_html[:int(last_start)] + overlap_warning + gold_html[int(last_start):]

                last_start = entity_start or last_start
                last_end = entity_end or last_end

                gold_entities.append({
                    "surfaceForm": entity['surfaceForm'],
                    "key": entity['key'],
                    "start": entity['start'],
                    "end": entity['end'],
                    "entity_type": entity['entity_type'],
                    "background": sf_colors[entity['key']]})
        return gold_entities, gold_html

    def _get_gold_html(self, item, sf_colors):

        gold_html = item['corpus']
        gold_entities, gold_html = self._get_gold_entities(item, sf_colors, gold_html)

        gold_entities_html = ""
        for entity in list(reversed(gold_entities)):
            gold_entities_html += '<p><span style="background-color:{background};"><b>{surfaceForm}</b></span> (<a href="{key}">{key}</a>): {start} - {end}: {entity_type}</p>'.format(**entity)

        return gold_html, gold_entities_html

    def _get_next_button(self, key):

        if key:
            next_item = os.path.join(str(key) + ".html")
            next_button = """<p><a id="next_page_link" class="btn btn-secondary" href="{url}" role="button" style="float: right;">Next Item &raquo;</a></p>""".format(url=next_item)
        else:
            next_button = ""

        return next_button

    def _get_previous_button(self, key):

        if key:
            previous_item = os.path.join(str(key) + ".html")
            previous_button = """<p><a id="previous_page_link" class="btn btn-secondary" href="{url}" role="button">&laquo; Previous Item</a></p>""".format(url=previous_item)
        else:
            previous_button = ""

        return previous_button

    def _build_html_page(self, item, next_item, previous_item, sf_colors):

        key = item['index']

        gold_html, gold_entities_html = self._get_gold_html(item, sf_colors)

        previous_button = self._get_previous_button(previous_item)
        next_button = self._get_next_button(next_item)
        html_item_dict = {
            "gold_html": gold_html,
            "gold_entities_html": gold_entities_html,
            "prev": previous_button, "next": next_button, "item_number": key
        }

        html = html_body.format(**html_item_dict)

        return html

    def run(self):

        timestamp = files.get_timestamp()
        folder_dir = os.path.join(self.folder + f"-{timestamp}")
        files.create_folder(folder_dir)

        app.logger.debug("Building Tunnelblick HTML pages")

        for item_key in self.queue:
            item = self.rucksack.itemview(item_key)

            try:
                next_item = self.queue[self.queue.index(item_key) + 1]
            except IndexError:
                next_item = self.queue[0]

            try:
                previous_item = self.queue[self.queue.index(item_key) - 1]
                with open("Exception.txt", "w") as of:
                    of.write(self.queue[self.queue.index(item_key) - 1])
            except IndexError as error:
                previous_item = None

            key = item['index']

            keys = self._get_keys(item)
            sf_colors = self._get_sf_colors(keys)
            html = self._build_html_page(item, next_item, previous_item, sf_colors)

            file_dir = os.path.join(folder_dir, str(key) + ".html")

            app.logger.debug(file_dir)
            with open(file_dir, "w") as open_file:
                open_file.write(html)

        app.logger.info("Finished building HTML pages")
