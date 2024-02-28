import pytest
import cfpq_data
import networkx as nx
from project import task1
import random
import pydot
import os

from unittest.mock import patch, MagicMock



@patch("cfpq_data.download")
@patch("cfpq_data.graph_from_csv")
def test_get_graph_info(mock_graph_from_csv, mock_download):
    # Mock the download function to return a dummy path
    mock_download.return_value = "/tmp/dummy_path.csv"

    # Mock the graph_from_csv function to return a dummy graph
    mock_graph = MagicMock()
    mock_graph.number_of_edges.return_value = 5
    mock_graph.number_of_nodes.return_value = 3
    mock_graph.edges.return_value = [
        (0, 1, {"label": "a"}),
        (1, 2, {"label": "b"}),
        (2, 0, {"label": "c"}),
    ]
    mock_graph_from_csv.return_value = mock_graph

    # Call the function with a dummy graph name
    result = task1.get_graph_info("dummy_graph")

    # Assert that the function returned the expected values
    assert result == (5, 3, {"a", "b", "c"})
