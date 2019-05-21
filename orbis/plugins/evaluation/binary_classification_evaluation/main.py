from orbis import app


class BinaryClassificationEvaluation(object):

    def __init__(self, rucksack):
        super(BinaryClassificationEvaluation, self).__init__()
        self.rucksack = rucksack
        self.file_name = rucksack.open['config']['file_name']
        self.scorer_condition = rucksack.open['config']['scoring']['condition']
        self.computed = rucksack.open['data']['computed']
        self.gold = rucksack.open['data']['gold']
        self.ignore_empty = rucksack.open['config']['scoring']['ignore_empty']
        self.entities = rucksack.open['config']['scoring'].get('entities', [])
        self.scorer = rucksack.plugins["scoring"]
        self.nel_scorer = self.scorer()
        self.metrics = rucksack.plugins["metrics"]
        self.bc_metrics = self.metrics()

    def run(self):
        self.rucksack.open["results"].update(self.binary_classification())
        return self.rucksack

    def binary_classification(self):
        results = {
            "items": {},
            "summary": {
                "binary_classification": {}
            }
        }
        micro = {
            "tp_sum": 0,
            "fp_sum": 0,
            "fn_sum": 0,
            "item_sum": 0
        }
        macro = {
            "precision": 0,
            "recall": 0,
            "f1_score": 0,
            "item_sum": 0
        }
        stats = {
            "has_score": 0,
            "no_score": 0,
            "empty_responses": 0
        }
        app.logger.info("Starting Evaluation Calculation for {}".format(self.file_name))
        for number, item in self.computed.items():
            # app.logger.debug(f"Evaluating item: {item}")
            results["items"] = {
                number: {
                    "binary_classification": {}
                }
            }
            if len(item) <= 0:
                stats["empty_responses"] += 1
                if self.ignore_empty:
                    continue
            if self.gold.get(number):
                current_gold = [entity for entity in self.gold[number] if entity["entity_type"] in self.entities or len(self.entities) <= 0]
            else:
                current_gold = []
            current_computed = [entity for entity in item if entity["entity_type"] in self.entities or len(self.entities) <= 0]
            # Scorer
            confusion_matrix = self.nel_scorer.run(current_computed, current_gold, self.scorer_condition)
            # app.logger.debug("Gold Entities: {}".format(current_gold))
            # multiline_logging(app, "Gold Entities: {}".format(current_gold))
            # app.logger.debug("Computed Entities: {}".format(current_computed))
            # multiline_logging(app, "Computed Entities: {}".format(current_computed))
            item_sum = len(current_gold)
            micro["tp_sum"] += confusion_matrix["tp_sum"]
            micro["fp_sum"] += confusion_matrix["fp_sum"]
            micro["fn_sum"] += confusion_matrix["fn_sum"]
            micro["item_sum"] += item_sum
            # Metrics
            precision = self.bc_metrics.get_precision(confusion_matrix["tp_sum"], confusion_matrix["fp_sum"])
            recall = self.bc_metrics.get_recall(confusion_matrix["tp_sum"], item_sum)
            f1_score = self.bc_metrics.get_f1_score(precision, recall)
            macro["precision"] += precision
            macro["recall"] += recall
            macro["f1_score"] += f1_score
            macro["item_sum"] += 1
            results["items"][number]["binary_classification"] = {
                "confusion_matrix": confusion_matrix,
                "item_sum": item_sum,
                "precision": precision,
                "recall": recall,
                "f1_score": f1_score,
                "entities": ", ".join(self.entities)
            }
            if f1_score > 0 or precision > 0 or recall > 0:
                stats["has_score"] += 1
            else:
                stats["no_score"] += 1
        # Metrics
        micro["precision"] = self.bc_metrics.get_precision(micro["tp_sum"], micro["fp_sum"])
        micro["recall"] = self.bc_metrics.get_recall(micro["tp_sum"], micro["item_sum"])
        micro["f1_score"] = self.bc_metrics.get_f1_score(micro["precision"], micro["recall"])
        if macro["item_sum"] > 0:
            macro["precision"] = macro["precision"] / macro["item_sum"]
            macro["recall"] = macro["recall"] / macro["item_sum"]
            macro["f1_score"] = macro["f1_score"] / macro["item_sum"]
        else:
            macro["precision"] = 0
            macro["recall"] = 0
            macro["f1_score"] = 0
        results["summary"]['binary_classification'] = {
            "has_score": stats["has_score"],
            "no_score": stats["no_score"],
            "empty_responses": stats["empty_responses"],
            "entities": ", ".join(self.entities),
            "total_tp": micro["tp_sum"],
            "total_fp": micro["fp_sum"],
            "total_fn": micro["fn_sum"],
            "total_item_sum": micro["item_sum"],
            "micro": {
                "precision": micro["precision"],
                "recall": micro["recall"],
                "f1_score": micro["f1_score"]
            },
            "macro": {
                "precision": macro["precision"],
                "recall": macro["recall"],
                "f1_score": macro["f1_score"]
            }
        }
        app.logger.debug(f'Running nel_evaluator for {self.file_name}')
        app.logger.debug(f'Micro precision = {micro["precision"]}')
        app.logger.debug(f'Micro recall = {micro["recall"]}')
        app.logger.debug(f'Micro f1_score = {micro["f1_score"]}')
        app.logger.debug(f'Macro precision = {macro["precision"]}')
        app.logger.debug(f'Macro recall = {macro["recall"]}')
        app.logger.debug(f'Macro f1_score = {macro["f1_score"]}')
        return results
