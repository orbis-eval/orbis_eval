class BinaryClassificationMetrics(object):

    def __init__(self):
        super(BinaryClassificationMetrics, self).__init__()

    @classmethod
    def get_precision(cls, true_positive, false_positive):
        true_positive, false_positive = float(true_positive), float(false_positive)
        try:
            result = (true_positive / (true_positive + false_positive))
        except ZeroDivisionError:
            result = 0
        return result

    @classmethod
    def get_recall(cls, true_positive, item_sum):
        true_positive, item_sum = float(true_positive), float(item_sum)
        try:
            result = (true_positive / item_sum)
        except ZeroDivisionError:
            result = 0
        return result

    @classmethod
    def get_f1_score(cls, precision, recall):
        precision, recall = float(precision), float(recall)
        try:
            result = 2 * ((precision * recall) / (precision + recall))
        except ZeroDivisionError:
            result = 0
        return result

    @classmethod
    def get_sensitivity(cls):
        """ aka true positive rate"""
        raise NotImplemented

    @classmethod
    def get_specificity(cls):
        """ aka true negative rate"""
        raise NotImplemented

    @classmethod
    def get_roc(cls):
        raise NotImplemented
