import graphitesend


def run(yaml_config, data, results):
    """ """

    graphite_server = 'localhost'
    # graphite_port = 2003

    g = graphitesend.init(graphite_server=graphite_server)

    metric_path = ".".join([yaml_config["scorer"]["name"],
                            yaml_config["aggregator"]["service"]["profile"],
                            "-".join([e for e in yaml_config["scorer"]["entities"]])])

    graphite_dict = {
        ".".join([metric_path, "has_score"]): results["has_score"],
        ".".join([metric_path, "no_score"]): results["no_score"],
        ".".join([metric_path, "empty_responses"]): results["empty_responses"],
        ".".join([metric_path, "precision"]): results["precision"],
        ".".join([metric_path, "recall"]): results["recall"],
        ".".join([metric_path, "f1_score"]): results["f1_score"]
    }

    response = g.send_dict(graphite_dict)

    return response
