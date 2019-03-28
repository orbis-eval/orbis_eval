
nif_namespace = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
itsrdf_namespace = Namespace("http://www.w3.org/2005/11/its/rdf#")

base_pattern = "https?:\/\/(www\.)?(wikidata|dbpedia|schema|umbel|xmlns)\.(org|com)\/?(foaf\/0\.1|class(\/yago)?|entity|ontology|umbel\/rc)?\/"
organization_pattern = base_pattern + "(Q737498|Q11032|Wikicat.*Companies|Agency|CentralBank|WikicatDefunctCompaniesBasedIn.*|Q327333|FinancialInstitution|WorldOrganization|WikicatPowerCompaniesOf.*|Wikicat.*Organizations|Wikicat.*Institutions|WikicatCompaniesListedOn.*|WikicatCompaniesEstablishedIn.*|WikicatCompaniesBasedIn.*|Foundation|Q43229|DrugCompany|WikicatMultinationalCompanies|Company|Organi(s|z)ation|(Social)?Group|Institution|Business|Enterprise|Bank)[0-9]*"
person_pattern = base_pattern + "(Surname|WikicatPeopleFrom.*|Senator|Politician|Governor|Capitalist|Intellectual|Leader|Investor|Q215627|Q5|Person|FictionalCharacter|SpiritualBeing|WikicatLivingPeople)[0-9]*"
location_pattern = base_pattern + "(WikicatIsIsland.*|Wikicat.*Countries|WikicatStatesOf.*|WikicatStatesAndTerritoriesEstablished.*|WikicatMemberStatesOf.*|WikicatProvincesOf.*|Land|UrbanArea|Village|Municipality|State|Settlement|Q15617994|Q6256|Q15617994|Q3455524|Place|Location|YagoGeoEntity|Region|PopulatedPlace|GeographicalArea|City|Country|District|AdministrativeDistrict|AdministrativeArea|WikicatCountries)[0-9]*"
