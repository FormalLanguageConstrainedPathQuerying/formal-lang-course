from project.utils import graph_utils

import rdflib


graph_info = graph_utils.get_graph_info("travel")


def test_number_nodes():
    assert graph_info.nodes == 131


def test_number_edges():
    assert graph_info.edges == 277


def test_graph_labels():
    assert graph_info.labels == {
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#unionOf"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#disjointWith"),
        rdflib.term.URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
        rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#onProperty"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#someValuesFrom"),
        rdflib.term.URIRef("http://www.owl-ontologies.com/travel.owl#hasPart"),
        rdflib.term.URIRef("http://www.w3.org/2000/01/rdf-schema#domain"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#inverseOf"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#oneOf"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#hasValue"),
        rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#rest"),
        rdflib.term.URIRef("http://www.owl-ontologies.com/travel.owl#hasAccommodation"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#complementOf"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#differentFrom"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#minCardinality"),
        rdflib.term.URIRef("http://www.w3.org/2000/01/rdf-schema#comment"),
        rdflib.term.URIRef("http://www.w3.org/2000/01/rdf-schema#range"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#equivalentClass"),
        rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#intersectionOf"),
        rdflib.term.URIRef("http://www.w3.org/2002/07/owl#versionInfo"),
    }
