# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import inspect
import io
from contextlib import redirect_stdout

import pytest
import re
from grammarinator.runtime import RuleSize, simple_space_serializer
from grammarinator.tool import (
    PickleTreeCodec,
    GeneratorTool,
    DefaultGeneratorFactory,
    DefaultPopulation,
)

import ProgramGenerator

# Fix import statements in try block to run tests
try:
    from project.task11 import prog_to_tree, nodes_count, tree_to_prog
except ImportError:
    pytestmark = pytest.mark.skip("Task 11 is not ready to test!")


# This fixture probably uses internal API, so it can be broken at any time :(
@pytest.fixture(scope="module")
def generator(request) -> GeneratorTool:
    return GeneratorTool(
        generator_factory=DefaultGeneratorFactory(
            ProgramGenerator.ProgramGenerator,
            model_class=None,
            cooldown=0.2,
            weights=None,
            lock=None,
            listener_classes=None,
        ),
        rule="prog",
        out_format="",
        limit=RuleSize(depth=20, tokens=RuleSize.max.tokens),
        population=(
            DefaultPopulation(
                "tests/autotests/program_examples/", "grtp", PickleTreeCodec()
            )
            if True
            else None
        ),
        generate=True,
        mutate=True,
        recombine=True,
        keep_trees=False,
        transformers=[],
        serializer=simple_space_serializer,
        cleanup=False,
        encoding="utf-8",
        errors="strict",
        dry_run=False,
    )


@pytest.fixture(params=range(100))
def program(generator, request) -> str:
    # Grammarinator's API cannot return plain string, it can either write to the file or to the stdout
    # So we catch stdout
    with io.StringIO() as buf, redirect_stdout(buf):
        with generator:
            generator.create(request.param)
        out = buf.getvalue()
    return out


class TestParser:
    def test_id(self, program: str):
        tree_before, is_valid = prog_to_tree(program)
        assert is_valid
        program_after = tree_to_prog(tree_before)
        tree_after, is_valid_after = prog_to_tree(program_after)
        assert is_valid_after
        assert nodes_count(tree_before) == nodes_count(tree_after)

    def test_wrong(self, program: str):
        reg = re.compile("[=,]", re.X)
        if reg.search(program):
            program_bad = reg.sub("", program)
            _, is_valid_bad = prog_to_tree(program_bad)
            assert not is_valid_bad
