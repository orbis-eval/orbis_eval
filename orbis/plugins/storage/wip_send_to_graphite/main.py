import graphitesend
from orbis import app


class SendToGraphite(object):
    """docstring for SendToGraphite"""

    def __init__(self, rucksack):
        super(SendToGraphite, self).__init__()
        raise NotImplementedError

        self.rucksack = rucksack
        self.config = self.rucksack["config"]
        self.data = self.rucksack["data"]
        self.results = self.rucksack["results"]

    def run(self):
        """ """
        graphite_server = 'localhost'
        # graphite_port = 2003

        g = graphitesend.init(graphite_server=graphite_server)

        metric_path = ".".join([self.config["scorer"]["name"],
                                self.config["aggregator"]["service"]["profile"],
                                "-".join([e for e in self.config["scorer"]["entities"]])])

        graphite_dict = {
            ".".join([metric_path, "has_score"]): self.results["has_score"],
            ".".join([metric_path, "no_score"]): self.results["no_score"],
            ".".join([metric_path, "empty_responses"]): self.results["empty_responses"],
            ".".join([metric_path, "precision"]): self.results["precision"],
            ".".join([metric_path, "recall"]): self.results["recall"],
            ".".join([metric_path, "f1_score"]): self.results["f1_score"]
        }

        response = g.send_dict(graphite_dict)
        app.logger.debug("Send to grapite")

        return response
