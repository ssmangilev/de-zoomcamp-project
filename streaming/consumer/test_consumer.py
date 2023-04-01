import argparse
import pytest

from consumer import main


def test_required_parameters_present():
    with pytest.raises(ValueError):
        main(argparse.Namespace(
            credentials_path=None,
            topic=None,
            bootstrap_servers=None,
            bq_project=None,
            bq_dataset=None,
            bq_table=None
        ))
