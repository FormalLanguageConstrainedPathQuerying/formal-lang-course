import pytest
from project import *
import cfpq_data


def test_by_bzip():
    bzip_path = cfpq_data.download("bzip")
    bzip = cfpq_data.graph_from_csv(bzip_path)
    assert get_graph_info_by_name("bzip") == get_graph_info(bzip)
