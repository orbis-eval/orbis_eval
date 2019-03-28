#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-



class Scorer(object):
    """docstring for Scorer"""
    def __init__(self, arg):
        super(Scorer, self).__init__()
        self.arg = arg

    @classmethod
    def get_class(cls, config):
        cls.config = config
        scorer_class = eval(config["Scorer"])
        return scorer_class(config)


class NEL_ScorerStrict(Scorer):
    """docstring for NEL_ScorerStrict"""
    def __init__(self):
        super(NEL_ScorerStrict, self).__init__()
