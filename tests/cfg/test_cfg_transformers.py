from pathlib import Path
from project.cfg.io import read_from_file
from project.cfg.transformers import *


class TestsForWcnfTransformer:
    def test_transform_to_wcnf(self):
        str_path = "./resources/cfg1"
        path = Path(str_path)

        original_cfg = read_from_file(path)
        wcnf_cfg = transform_to_wcnf(original_cfg)

        # wcnf test
        for production in wcnf_cfg.productions:
            assert production.head in wcnf_cfg.variables
            if len(production.body) == 1:
                assert production.body[0] in wcnf_cfg.terminals
            elif len(production.body) == 2:
                assert (
                    production.body[0] in wcnf_cfg.variables
                    and production.body[1] in wcnf_cfg.variables
                )
            else:
                assert len(production.body) == 0

        # if possible not cnf test
        def get_flags(cfg):
            eps_flag = False
            right_start_flag = False
            for product in cfg.productions:
                if not product.body and product.head != cfg.start_symbol:
                    eps_flag = True

                for elem in product.body:
                    if elem == cfg.start_symbol:
                        right_start_flag = True

            return eps_flag, right_start_flag

        orig_eps, orig_right_start = get_flags(original_cfg)
        wcnf_eps, wcnf_right_start = get_flags(wcnf_cfg)
        if orig_eps or orig_right_start:
            assert wcnf_eps or wcnf_right_start
