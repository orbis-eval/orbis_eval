# TODO 0: can be multiple types, must build a check
def get_dbpedia_type(lang, uri, check_redirect=False):

    uri_unquoted = urllib.parse.unquote(uri).encode("utf8")
    uri_unquoted = get_redirect() if check_redirect else uri_unquoted

    query = f'''
        SELECT DISTINCT ?obj
        WHERE {{ <{uri_unquoted.decode("utf-8")}> (rdf:type)* ?obj .}}
    '''

    organization_pattern = regex.compile(organization_pattern)
    person_pattern = regex.compile(person_pattern)
    location_pattern = regex.compile(location_pattern)

    sparql = SPARQLWrapper(lang)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    print(f"Processing: {uri_unquoted.decode("utf-8")}")

    # TODO 0: can be multiple types, must build a check
    if len(results["results"]["bindings"]) > 0:
        for result in results["results"]["bindings"]:

            binding = result["obj"]["value"]

            if organization_pattern.match(binding):
                entity_type = 'Organisation'
                break
            elif person_pattern.match(binding):
                entity_type = 'Person'
                break
            elif location_pattern.match(binding):
                entity_type = 'Location'
                break
            elif "http://aksw.org/notInWiki" in binding:
                entity_type = 'notInWiki'
                break
            else:
                entity_type = False
                not_found_uris.append(binding)

        if entity_type:
            if entity_type != 'notInWiki':
                with open("Found.txt", "a") as open_file:
                    open_file.write("[{}] {}\n".format(entity_type, uri_unquoted.decode("utf8").split("/")[-1]))
            else:
                with open("notInWiki.txt", "a") as open_file:
                    open_file.write("[{}] {}\n".format(entity_type, uri_unquoted.decode("utf8")))
        else:
            with open("UnMatched.txt", "a") as open_file:
                for not_found_uri in not_found_uris:
                    open_file.write("; ".join([uri_unquoted.decode("utf8"), not_found_uri]) + "\n")
    else:
        entity_type = False
        with open("NotInDB.txt", "a") as open_file:
            open_file.write("[{}] {}\n".format(str(entity_type), uri_unquoted.decode("utf8")))

def get_redirect(uri_unquoted):
    redirect_query = """
    SELECT DISTINCT ?redirected
    WHERE
        {{
            <{uri_unquoted}> <http://dbpedia.org/ontology/wikiPageRedirects> ?redirected .
        }}
    """

    sparql = SPARQLWrapper(lang)
    sparql.setQuery(redirect_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    redirect_uri = results["results"]["bindings"][0]["obj"]["value"]
    redirect_uri_unquoted = urllib.parse.unquote(redirect_uri).encode("utf8")

    if redirect_uri_unquoted != uri_unquoted:
        uri_unquoted = redirect_uri_unquoted

    return uri_unquoted