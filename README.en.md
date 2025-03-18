[![Check code style](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/actions/workflows/code_style.yml/badge.svg)](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/actions/workflows/code_style.yml)
[![Code style](https://img.shields.io/badge/Code%20style-black-000000.svg)](https://github.com/psf/black)
---
# Formal Language Course

A course on formal languages: repository template for completing homework assignments, as well as course materials and other related information.

Useful links:
- [List of exercises](tasks.en.md)
- [Code style reference](https://www.python.org/dev/peps/pep-0008/)
- [On reachability with constraints in terms of formal languages, in Russian](https://github.com/FormalLanguageConstrainedPathQuerying/FormalLanguageConstrainedReachability-LectureNotes)
- A textbook on parsing algorithms: [Dick Grune, Ceriel J. H. Jacobs, "Parsing Techniques A Practical Guide"](https://link.springer.com/book/10.1007/978-0-387-68954-8#bibliographic-information)
- A textbook on formal language theory: [M. A. Harrison. 1978. "Introduction to Formal Language Theory"](https://dl.acm.org/doi/book/10.5555/578595)
- Recent work on automata theory and its applications in various fields: [Editors: Jean-Éric Pin. 2021. "Handbook of Automata Theory"](https://ems.press/books/standalone/172)
- [Tool for constructing and simulating various recognizers](https://github.com/spbu-se/KotlinAutomataConstructor)

Technology stack:
- Python 3.12
- Pytest for unit testing
- GitHub Actions for CI
- Python notebook for setting up and documenting experiments
- Dependency management with [Rye](https://rye.astral.sh/)
- English language for documentation or self-documenting code

## Table of contents

- [Formal Language Course](#formal-language-course)
  - [Table of contents](#table-of-contents)
  - [Grading](#grading)
    - [Tests](#tests)
    - [Exercises](#exercises)
  - [Working with the Project](#working-with-the-project)
  - [Homework](#homework)
    - [Completing homework](#completing-homework)
    - [Exercise grading rules](#exercise-grading-rules)
  - [Code style](#code-style)
  - [Tests and Autotests](#tests-and-autotests)
  - [Experiments](#experiments)
  - [Repository Structure](#repository-structure)
  - [Course developers](#course-developers)

## Grading

The grade for the course is based on the points earned throughout the semester.
Points are awarded for the following:
- Exercises (points for each task are specified separately).
- Tests (short, 5-10 minute assessment).
  A test is graded from 0 to 1 points.
  Points from tests are used to weigh the points for exercises.
- Additional tasks assigned by the instructor, such as preparing course materials, implementing demonstration algorithms, etc.
  These are graded at the instructor's discretion, but no more than 30 points in total can be awarded.

The course is divided into blocks, where each block contains some exercises and a test that will weigh those exercises.
The final grade for the course is a weighted sum of the points for the exercises and additional assignments, where the weight is the latest score for the test of the block.
For example, suppose there are two blocks, each with 2 exercises, and 2 tests.
Let's say the first two exercises earned 4 and 5 points, and the remaining two earned 2.5 and 3 points respectively. For the first test, the score is 0.25 points, and for the second test, it is 0.75 points.
Then, the final grade for the course would be:
$(4 + 5) * 0.25 + (2.5 + 3) * 0.75 = 6.375$.

Points are converted to grades as follows:

|   Points    | ECTS  | Traditional |
| :---------: | :---: | :---------: |
| (90 -- 100] |   A   |      5      |
| (80 -- 90]  |   B   |      4      |
| (70 -- 80]  |   C   |      4      |
| (60 -- 70]  |   D   |      3      |
| (50 -- 60]  |   E   |      3      |
|  [0 -- 50]  |   F   |      2      |

### Tests

A test is a small assessment (lasting 5-10 minutes) that is written during a class (usually at the beginning).
The typical number of tests during a course is 2-3.
During the test, students can use any materials, but the time limit is strictly enforced.
Tests can be rewritten (rewrites are usually centralized at the end of the semester), but with each rewrite, the maximum possible score for the test is halved.
So, if you can get a maximum of 1 point for a test written on the first attempt, then for a perfectly written test on the second attempt, you can only get 0.5 points, and so on.
Moreover, the score recorded for the test is the score from the last attempt (not the maximum across all attempts, for example).

Typical test questions:
- Construct a leftmost derivation of this string in this grammar.
- Build a finite automaton that represents the same language as this regular expression.
- What is the space complexity of algorithm X?
- Give the definition of a RSM.
- What is the difference between CNF and wCNF?

### Exercises

There are two types of exercises:
- **Exercises with fully automated grading.**
  These exercises have known function names, signatures, and a set of test cases; if the tests pass, the task is considered completed.
  The number of points for such exercises is at least 60.
  This means that by completing all tests and submitting all such exercises, you can guarantee a grade of 3 (E-D) for the course.
- **Exercises requiring evaluation by the instructor or assistant.**
  These are typically exercises that involve setting up experiments or developing relatively non-trivial solutions.
  They are based on exercises of the previous type, so solving them in isolation can be difficult.

## Working with the Project

- To complete the exercises, you need to fork this repository to your GitHub account.
- It is recommended to install [`pre-commit`](https://pre-commit.com/#install) to keep the project in good condition.
  - You can install `pre-commit` by running the following command in the root of your project:
    ```shell
    pre-commit install
    ```
  - To format the code according to the accepted style, run the following command in the root of your project:
    ```shell
    pre-commit run --all-files
    ```
- Share the link to your fork of the repository with the instructor for it to be added to the results table.
- You need to add reviewers to your repository with `admin` rights for reading, editing, and reviewing pull requests.

## Homework

All exercises have a deadline (usually one week from when they are assigned), after which the maximum score for the task is halved.

The number of reviews is limited to three.
Requesting a review counts as an attempt to submit assignment.
After three attempts, the points for the task are lost.
The first review request must be made **before the deadline**.
**Note**, there should be no commits between the review request and the actual review.
This means you must ensure everything is ready before requesting a review.
If there are commits after the request and before the review, the points for the task will be halved permanently.

Please note that if a review is requested but not all requirements for the solution are met (e.g., CI fails, not all parts of the task are completed, not all questions are answered, or requirements for the reports are not followed), a detailed review of the task will not be conducted, and the attempt will be considered failed.
In such a case, the only feedback you may receive is something like "the task is not fully completed".
Therefore, completing the task properly is the responsibility of the student.

### Completing homework

When working on the homework, you must follow the GitHub Flow ([more info here](https://githubflow.github.io/) and [here (in Russian)](https://habr.com/ru/articles/346066/)).

Additionally, keep the following points in mind:
- Each homework assignment should be completed in a separate branch.
  The branch should have a meaningful and consistent name.
- The branch should only contain commits made by the person submitting the task, and only those commits that directly relate to solving the task.
- The filename should reflect its content (e.g., the name of the algorithm).
- Automatic tests should not be modified, except in cases explicitly mentioned in the task description.
- Commit messages should be clear and reflect commit content.
- When completing homework in a new branch, you must open a corresponding pull request to the `main` branch of your fork.
- Note that all tests must pass, not just those related to the task being submitted in the current pull request.
- The pull request should have a clear title and description with relevant progress points.
- The task will be reviewed through the review of your pull request (by filling in the Reviewers field).
  Even if the task doesn't require instructor verification, a review request must still be made.
- Once you believe the task is complete, you can request a review from the reviewer.
  - To earn full points for the task, the review must be requested **before the deadline**.
- When the review is complete and the task is **approved**, it must be merged into the `main` branch of your fork.
- The results of completed exercises will be reused in subsequent homework assignments.

### Exercise grading rules

- If a review was requested _before_ **the deadline** _and_ the task was accepted **on the first attempt**, _and_ no commits were made to the branch between the review request and the review itself, you receive **full score for the homework**.
- All other cases result in a lower score. Common scenarios:
  - If the review was requested _after_ **the deadline** _and_ **no more than three attempts were used**, you receive **half of the full score for the homework**.
  - If the review was requested _before_ **the deadline** _but_ more than one and no more than three attempts were used, you receive **half of the score for the homework**.
    - For tasks involving experiments and the final task (developing an interpreter), in this case, you receive **3/4 of the full score (75%)**.
  - If the maximum number of attempts (more than three) has been used, you receive **0 points** for the task.
- If commits were made to the branch between the review request and the review itself, the maximum possible score for the task is **only half**.
  In other words, in the previous scenarios, replace **full score** with **half score**.

## Code style

- Place the source code for programming exercises in the `project` folder.
- Give files and modules meaningful names, following the officially accepted style.
- Structure the code by using both classes and well-defined functions.
  The clearer the code, the faster it can be reviewed, and the more likely you are to receive full points.

## Tests and Autotests

There are two types of tests: those prepared by the instructor and your own.

The instructor-prepared tests are located in the `tests/autotests` folder and are used to check exercises with fully automated grading.
When working with these tests, the following rules should be followed:

- In these tests, usually, only one block should be modified:
  ```python
  try:
      from project.task2 import regex_to_dfa, graph_to_nfa
  except ImportError:
      pytestmark = pytest.mark.skip("Task 2 is not ready to test!")
  ```
  In this block, you need to specify from which module(s) the required functions should be imported; otherwise, the tests will be skipped.
- If you find a bug **and** are willing to fix it, you can modify the file and then submit the change via a Pull Request to the main repository.
- If you find a bug and are not willing to fix it, you must inform the instructor and take no further action!

The following rules apply to your own tests:

- Place tests for homework assignments in the `tests` folder.
- The naming format for test files is `test_[module/class/function being tested].py`.
- Use [`pytest`](https://docs.pytest.org/en/6.2.x/) to work with tests.
- To run the tests, use the following command from the root of the project:
  ```shell
  python ./scripts/run_tests.py
  ```

## Experiments

An experiment (setup, measurements, results, analysis of results) should be documented as a Python notebook, which is published on GitHub.
- To perform experiments, you will need not only the code but also the environment and some configuration.
  Accordingly, the solution submitted should include instructions for setting up the environment and reproducing the experiments.
  Ideally, all of this should be included in the notebook.
- Experiments should be reproducible (e.g., by reviewers).
- The notebook must contain the setup, code for the experiments, preparation of reports, and creation of graphs.
- The notebook serves as a connected narrative describing the goals of the experiment, the methodology, analysis of the results, and answers to the questions posed.
  - The answers to the questions must be substantiated (by experiments), the observed behavior should be analyzed and justified.

## Repository Structure

```text
.
├── .github - files for CI setup and checks
├── docs - text documents and course materials
├── project - source code for homework assignments
├── scripts - helper scripts for automating development
├── tests - directory for unit tests of homework assignments
│   └── autotests - directory with automated tests for homework assignments
├── pyproject.toml - dependencies for repository
├── README.en.md - main information about the project (in English)
├── README.md - main information about the project (in Russian)
├── tasks.em.md - file with descriptions of homework assignments (in English)
└── tasks.md - file with descriptions of homework assignments (in Russian)
```

## Course developers

- Semyon Grigorev [@gsvgit](https://github.com/gsvgit)
- Nikolai Ponomarev [@wowaster](https://github.com/WoWaster)
- Efim Kubishkin [@kubef](https://github.com/KubEF)
- Egor Orachyov [@EgorOrachyov](https://github.com/EgorOrachyov)
- Vadim Abzalov [@vadyushkins](https://github.com/vadyushkins)
- Rustam Azimov [@rustam-azimov](https://github.com/rustam-azimov)
- Ekaterina Shemetova [@katyacyfra](https://github.com/katyacyfra)
