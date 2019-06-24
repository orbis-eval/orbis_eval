#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from operator import itemgetter
from palettable.tableau import Tableau_20
from typing import Tuple, Dict, List, Any
import csv
import datetime
import glob
import json
import os

from orbis.addons.satyanweshi import templates
from orbis.config.paths import output_path


def run(args=None):
    print(type(args))
    if not args or not args.input:
        response = str(input(f"Search for json item files in {output_path}? (Y/n)")).lower()
        while response not in ["y", "j", "n"] and len(response) > 0:
            response = str(input(f"Response {response}({type(response)}) invalid.\nSearch for json item files in {output_path}? (Y/n)")).lower()
        if response == "y" or response == "j" or len(response) == 0:
            source_dir = output_path
        else:
            source_dir = str(input("Please enter directory to search for json item files:\n"))
            while not os.path.isdir(source_dir):
                source_dir = str(input("Input not a directory. Please enter directory to search for json item files:\n"))
        files = sorted(glob.glob(os.path.join(source_dir, "*.json")))
        print("\nPlease choose two files to compare: ")
        for idx, file in enumerate(files):
            space = 5 - len(str(idx))
            print(f"[{idx}]{space * ' '}{file.split('/')[-1]}")

        def file_selection():
            response = input("\nEnter numbers of selection seperated by space (e.g. 23 42)")
            file_a = int(response.split(" ")[0])
            file_b = int(response.split(" ")[1])
            print(f"\nYou chose to compare:\n[{file_a}] {files[file_a].split('/')[-1]}\nwith\n[{file_b}] {files[file_b].split('/')[-1]}")
            response = str(input("Is this correct? (Y/n)")).lower()
            if response == "y" or response == "j" or len(response) == 0:
                return files[file_a], files[file_b]
            else:
                file_selection()

        files = file_selection()
    else:
        files = args.input.split(",")
    print("Loading files. Please wait...")
    jsons = load_jsons(files)
    print("Files loaded. Building html now.")
    build_html_pages(jsons)
    print("Build complete. Have a nice day!")


def load_jsons(files):
    result = []
    for file in files:
        data = json.load(open(file))
        result.append(data)
    return result


def get_sf_colours(content, keys=None):
    keys = keys or set()
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
    return keys, sf_colors


def get_gold_entities(content, config, sf_colors) -> Tuple[Any, List[Dict[str, Any]]]:
    html = content["corpus"]
    entities = []
    if len(content["gold"]) > 0:
        last_start = int(len(content["corpus"]))
        last_end = int(len(content["corpus"]))
        for entity in sorted(content["gold"], key=itemgetter("end"), reverse=True):
            if entity["entity_type"] not in config["scorer"]["entities"] and len(config["scorer"]["entities"]) > 0:
                continue
            start_tag = f'<abbr title="{entity["key"]}" style="background-color:{sf_colors[entity["key"]]};">'
            end_tag = '</abbr>'
            if int(entity["start"]) <= int(last_start):
                if int(entity["start"]) < int(last_end):
                    entity_start = int(entity["start"])
                else:
                    entity_start = False
            else:
                entity_start = False
            if int(entity["end"]) < int(last_end):
                if int(entity["end"]) < int(last_start):
                    entity_end = int(entity["end"])
                else:
                    entity_end = False
            else:
                entity_end = False
            if isinstance(entity_start, int) and entity_end:
                html = html[:int(entity["end"])] + end_tag + html[int(entity["end"]):]
                html = html[:int(entity["start"])] + start_tag + html[int(entity["start"]):]
            else:
                if len(entity["key"]) > 0:
                    overlap_warning = f'<abbr title="{entity["key"]}" style="background-color:{sf_colors[entity["key"]]};"><b>&#x22C2;</b></abbr>'
                    html = html[:int(last_start)] + overlap_warning + html[int(last_start):]
            last_start = entity_start or last_start
            last_end = entity_end or last_end
            entities.append({
                "surfaceForm": entity["surfaceForm"],
                "key": entity["key"],
                "start": entity["start"],
                "end": entity["end"],
                "background": sf_colors[entity["key"]]})
    return html, entities


def get_computed_entities(content, config, sf_colors) -> Tuple[Any, List[Dict[str, Any]]]:
    html = content["corpus"]
    entities = []
    if len(content["computed"]) > 0:
        last_start = len(content["corpus"])
        last_end = len(content["corpus"])
        for e_idx, entity in enumerate(sorted(content["computed"], key=itemgetter("document_end"), reverse=True)):
            if entity["entity_type"] not in config["scorer"]["entities"] and len(config["scorer"]["entities"]) > 0:
                continue
            entity_id = "{},{}".format(
                entity["document_start"], entity["document_end"])
            is_fp = True if entity_id in content["evaluation"][
                "precision_and_recall"]["confusion_matrix"]["fp_ids"] else False
            if is_fp:
                start_tag = f'<abbr title="{entity["key"]}" style="background-color:{sf_colors[entity["key"]]}"><s>'
                end_tag = '</s></abbr>'
            else:
                start_tag = f'<abbr title="{entity["key"]}" style="background-color:{sf_colors[entity["key"]]}">'
                end_tag = '</abbr>'
            if int(entity["document_start"]) <= int(last_start):
                if int(entity["document_start"]) < int(last_end):
                    entity_start = int(entity["document_start"])
                else:
                    entity_start = False
            else:
                entity_start = False
            if int(entity["document_end"]) < int(last_end):
                if int(entity["document_end"]) < int(last_start):
                    entity_end = int(entity["document_end"])
                else:
                    entity_end = False
            else:
                entity_end = False
            if isinstance(entity_start, int) and entity_end:
                html = html[:int(entity["document_end"])] + end_tag + html[int(entity["document_end"]):]
                html = html[:int(entity["document_start"])] + start_tag + html[int(entity["document_start"]):]
            else:
                if len(entity["key"]) > 0:
                    if is_fp:
                        overlap_warning = f'<abbr title="{entity["key"]}" style="background-color:{sf_colors[entity["key"]]};"><s><b>&#x22C2;</b></s></abbr>'
                    else:
                        overlap_warning = f'<abbr title="{entity["key"]}" style="background-color:{sf_colors[entity["key"]]};"><b>&#x22C2;</b></abbr>'
                    html = html[:int(last_start)] + overlap_warning + html[int(last_start):]
            last_start = entity_start or last_start
            last_end = entity_end or last_end
            entities.append({
                "surfaceForm": entity["surfaceForm"],
                "key": entity["key"],
                "start": entity["document_start"],
                "end": entity["document_end"],
                "background": sf_colors[entity["key"]]})
    return html, entities


def get_entities_html(entities):
    entities_html = ""
    for entity in list(reversed(entities)):
        entities_html += '<p><span style="background-color:{background};"><b>{surfaceForm}</b></span> (<a href="{key}">{key}</a>): {start} - {end}</p>'.format(
            **entity)
    return entities_html


def get_prev_next_links(key, content, directory_name):
    key = int(key)
    if content.get(str(key - 1)):
        previous_item = os.path.join(
            directory_name, str(key - 1) + ".html")
        previous_html = f'<p><a id="previous_page_link" class="btn btn-secondary" href="{previous_item}" role="button">&laquo; Previous Item</a></p>'
    else:
        previous_html = ""
    if content.get(str(key + 1)):
        next_item = os.path.join(directory_name, str(key + 1) + ".html")
        next_html = f'<p><a id="next_page_link" class="btn btn-secondary" href="{next_item}" role="button" style="float: right;">Next Item &raquo;</a></p>'
    else:
        next_html = ""
    return previous_html, next_html


def build_index_rows(table, directory_name):
    print("Building index rows.")
    rows = ""
    for key in sorted(table.keys()):
        f1score_0 = float(table[key]["f1score_0"])
        f1score_1 = float(table[key]["f1score_1"])
        if f1score_0 > f1score_1:
            row_colour = "danger"
        elif f1score_0 < f1score_1:
            row_colour = "success"
        else:
            row_colour = "light"
        f1_threshold = 0.6
        bold_row = ""
        if abs(f1score_1 - f1score_0) > f1_threshold:
            bold_row = 'style="font-weight:bold"'
        table[key]["row_colour"] = row_colour
        table[key]["bold_row"] = bold_row
        rows += """
        <tr class="table-{row_colour}" {bold_row}>
          <th scope="row">{item_number}</th>
          <td>{f1score_0:.3f}</td>
          <td>{tp_0:.3f}</td>
          <td>{fp_0:.3f}</td>
          <td>{fn_0:.3f}</td>
          <td>{f1score_1:.3f}</td>
          <td>{tp_1:.3f}</td>
          <td>{fp_1:.3f}</td>
          <td>{fn_1:.3f}</td>
        </tr>
        """.format(**table[key])
    html = templates.index_body.format(rows=rows)
    file_dir = os.path.join(directory_name, "index.html")
    with open(file_dir, "w") as open_file:
        open_file.write(html)


def build_index_csv(table, directory_name):
    print("Building index csv")
    file_name = os.path.join(directory_name, "index.csv")
    with open(file_name, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        for key in sorted(table.keys()):
            row_list = [
                table[key]["item_number"],
                table[key]["f1score_0"], table[key]["tp_0"], table[key]["fp_0"], table[key]["fn_0"],
                table[key]["f1score_1"], table[key]["tp_1"], table[key]["fp_1"], table[key]["fn_1"]
            ]
            spamwriter.writerow(row_list)


def build_html_pages(data):
    config_0 = data[0]["config"]
    config_1 = data[1]["config"]
    algorithm_0 = config_0["aggregator"]["service"]["name"]
    algorithm_1 = config_1["aggregator"]["service"]["name"]
    corpus = config_0["aggregator"]["input"]["data_set"]["name"]
    file_name = f"santyanweshi - {algorithm_0} vs {algorithm_1} on {corpus} corpus"
    file_name = file_name + " - {:%Y-%m-%d_%H:%M:%S}".format(datetime.datetime.now())
    directory_name = os.path.join(output_path, file_name)
    table = {}
    try:
        os.makedirs(directory_name)
    except Exception:
        pass
    for key in data[0]["items"].keys():
        content_0 = data[0]["items"][key]
        content_1 = data[1]["items"][key]
        keys = set()
        keys, sf_colors = get_sf_colours(content_0, keys)
        keys, sf_colors = get_sf_colours(content_1, keys)
        gold_html, gold_entities = get_gold_entities(content_0, config_0, sf_colors)
        if gold_html != get_gold_entities(content_1, config_1, sf_colors)[0]:
            break
        computed_html_0, computed_entities_0 = get_computed_entities(content_0, config_0, sf_colors)
        computed_html_1, computed_entities_1 = get_computed_entities(content_1, config_1, sf_colors)
        gold_entities_html = get_entities_html(gold_entities)
        computed_entities_html_0 = get_entities_html(computed_entities_0)
        computed_entities_html_1 = get_entities_html(computed_entities_1)
        previous_html, next_html = get_prev_next_links(key, data[0]["items"], directory_name)
        html_content_dict = {
            "gold_html": gold_html,
            "computed_html_0": computed_html_0,
            "computed_html_1": computed_html_1,
            "gold_entities_html": gold_entities_html,
            "computed_entities_html_0": computed_entities_html_0,
            "computed_entities_html_1": computed_entities_html_1,
            "precision_0": content_0["evaluation"]["precision_and_recall"]["precision"],
            "precision_1": content_1["evaluation"]["precision_and_recall"]["precision"],
            "recall_0": content_0["evaluation"]["precision_and_recall"]["recall"],
            "recall_1": content_1["evaluation"]["precision_and_recall"]["recall"],
            "f1score_0": content_0["evaluation"]["precision_and_recall"]["f1_score"],
            "f1score_1": content_1["evaluation"]["precision_and_recall"]["f1_score"],
            "tp_0": content_0["evaluation"]["precision_and_recall"]["confusion_matrix"]["tp_sum"],
            "tp_1": content_1["evaluation"]["precision_and_recall"]["confusion_matrix"]["tp_sum"],
            "fp_0": content_0["evaluation"]["precision_and_recall"]["confusion_matrix"]["fp_sum"],
            "fp_1": content_1["evaluation"]["precision_and_recall"]["confusion_matrix"]["fp_sum"],
            "fn_0": content_0["evaluation"]["precision_and_recall"]["confusion_matrix"]["fn_sum"],
            "fn_1": content_1["evaluation"]["precision_and_recall"]["confusion_matrix"]["fn_sum"],
            "prev": previous_html, "next": next_html,
            "item_number": key
        }
        html = templates.html_body.format(**html_content_dict)
        file_dir = os.path.join(directory_name, str(key) + ".html")
        with open(file_dir, "w") as open_file:
            open_file.write(html)
        table[key] = html_content_dict
    build_index_rows(table, directory_name)
    build_index_csv(table, directory_name)
