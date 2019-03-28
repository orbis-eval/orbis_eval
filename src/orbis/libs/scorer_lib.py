#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


from operator import itemgetter
from orbis import app
# from orbis.libs.cli_lib import multiline_logging


def get_confusion_matrix(computed, gold, conditions):
    """

    :param computed:
    :param gold:
    :param conditions:
    :return:
    """
    entity_mappings = []

    gold_0 = gold.copy()
    computed_0 = computed.copy()

    for gold_entry in sorted(gold_0, key=itemgetter("start")):

        gold_start = int(gold_entry["start"])
        gold_end = int(gold_entry["end"])
        gold_id = "{},{}".format(gold_start, gold_end)

        gold_url = gold_entry["key"]
        gold_type = gold_entry["entity_type"]
        gold_surface_form = gold_entry["surfaceForm"]

        entity_mapping = [gold_id, False, 0]

        for comp_entry in sorted(computed_0, key=itemgetter("document_start")):

            comp_start = int(comp_entry["document_start"])
            comp_end = int(comp_entry["document_end"])

            comp_url = comp_entry["key"]
            comp_type = comp_entry["entity_type"]
            comp_surface_form = comp_entry["surfaceForm"]

            states = {
                "same_url": gold_url == comp_url,
                "same_type": gold_type == comp_type,
                "same_surfaceForm": gold_surface_form == comp_surface_form,
                "overlap": gold_end >= comp_start and gold_start <= comp_end,
                "same_start": gold_start == comp_start,
                "same_end": gold_end == comp_end
            }

            # multiline_logging(app, states)

            if all([states[condition] for condition in conditions]):

                comp_id = "{},{}".format(comp_start, comp_end)

                entity_mapping[1] = comp_id
                entity_mapping[2] += 1

                gold_0.remove(gold_entry)
                computed_0.remove(comp_entry)
                break

        entity_mappings.append(entity_mapping)

    for comp_entry in sorted(computed_0, key=itemgetter("document_start")):

        comp_start = int(comp_entry["document_start"])
        comp_end = int(comp_entry["document_end"])
        comp_id = "{},{}".format(comp_start, comp_end)
        entity_mapping = [False, comp_id, 0]

        entity_mappings.append(entity_mapping)

    confusion_matrix = {
        "tp": [],
        "fp": [],
        "fn": [],
        "tp_ids": [],
        "fp_ids": [],
        "fn_ids": []
    }

    for gold, comp, num in entity_mappings:

        if gold and comp:
            # app.logger.debug("TP: Gold: {}; Comp: {}; ({})".format(gold, comp, num))
            confusion_matrix["tp"].append(1)
            confusion_matrix["fp"].append(0)
            confusion_matrix["fn"].append(0)
            confusion_matrix["tp_ids"].append(comp)

        elif comp and not gold:
            # app.logger.debug("FP: Gold: {}; Comp: {}; ({})".format(gold, comp, num))
            confusion_matrix["fp"].append(1)
            confusion_matrix["tp"].append(0)
            confusion_matrix["fn"].append(0)
            confusion_matrix["fp_ids"].append(comp)

        elif gold and not comp:
            # app.logger.debug("FN: Gold: {}; Comp: {}; ({})".format(gold, comp, num))
            confusion_matrix["fn"].append(1)
            confusion_matrix["tp"].append(0)
            confusion_matrix["fp"].append(0)
            confusion_matrix["fn_ids"].append(gold)

        elif not gold and not comp:
            raise RuntimeError

        else:
            # print("Error")
            pass

    confusion_matrix["tp_sum"] = sum(confusion_matrix["tp"])
    confusion_matrix["fp_sum"] = sum(confusion_matrix["fp"])
    confusion_matrix["fn_sum"] = sum(confusion_matrix["fn"])

    return confusion_matrix
