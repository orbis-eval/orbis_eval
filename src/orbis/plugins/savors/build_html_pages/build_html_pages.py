from orbis import app
from orbis.libs.files_lib import build_file_name
from orbis.libs.files_lib import create_folder
from .html_templates import html_body

import os
from palettable.tableau import Tableau_20
from operator import itemgetter


def run(yaml_config: dict, data: dict, results: dict) -> None:
    """ Builds the HTML Pages displaying the gold standard annotated
    text next to the text with the computed annotation.

    :param results:
    :param data:
    :param yaml_config:

    """
    # return False

    app.logger.info("Building HTML pages")

    directory_name = build_file_name("html/", yaml_config)
    create_folder(directory_name)

    for key, content in data.items():
        # print("Building HTML for {}".format(key))

        text = content["corpus"]
        computed_html = text
        gold_html = text

        keys = set()
        for entity in content["gold"]:
            keys.add(entity["key"])
        for entity in content["computed"]:
            keys.add(entity["key"])

        sf_colors = {}
        c_idx = 0
        for sf in keys:
            sf_colors[sf] = Tableau_20.hex_colors[c_idx]
            if c_idx == 19:
                c_idx = 0
            else:
                c_idx += 1

        gold_entities = []
        if len(content["gold"]) > 0:
            last_start = int(len(content["corpus"]))
            last_end = int(len(content["corpus"]))
            last_word = ""

            for entity in sorted(content["gold"], key=itemgetter("end"), reverse=True):

                if entity["entity_type"] not in yaml_config["scorer"]["entities"] and len(yaml_config["scorer"]["entities"]) > 0:
                    continue

                start_tag = '<abbr title="{}" style="background-color:{};">'.format(entity["key"], sf_colors[entity["key"]])
                end_tag = '</abbr>'

                if int(entity["start"]) <= int(last_start):
                    if int(entity["start"]) < int(last_end):
                        entity_start = int(entity["start"])
                    else:
                        entity_start = False
                        case = 1
                        # print("{}\t-\t{}: {} (1)\n{}\t-\t{}: {}".format(entity["start"], entity["end"], entity["surfaceForm"], last_start, last_end, last_word))
                else:
                    entity_start = False
                    case = 2
                    # print("{}\t-\t{}: {} (2)\n{}\t-\t{}: {}".format(entity["start"], entity["end"], entity["surfaceForm"], last_start, last_end, last_word))

                if int(entity["end"]) < int(last_end):
                    if int(entity["end"]) < int(last_start):
                        entity_end = int(entity["end"])
                    else:
                        entity_end = False
                        case = 3
                        # print("{}\t-\t{}: {} (3)\n{}\t-\t{}: {}".format(entity["start"], entity["end"], entity["surfaceForm"], last_start, last_end, last_word))
                else:
                    entity_end = False
                    case = 4
                    # print("{}\t-\t{}: {} (4)\n{}\t-\t{}: {}".format(entity["start"], entity["end"], entity["surfaceForm"], last_start, last_end, last_word))

                if isinstance(entity_start, int) and entity_end:
                    gold_html = gold_html[:int(entity["end"])] + end_tag + gold_html[int(entity["end"]):]
                    gold_html = gold_html[:int(entity["start"])] + start_tag + gold_html[int(entity["start"]):]
                else:
                    if len(entity["key"]) > 0:
                        overlap_warning = '<abbr title="{}" style="background-color:{};"><b>&#x22C2;</b></abbr>'.format(entity["key"], sf_colors[entity["key"]])
                        gold_html = gold_html[:int(last_start)] + overlap_warning + gold_html[int(last_start):]
                        # print("-{}-> {}\t-\t{}: {}\n{}\t-\t{}: {}".format(case, entity["start"], entity["end"], entity["surfaceForm"], last_start, last_end, last_word))

                last_start = entity_start or last_start
                last_end = entity_end or last_end
                last_word = entity["surfaceForm"]

                gold_entities.append({
                    "surfaceForm": entity["surfaceForm"],
                    "key": entity["key"],
                    "start": entity["start"],
                    "end": entity["end"],
                    "entity_type": entity["entity_type"],
                    "background": sf_colors[entity["key"]]})

        computed_entities = []
        if len(content["computed"]) > 0:
            last_start = len(content["corpus"])
            last_end = len(content["corpus"])
            last_word = ""
            for e_idx, entity in enumerate(sorted(content["computed"], key=itemgetter("document_end"), reverse=True)):

                if entity["entity_type"] not in yaml_config["scorer"]["entities"] and len(yaml_config["scorer"]["entities"]) > 0:
                    continue

                is_fp = False
                entity_id = "{},{}".format(entity["document_start"], entity["document_end"])
                is_fp = True if entity_id in content["evaluation"]["binary_classification"]["confusion_matrix"]["fp_ids"] else False

                if is_fp:
                    start_tag = '<abbr title="{}" style="background-color:{}"><s>'.format(entity["key"], sf_colors[entity["key"]])
                    end_tag = '</s></abbr>'
                else:
                    start_tag = '<abbr title="{}" style="background-color:{}">'.format(entity["key"], sf_colors[entity["key"]])
                    end_tag = '</abbr>'

                if int(entity["document_start"]) <= int(last_start):
                    if int(entity["document_start"]) < int(last_end):
                        entity_start = int(entity["document_start"])
                    else:
                        entity_start = False
                        case = 1
                        # print("{}\t-\t{}: {} (1)\n{}\t-\t{}: {}".format(entity["document_start"], entity["document_end"], entity["surfaceForm"], last_start, last_end, last_word))
                else:
                    entity_start = False
                    case = 2
                    # print("{}\t-\t{}: {} (2)\n{}\t-\t{}: {}".format(entity["document_start"], entity["document_end"], entity["surfaceForm"], last_start, last_end, last_word))

                if int(entity["document_end"]) < int(last_end):
                    if int(entity["document_end"]) < int(last_start):
                        entity_end = int(entity["document_end"])
                    else:
                        entity_end = False
                        case = 3
                        # print("{}\t-\t{}: {} (3)\n{}\t-\t{}: {}".format(entity["document_start"], entity["document_end"], entity["surfaceForm"], last_start, last_end, last_word))
                else:
                    entity_end = False
                    case = 4
                    # print("{}\t-\t{}: {} (4)\n{}\t-\t{}: {}".format(entity["document_start"], entity["document_end"], entity["surfaceForm"], last_start, last_end, last_word))

                if isinstance(entity_start, int) and entity_end:
                    computed_html = computed_html[:int(entity["document_end"])] + end_tag + computed_html[int(entity["document_end"]):]
                    computed_html = computed_html[:int(entity["document_start"])] + start_tag + computed_html[int(entity["document_start"]):]
                else:
                    if len(entity["key"]) > 0:
                        if is_fp:
                            overlap_warning = '<abbr title="{}" style="background-color:{};"><s><b>&#x22C2;</b></s></abbr>'.format(entity["key"], sf_colors[entity["key"]])
                        else:
                            overlap_warning = '<abbr title="{}" style="background-color:{};"><b>&#x22C2;</b></abbr>'.format(entity["key"], sf_colors[entity["key"]])
                        computed_html = computed_html[:int(last_start)] + overlap_warning + computed_html[int(last_start):]
                        # print("[orbis] -{}-> {}\t-\t{}: {}\n{}\t-\t{}: {}".format(case, entity["document_start"], entity["document_end"], entity["surfaceForm"], last_start, last_end, last_word))

                last_start = entity_start or last_start
                last_end = entity_end or last_end
                last_word = entity["surfaceForm"]

                computed_entities.append({
                    "surfaceForm": entity["surfaceForm"],
                    "key": entity["key"],
                    "start": entity["document_start"],
                    "end": entity["document_end"],
                    "entity_type": entity["entity_type"],
                    "background": sf_colors[entity["key"]]})

        header_dict_0 = {
            "aggregator_name": yaml_config["aggregator"]["service"]["name"],
            "aggregator_profile": yaml_config["aggregator"]["service"].get("profile", "None"),
            "aggregator_limit": yaml_config["aggregator"]["service"].get("limit", "None"),
            "aggregator_location": yaml_config["aggregator"]["service"]["location"]
        }

        header_dict_1 = {
            "aggregator_data_set": yaml_config["aggregator"]["input"]["data_set"]["name"],
            "evaluator_name": yaml_config["evaluator"]["name"],
            "scorer_name": yaml_config["scorer"]["name"],
            "entities": ", ".join([e for e in yaml_config["scorer"]["entities"]])
        }

        header_dict_2 = {
            "has_score": results["has_score"],
            "no_score": results["no_score"],
            "empty_responses": results["empty_responses"]
        }

        micro_precision = f"{results['binary_classification']['micro']['precision']:.3f}"
        macro_precision = f"{results['binary_classification']['macro']['precision']:.3f}"
        micro_macro_precision = "(" + "/".join([str(micro_precision), str(macro_precision)]) + ")"

        micro_recall = f"{results['binary_classification']['micro']['recall']:.3f}"
        macro_recall = f"{results['binary_classification']['macro']['recall']:.3f}"
        micro_macro_recall = "(" + "/".join([str(micro_recall), str(macro_recall)]) + ")"

        micro_f1_score = f"{results['binary_classification']['micro']['f1_score']:.3f}"
        macro_f1_score = f"{results['binary_classification']['macro']['f1_score']:.3f}"
        micro_macro_f1_score = "(" + "/".join([str(micro_f1_score), str(macro_f1_score)]) + ")"

        header_dict_3 = {
            "precision": micro_macro_precision,
            "recall": micro_macro_recall,
            "f1_score": micro_macro_f1_score,
        }

        header_dict_4 = {
            "precision": content["evaluation"]["binary_classification"]["precision"],
            "recall": content["evaluation"]["binary_classification"]["recall"],
            "f1_score": content["evaluation"]["binary_classification"]["f1_score"]
        }

        header_dict_5 = {
            "tp": sum(content["evaluation"]["binary_classification"]["confusion_matrix"]["tp"]),
            "fp": sum(content["evaluation"]["binary_classification"]["confusion_matrix"]["fp"]),
            "fn": sum(content["evaluation"]["binary_classification"]["confusion_matrix"]["fn"])
        }

        header_html_0 = """
        <b>Aggregator Name:</b>\t{aggregator_name}</br>
        <b>Aggregator Profile:</b>\t{aggregator_profile}</br>
        <b>Aggregator Limit:</b>\t{aggregator_limit}</br>
        <b>Aggregator Service:</b>\t{aggregator_name}</br>
        """.format(**header_dict_0)

        header_html_1 = """
        <b>Aggregator Dataset:</b>\t{aggregator_data_set}</br>
        <b>Evaluator Name:</b>\t{evaluator_name}</br>
        <b>Scorer Name:</b>\t{scorer_name}</br>
        <b>Entities:</b>\t{entities}</br>
        """.format(**header_dict_1)

        header_html_2 = """
        <b>Some Score:</b>\t{has_score}</br>
        <b>No Score:</b>\t{no_score}</br>
        <b>Empty Responses:</b>\t{empty_responses}</br>
        """.format(**header_dict_2)

        header_html_3 = """
        <b>Precision (micro/macro):</b>\t{precision}</br>
        <b>Recall (micro/macro):</b>\t{recall}</br>
        <b>F1 Score (micro/macro):</b>\t{f1_score}</br>
        """.format(**header_dict_3)

        header_html_4 = """
        <b>Precision:</b>\t{precision:.3f}</br>
        <b>Recall:</b>\t{recall:.3f}</br>
        <b>F1 Score:</b>\t{f1_score:.3f}</br>
        """.format(**header_dict_4)

        header_html_5 = """
        <b>True Positives:</b>\t{tp}</br>
        <b>False Positives:</b>\t{fp}</br>
        <b>False Negatives:</b>\t{fn}</br>
        """.format(**header_dict_5)

        gold_entities_html = ""
        for entity in list(reversed(gold_entities)):
            gold_entities_html += '<p><span style="background-color:{background};"><b>{surfaceForm}</b></span> (<a href="{key}">{key}</a>): {start} - {end}: {entity_type}</p>'.format(**entity)

        computed_entities_html = ""
        for entity in list(reversed(computed_entities)):
            computed_entities_html += '<p><span style="background-color:{background};"><b>{surfaceForm}</b></span> (<a href="{key}">{key}</a>): {start} - {end}: {entity_type}</p>'.format(**entity)

        if data.get(str(int(key) - 1)):
            previous_item = os.path.join(str(int(key) - 1) + ".html")
            previous_html = """<p><a id="previous_page_link" class="btn btn-secondary" href="{url}" role="button">&laquo; Previous Item</a></p>""".format(url=previous_item)
        else:
            previous_html = ""

        if data.get(str(int(key) + 1)):
            next_item = os.path.join(str(int(key) + 1) + ".html")
            next_html = """<p><a id="next_page_link" class="btn btn-secondary" href="{url}" role="button" style="float: right;">Next Item &raquo;</a></p>""".format(url=next_item)
        else:
            next_html = ""

        html_content_dict = {
            "header_html_0": header_html_0, "header_html_1": header_html_1,
            "header_html_2": header_html_2, "header_html_3": header_html_3,
            "header_html_4": header_html_4, "header_html_5": header_html_5,
            "gold_html": gold_html, "computed_html": computed_html,
            "gold_entities_html": gold_entities_html, "computed_entities_html": computed_entities_html,
            "prev": previous_html, "next": next_html, "item_number": key
        }

        html = html_body.format(**html_content_dict)

        file_dir = os.path.join(directory_name, str(key) + ".html")
        with open(file_dir, "w") as open_file:
            open_file.write(html)

    app.logger.info("Finished building HTML pages")
