[![Check code style](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/actions/workflows/code_style.yml/badge.svg)](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/actions/workflows/code_style.yml)
[![Code style](https://img.shields.io/badge/Code%20style-black-000000.svg)](https://github.com/psf/black)
---
# Formal Language Course

A course on formal languages: repository structure template for completing homework assignments, as well as course materials and other related information.

Current:
- [List of tasks](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/blob/main/tasks.en.md)
- [Code style reference](https://www.python.org/dev/peps/pep-0008/)
- [On reachability with constraints in terms of formal languages, in Russian](https://github.com/FormalLanguageConstrainedPathQuerying/FormalLanguageConstrainedReachability-LectureNotes)
- A classic textbook on parsing algorithms: [Dick Grune, Ceriel J. H. Jacobs, "Parsing Techniques A Practical Guide"](https://link.springer.com/book/10.1007/978-0-387-68954-8#bibliographic-information)
- A classic textbook on formal language theory: [M. A. Harrison. 1978. "Introduction to Formal Language Theory"](https://dl.acm.org/doi/book/10.5555/578595)
- Recent work on automata theory and its applications in various fields: [Editors: Jean-Éric Pin. 2021. "Handbook of Automata Theory"](https://ems.press/books/standalone/172)
- [Tool for constructing and simulating various recognizers](https://github.com/spbu-se/KotlinAutomataConstructor)

Technologies:
- Python 3.12
- Pytest for unit testing
- GitHub Actions for CI
- Python notebook for setting up and documenting experiments
- Dependency management with [Rye](https://rye.astral.sh/)
- English language for documentation or self-documenting code

## Table of contents

- [Formal Language Course](#formal-language-course)
  - [Table of contents](#table-of-contents)
  - [Marks computation](#marks-computation)
    - [Tests](#tests)
    - [Homework Practical Tasks](#homework-practical-tasks)
  - [Working with the Project](#working-with-the-project)
  - [Homework Practical Tasks](#homework-practical-tasks-1)
    - [Completing Homework](#completing-homework)
    - [Получение оценки за домашнюю работу](#получение-оценки-за-домашнюю-работу)
  - [Code](#code)
  - [Tests](#tests-1)
  - [Experiments](#experiments)
  - [Repository Structure](#repository-structure)
  - [Course developers](#course-developers)
  - [Вместо введения](#вместо-введения)

## Marks computation

The grade for the course is based on the points earned throughout the semester.
Points are awarded for the following:
- Homework assignments (points for each task are specified separately).
- Tests (short, 5-10 minute control tasks).
A test is graded from 0 to 1 points.
Points from tests are used to weigh the points for homework assignments.
- Additional tasks assigned by the instructor, such as preparing course materials, implementing demonstration algorithms, etc.
These are graded at the instructor's discretion, but no more than 30 points in total can be awarded.

__TODO: первое предложение бредовое слегка и на русском. Надо поправить и там, и там__

The final grade for the course is a weighted sum of the points for tasks and additional assignments, where the weight is the points for the nearest tests (chronologically speaking) to the right.
One can think of the course as divided into blocks, where each block contains some tasks and a test that will weigh those tasks.
For example, suppose there are two blocks, each with 2 tasks and 2 tests.
Let's say the first two tasks earned 4 and 5 points, and the remaining two earned 2.5 and 3 points respectively. For the first test, the score is 0.25 points, and for the second test, it is 0.75 points.
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

__TODO: Подумать надо ли как-то поменять табличку выше__

### Tests

A "test" is a small control task (lasting 5-10 minutes) that is written during a class (usually at the beginning).
The typical number of tests during a course is 2-3.
During the test, students can use any materials, but the time limit is strictly enforced.
Tests can be rewritten (rewrites are usually centralized at the end of the semester), but with each rewrite, the maximum possible score for the test is halved.
So, if you can get a maximum of 1 point for a test written on the first attempt, then for a perfectly written test on the second attempt, you can only get 0.5 points, and so on.
Moreover, the score recorded for the test is the score from the last attempt (not the maximum across all attempts, for example).

Typical test questions:
- Construct a leftmost derivation of this string in this grammar.
- Build a finite automaton that represents the same language as this regular expression.
- What is the space complexity of algorithm X?
- Give the definition of a recursive finite automaton.
- What is the difference between CNF and wCNF?

### Homework Practical Tasks

There are two types of tasks:
- Tasks with fully automated grading.
These tasks have known function names, signatures, and a set of test cases; if the tests pass, the task is considered completed.
The number of points for such tasks is at least 60.
This means that by completing all tests and submitting all such tasks, you can guarantee a grade of 3 (E-D) for the course.
- Tasks requiring evaluation by the instructor or assistant.
These are typically tasks that involve setting up experiments or developing relatively non-trivial solutions.
They are based on tasks of the previous type, so solving them in isolation can be difficult.

## Working with the Project

- To complete the homework practical tasks, you need to fork this repository to your GitHub account.
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

## Homework Practical Tasks

All tasks have a deadline (usually one week from when they are assigned), after which the maximum score for the task is halved.

The number of reviews is limited to three.
A review request is considered a check attempt.
After three attempts, the points for the task are lost.
The first review request must be made **before the deadline**.
**Note**, there should be no commits between the review request and the actual review.
This means you should ensure everything is ready before requesting a review.
If there are commits after the request and before the review, the points for the task will be halved permanently.

Please note that if a review is requested but not all requirements for the solution are met (e.g., CI fails, not all parts of the task are completed, not all questions are answered, or report requirements are not followed), a detailed review of the task will not be conducted, and the attempt will be considered failed.
In such a case, the only feedback you may receive is something like "the task is not fully completed".
Therefore, completing the task properly is the responsibility of the student.

### Completing Homework

When working on the homework, you must follow the GitHub Flow ([more info here](https://githubflow.github.io/) and [here](https://habr.com/ru/articles/346066/)).

Additionally, keep the following points in mind:
- Each homework assignment should be completed in a separate branch.
The branch should have a meaningful and consistent name.
- The branch should only contain commits made by the person submitting the task, and only those commits that directly relate to solving the task.
- The filename should reflect its content (e.g., the name of the algorithm).
- Automatic tests should not be modified, except in cases explicitly mentioned in the task description.
- Commit messages should be clear and reflect the essence of what was done.
- When completing homework in a new branch, you must open a corresponding pull request to the `main` branch of your fork.
- Note that all tests must pass, not just those related to the task being submitted in the current pull request.
- The pull request should have a clear title and description with relevant progress points.
- The task will be reviewed through the review of your pull request (by filling in the Reviewers field).
Even if the task doesn't require instructor verification, a review request must still be made.
- Once you believe the task is complete, you can request a review from the reviewer.
  - To earn full points for the task, the review must be requested **before the deadline**.
- When the review is complete and the task is **approved**, it must be merged into the `main` branch of your fork.
- The results of completed tasks will be reused in subsequent homework assignments.

### Получение оценки за домашнюю работу

__TODO: Здесь вроде что-то надо было чинить, так что пока не переводил__

- Если ревью было запрошено _до_ **дедлайна** _и_ задача зачтена с **с первой попытки** _и_ после запроса ревью и до самого ревью в ветку не было коммитов, то вы получаете **полный балл за домашнюю работу**.
- Все остальные варианты --- меньшее количество баллов. Частые случаи:
  - Если проверка запрошена _после_ **дедлайна** _и_ **потрачено не больше трёх попыток**, то вы получаете **половину полного балла за домашнюю работу**.
  - Если проверка запрошена _до_ **дедлайна** _но_ **потрачено больше одной и не больше трёх попыток**, то вы получаете **половину полного балла за домашнюю работу**.
    - Для задач на постановку экспериментов и последней задачи (разработка интерпретатора) в данном случае получаете **3/4 от полного балла (75%)**.
  - Если исчерпано количество попыток сдать задачу (больше трёх), то за неё получаете **0 баллов**.
- Если после запроса ревью и до самого ревью в ветку были ещё коммиты, то за задачу можно получить **максимум половину баллов**. То есть в предыдущих пунктах заменяем **полный балл** на **половину полного балла**.

## Code

- Place the source code for programming tasks in the `project` folder.
- Give files and modules meaningful names, following the officially accepted style.
- Structure the code by using both classes and well-defined functions.
The clearer the code, the faster it can be reviewed, and the more likely you are to receive full points.

## Tests

There are two types of tests: those prepared by the instructor and your own.

The instructor-prepared tests are located in the `tests/autotests` folder and are used to check tasks with fully automated grading.
When working with these tests, the following rules should be followed:

- In these tests, usually, only one block should be modified:
  ```python
  try:
      from project.task2 import regex_to_dfa, graph_to_nfa
  except ImportError:
      pytestmark = pytest.mark.skip("Task 2 is not ready to test!")
  ```
  In this block, you need to specify from which module(s) the required functions should be imported; otherwise, the tests will be skipped.
- If you find a bug **and** are ready to fix it, you can modify the file and then submit the change via a Pull Request to the main repository.
- If you find a bug and are not ready to fix it, you must urgently inform the instructor and take no further action!

The following rules apply to your own tests:

- Place tests for homework assignments in the `tests` folder.
- The naming format for test files is `test_[module/class/function being tested].py`.
- Use [`pytest`](https://docs.pytest.org/en/6.2.x/) to work with tests.
- To run the tests, you need to execute the following command from the root of the project:
  ```shell
  python ./scripts/run_tests.py
  ```

## Experiments

An experiment (setup, measurements, results, analysis of results) should be documented as a Python notebook, which is published on GitHub.
- To perform experiments, you will need not only the code but also the environment and some configuration.
Accordingly, the solution submitted should include instructions for setting up the environment and reproducing the experiments.
Ideally, all of this should be included in the notebook.
- Experiments should be reproducible (e.g., by reviewers).
- The notebook contains all the setup, code for the experiments, preparation of reports, and creation of graphs.
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
├── pyproject.toml - dependencies for repository setup
├── README.md - main information about the project
└── tasks.md - file with descriptions of homework assignments
```

__TODO: вот здесь русскую или английскую версию файлов лучше указать?__

## Course developers

- Semyon Grigorev [@gsvgit](https://github.com/gsvgit)
- Nikolai Ponomarev [@wowaster](https://github.com/WoWaster)
- Efim Kubishkin [@kubef](https://github.com/KubEF)
- Egor Orachyov [@EgorOrachyov](https://github.com/EgorOrachyov)
- Vadim Abzalov [@vadyushkins](https://github.com/vadyushkins)
- Rustam Azimov [@rustam-azimov](https://github.com/rustam-azimov)
- Ekaterina Shemetova [@katyacyfra](https://github.com/katyacyfra)

## Вместо введения

__TODO: этот раздел переводить?__

Данный курс является прикладным. Основная задача --- показать, что формальные языки возникают и могут применяться в разных областях. Примеры таких областей:

- Синтаксический анализ языков программирования: в компиляторах, интерпертаторах, средах разработки, других инстументах.
- Анализ естественных языков. Активность в этой области несколько спала, так как на передний план сейчас вышли различные методы машинного обучения.
  Однако и в этой области ведуться работы.Например, [International Conference on Parsing Technologies](http://www.wikicfp.com/cfp/program?id=1853).
- Статический анализ кода.
  - Различные задачи межпроцедурного анализа. Основной подход --- language reachability. Основоположник --- Томас Репс. Примеры работ.
    - Thomas Reps. 1997. Program analysis via graph reachability. In Proceedings of the 1997 international symposium on Logic programming (ILPS ’97). MIT Press, Cambridge, MA, USA, 5–19.
    - Qirun Zhang and Zhendong Su. 2017. Context-sensitive data-dependence analysis via linear conjunctive language reachability. In Proceedings of the 44th ACM SIGPLAN Symposium on Principles of Programming Languages (POPL 2017). Association for Computing Machinery, New York, NY, USA, 344–358. DOI:https://doi.org/10.1145/3009837.3009848
    - Kai Wang, Aftab Hussain, Zhiqiang Zuo, Guoqing Xu, and Ardalan Amiri Sani. 2017. Graspan: A Single-machine Disk-based Graph System for Interprocedural Static Analyses of Large-scale Systems Code. In Proceedings of the Twenty-Second International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS ’17). Association for Computing Machinery, New York, NY, USA, 389–404. DOI:https://doi.org/10.1145/3037697.3037744
    - Lu Y., Shang L., Xie X., Xue J. (2013) An Incremental Points-to Analysis with CFL-Reachability. In: Jhala R., De Bosschere K. (eds) Compiler Construction. CC 2013. Lecture Notes in Computer Science, vol 7791. Springer, Berlin, Heidelberg
  - Интерливинг (или шафл) языков для верификаци многопоточных программ.
    - [Approximating the Shuffle of Context-free Languages to Find Bugs in Concurrent Recursive Programs](http://uu.diva-portal.org/smash/get/diva2:442518/FULLTEXT01.pdf)
    - Flick N.E. (2015) Quotients of Unbounded Parallelism. In: Leucker M., Rueda C., Valencia F. (eds) Theoretical Aspects of Computing - ICTAC 2015. ICTAC 2015. Lecture Notes in Computer Science, vol 9399. Springer, Cham

  - Система типов Java: [Radu Grigore, Java Generics are Turing Complete](https://arxiv.org/abs/1605.05274).

- Графовые базы данных. Поиск путей с ограничениями.
    - Maurizio Nolé and Carlo Sartiani. 2016. Regular Path Queries on Massive Graphs. In Proceedings of the 28th International Conference on Scientific and Statistical Database Management (SSDBM ’16). Association for Computing Machinery, New York, NY, USA, Article 13, 1–12. DOI:https://doi.org/10.1145/2949689.2949711
    - Jochem Kuijpers, George Fletcher, Nikolay Yakovets, and Tobias Lindaaker. 2019. An Experimental Study of Context-Free Path Query Evaluation Methods. In Proceedings of the 31st International Conference on Scientific and Statistical Database Management (SSDBM ’19). Association for Computing Machinery, New York, NY, USA, 121–132. DOI:https://doi.org/10.1145/3335783.3335791
    - [Jelle Hellings. Querying for Paths in Graphs using Context-Free Path Queries.](https://arxiv.org/abs/1502.02242)

- Биоинформатика. В основном это анализ геномных и белковых последовательностей.
    - [Witold Dyrka, Mateusz Pyzik, Francois Coste, and Hugo Talibart. Estimating probabilistic context-free grammars for proteins using contact map constraints.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6428041/)
    - [James WJ Anderson, Paula Tataru, Joe Staines, Jotun Hein, and Rune Lyngso. Evolving stochastic context-free grammars for RNA secondary structure prediction.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3464655/)
    - [Ryan Zier-Vogel. Predicting RNA secondary structure using a stochastic conjunctive grammar.](https://www.semanticscholar.org/paper/Predicting-RNA-secondary-structure-using-a-grammar-Zier-Vogel/90bb312cb1a0f61eddb7a8b5b782bb40630894dd).

- Машинное обучение.
   - [Matt J. Kusner, Brooks Paige, José Miguel Hernández-Lobato. Grammar Variational Autoencoder](https://arxiv.org/abs/1703.01925). Опубликована в 2017 году и уже [больше 950 цитирований.](https://scholar.google.com/scholar?cites=4080460899049502885&as_sdt=2005&sciodt=0,5&hl=ru)
   - [TAG Parsing with Neural Networks and Vector Representations of Supertags](https://www.aclweb.org/anthology/D17-1180.pdf). К разговору об оброаботке естественных языков.
   - [Jungo Kasai, Robert Frank, Pauli Xu, William Merrill, Owen Rambow. End-to-end Graph-based TAG Parsing with Neural Networks.](https://arxiv.org/abs/1804.06610)

- Языки --- это не только про строки.
  - Языки деревьев: [Tree Automata Techniques and Applications](http://tata.gforge.inria.fr/).
  - Языки графов:
     - [Graph Grammars](http://www.its.caltech.edu/~matilde/GraphGrammarsLing.pdf)
     - [HYPEREDGE REPLACEMENT GRAPH GRAMMARS](https://people.cs.umu.se/drewes/biblio/ps-files/hrg.pdf)
     - [(Re)introducing Regular Graph Languages](https://www.aclweb.org/anthology/W17-3410.pdf)
     - [Hyperedge Replacement: Grammars and Languages](https://www.springer.com/gp/book/9783540560050)
  - $\ldots$
- Теория групп. Как правило, это проблема слов группы или дополнение к ней.
   - Anisimov, A.V. Group languages. Cybern Syst Anal (1971) 7: 594.
   - David E. Muller, Paul E. Schupp, Groups, the Theory of ends, and context-free languages, Journal of Computer and System Sciences, Volume 26, Issue 3, 1983, Pages 295-310, ISSN 0022-0000
   - HOLT, D., REES, S., ROVER, C., \& THOMAS, R. (2005). GROUPS WITH CONTEXT-FREE CO-WORD PROBLEM. Journal of the London Mathematical Society, 71(3), 643-657. doi:10.1112/S002461070500654X
   - [Groups with Context-Free Co-Word Problem and Embeddings into Thompson's Group V](https://arxiv.org/abs/1407.7745)
   - [Kropholler, R. \& Spriano, D. (2019). Closure properties in the class of multiple context-free groups. Groups Complexity Cryptology, 11(1), pp. 1-15. Retrieved 13 Feb. 2020, from doi:10.1515/gcc-2019-2004](https://www.degruyter.com/view/j/gcc.2019.11.issue-1/gcc-2019-2004/gcc-2019-2004.xml)
   - [Word problems of groups, formal languages and decidability](https://personalpages.manchester.ac.uk/staff/Mark.Kambites/events/nbsan/nbsan17_thomas.pdf)

- Прочая интересная математика.
  - Немного топологии в теории формальных языков: [Salvati S. On is an n-MCFL. – 2018.](https://hal.archives-ouvertes.fr/hal-01771670/)
  - Salvati S. MIX is a 2-MCFL and the word problem in Z2 is captured by the IO and the OI hierarchies //Journal of Computer and System Sciences. -- 2015. -- Т. 81. -- \textnumero. 7. -- С. 1252-1277.
  - О том, как задачи из теории графов связаны с теорией формальных языков: Abboud, Amir \& Backurs, Arturs \& Williams, Virginia. (2015). If the Current Clique Algorithms are Optimal, So is Valiant's Parser. 98-117. 10.1109/FOCS.2015.16.
  - [A context-free grammar for the Ramanujan-Shor polynomials](https://www.sciencedirect.com/science/article/abs/pii/S0196885819300739)
