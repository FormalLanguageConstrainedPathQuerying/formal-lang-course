# Tasks for "Formal Languages" course

- [Tasks for "Formal Languages" course](#tasks-for-formal-languages-course)
  - [Task 1. Initializing the Working Environment](#task-1-initializing-the-working-environment)
  - [Task 2. Constructing a DFA from a Regular Expression and a NFA from a Graph](#task-2-constructing-a-dfa-from-a-regular-expression-and-a-nfa-from-a-graph)
  - [Task 3. All-pairs RPQ algorithm](#task-3-all-pairs-rpq-algorithm)
  - [Task 4. Multiple-source BFS-based RPQ algorithm](#task-4-multiple-source-bfs-based-rpq-algorithm)
  - [Task 5. Experimental Study of RPQ algorithms](#task-5-experimental-study-of-rpq-algorithms)
  - [Task 6. Weak Chomsky Normal Form (wCNF) transformation, Helling's CFPQ Algorithm](#task-6-weak-chomsky-normal-form-wcnf-transformation-hellings-cfpq-algorithm)
  - [Task 7. Matrix multiplication based CFPQ algorithm](#task-7-matrix-multiplication-based-cfpq-algorithm)
  - [Task 8. Kronecker product based CFPQ algorithm](#task-8-kronecker-product-based-cfpq-algorithm)
  - [Task 9. GLL-based CFPQ algorithm](#task-9-gll-based-cfpq-algorithm)
  - [Task 10. Experimental Study of CFPQ algorithms](#task-10-experimental-study-of-cfpq-algorithms)
  - [Task 11. Graph Query Language](#task-11-graph-query-language)
    - [Concrete Syntax](#concrete-syntax)
    - [Type Inference Rules](#type-inference-rules)
    - [Dynamic Semantics of the Query Language](#dynamic-semantics-of-the-query-language)
    - [Task](#task)
  - [Task 12. Graph Query Language Interpreter](#task-12-graph-query-language-interpreter)

## Task 1. Initializing the Working Environment

> Max score: 5

- [ ] Fork this repository.
- [ ] Share a link to your fork with the instructor.
- [ ] Add one of the assistants as a co-owner of your fork (instructor will tell you, who your assistant is).
- [ ] Implement a module that provides the following functionalities.
  For working with graphs, use [cfpq-data](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/tutorial.html#graphs).
  This module will be extended in the future. The functions to implement:
  - [ ] Given the graph name, return the number of vertices, edges, and list the different labels that appear on the edges.
    To get the graph by name, use [this function](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/tutorial.html#load-graph).
  - [ ] Based on the number of vertices in cycles and the labels of the edges, construct a [graph of two cycles](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/reference/graphs/generated/cfpq_data.graphs.generators.labeled_two_cycles_graph.html#cfpq_data.graphs.generators.labeled_two_cycles_graph) and save it to a specified file in DOT format (use pydot).
- [ ] Add necessary tests.


## Task 2. Constructing a DFA from a Regular Expression and a NFA from a Graph

> Max score: 5

- [ ] Using the features of [pyformlang](https://pyformlang.readthedocs.io/en/latest/), implement a **function** to build the minimal DFA (Deterministic Finite Automaton) from a given regular expression. [Regular expression format](https://pyformlang.readthedocs.io/en/latest/usage.html#regular-expression).
  - Required function:
  ```python
  def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
      pass
  ```
- [ ] Using the features of [pyformlang](https://pyformlang.readthedocs.io/en/latest/), implement a **function** to build a Non-Deterministic Finite Automaton (NFA) from a [graph](https://networkx.org/documentation/stable/reference/classes/multidigraph.html), including any of the graphs that can be obtained using the functionality implemented in [Task 1](#task-1-initializing-the-working-environment) (loaded from the dataset by graph name or a generated synthetic graph).
Ensure the ability to specify start and final states.
If they are not specified, assume all vertices are start and final states.
  - Required function:
  ```python
  def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
  ) -> NondeterministicFiniteAutomaton:
      pass
  ```
- [ ] Add your own tests as needed.

## Task 3. All-pairs RPQ algorithm

> Max score: 5

- [ ] Implement a type (`AdjacencyMatrixFA`) that represents a finite automaton as a sparse adjacency matrix from [sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html) (or its Boolean decomposition) along with information about start and final vertices.
  Instances must be initialized with `DeterministicFiniteAutomaton` and `NondeterministicFiniteAutomaton` (the first being a subclass of the second, so they can be handled interchangeably) from [Task 2](#task-2-constructing-a-dfa-from-a-regular-expression-and-a-nfa-from-a-graph).
- [ ] Implement an interpreter function for the `AdjacencyMatrixFA` type that determines whether the automaton accepts a given string and whether the language defined by the automaton is empty.
  It is recommended to use the transitive closure of the adjacency matrix to implement the second function.
  - Required functions:
     ```python
    def accepts(self, word: Iterable[Symbol]) -> bool:
      pass
    def is_empty(self) -> bool:
      pass
    ```
- [ ] Using [sparse matrices from sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html), implement a **function** to compute the intersection of two finite automata by computing tensor product.
  - Required function:
     ```python
    def intersect_automata(automaton1: AdjacencyMatrixFA,
             automaton2: AdjacencyMatrixFA) -> AdjacencyMatrixFA:
        pass
    ```
- [ ] Based on the previous function, implement a **function** to evaluate regular path queries on graphs: given a graph with specified start and final vertices and a regular expression, return the pairs of vertices from the start and final vertices that are connected by a path forming a word from the language defined by the regular expression.
  - Required function:
     ```python
    def tensor_based_rpq(regex: str, graph: MultiDiGraph, start_nodes: set[int],
           final_nodes: set[int]) -> set[tuple[int, int]]:
        pass
    ```

  - To construct the regular query and graph transformations, use the results from [Task 2](#task-2-constructing-a-dfa-from-a-regular-expression-and-a-nfa-from-a-graph).
- [ ] Add your own tests as needed.

## Task 4. Multiple-source BFS-based RPQ algorithm

> Max score: 8

- [ ] Using [sparse matrices from sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html), implement a **function** for reachability with regular constraints for multiple start vertices (algorithm based on multiple source BFS and linear algebra).
  - To construct the regular query and graph, use the results from [Task 2](#task-2-constructing-a-dfa-from-a-regular-expression-and-a-nfa-from-a-graph).
  - Required function:
  ```python
  def ms_bfs_based_rpq(regex: str, graph: MultiDiGraph, start_nodes: set[int],
           final_nodes: set[int]) -> set[tuple[int, int]]:
    pass
  ```
- [ ] Add your own tests as needed.

## Task 5. Experimental Study of RPQ algorithms

> Max score: 15

This task is dedicated to the performance analysis of the algorithm for solving the reachability problem between all pairs of vertices with a given set of start vertices under regular constraints.

The following reachability problems, solved in previous tasks, are investigated:
- Reachability between all pairs of vertices.
- Reachability for each vertex from the given set of start vertices.

Questions that need to be answered during the research:
- Which sparse matrix and vector representation is best suited for each of the problems being solved?
- Starting from what size of the starting set is it more advantageous to solve the problem for all pairs and select the required ones?

The solution to this task should be presented as a Python notebook.
In order to ensure the possibility of verification, the notebook must be self-contained: it should include all actions necessary to reproduce the experiment.
Additionally, the notebook should include a report and an analysis of the results of your experiments in textual form.
The report should be accompanied by diagrams, tables, and images, if necessary, to explain the results.

The solution is not just code, but an experimental research report that should be a connected text containing (at least) the following sections:
- Problem statement
- Description of the solutions being researched
- Description of the dataset for the experiments
  - Graphs
  - Queries
- Description of the experiment
  - Hardware
  - What and how was measured, and how these measurements should help answer the questions posed
- Experiment results
  - Graphs, tables
- Analysis of the experiment results
  - Answers to the posed questions, with reasoning for the answers

For setting up the experiments and basic analysis of the results, it will be helpful to refer to [this cheat sheet (in Russian)](https://github.com/spbu-se/measurements/blob/main/measurements_cheat_sheet.pdf).
For writing the report, you may find inspiration in the recommendations [here (in Russian)](https://github.com/spbu-se/matmex-diploma-template/blob/master/040_experiment.tex).

- [ ] Create a Python notebook and include the necessary dependencies.
- [ ] Include solutions from previous tasks.
- [ ] Prepare the dataset.
  - [ ] Choose several graphs from the [collection](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/index.html).
    Be sure to justify why you selected these particular graphs.
  - [ ] Using the function from the first homework, find the edge labels of the graphs and, based on this information, formulate at least four different queries for each graph. It's better to use the most frequent labels.
    Query requirements:
      - Queries for all graphs should follow a common template. For example, if there are graphs `g1` and `g2` with different label sets, the queries might look like:
        - `g1`:
          - `(l1 | l2)* l3`
          - `(l3 | l4)+ l1*`
          - `l1 l2 l3 (l4|l1)*`
        - `g2`:
          - `(m1 | m3)* m2`
          - `(m1 | m3)+ m2*`
          - `m1 m2 m3 (m3|m1)*`
      - The queries should use all commonly accepted regular expression constructs (closure, concatenation, alternation). That is, at least one query for each graph must contain each of these constructs.
  - [ ] To generate the sets of start vertices, use [this function](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/reference/graphs/generated/cfpq_data.graphs.utils.multiple_source_utils.html#cfpq_data.graphs.utils.multiple_source_utils.generate_multiple_source).
    Remember that the computation time of the query depends heavily on how the start set is constructed.
- [ ] Formulate the stages of the experiment. What needs to be done to answer the posed questions? Why?
- [ ] Perform the necessary experiments and measurements.
- [ ] Present the results of the experiments.
- [ ] Analyze the results.
  - [ ] Answer the posed questions.
  - [ ] Justify the answers (using the results from the experiments).
- [ ] Don't forget to publish the notebook in the repository.

## Task 6. Weak Chomsky Normal Form (wCNF) transformation, Helling's CFPQ Algorithm

> Max score: 10

- [ ] Using [pyformlang capabilities for working with context-free grammars](https://pyformlang.readthedocs.io/en/latest/usage.html#context-free-grammar), implement a **function** that transforms a context-free grammar into a weak Chomsky Normal Form (wCNF).
  ```python
  def cfg_to_weak_normal_form(cfg: pyformlang.cfg.CFG) -> pyformlang.cfg.CFG:
      pass
  ```
- [ ] Implement a **function**, based on Hellings' algorithm, to solve the reachability problem between all pairs of vertices for a given graph and a given context-free grammar (not necessarily in wCNF).
  - For working with the graph, use functions from previous tasks.
  ```python
  def hellings_based_cfpq(
    cfg: pyformlang.cfg.CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
  ) -> set[tuple[int, int]]:
     pass
  ```
- [ ] Add custom tests if necessary.

## Task 7. Matrix multiplication based CFPQ algorithm

> Max score: 10

- [ ] Implement a **function**, based on the matrix algorithm, that solves the reachability problem between all pairs of vertices for a given graph and a given context-free grammar.
  - Use the results from previous tasks for transforming the grammar into wCNF.
  - Use [sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html) for matrix operations.
    ```python
    def matrix_based_cfpq(
        cfg: pyformlang.cfg.CFG,
        graph: nx.DiGraph,
        start_nodes: Set[int] = None,
        final_nodes: Set[int] = None,
    ) -> set[tuple[int, int]]:
      pass
    ```
- [ ] Add custom tests if necessary.

## Task 8. Kronecker product based CFPQ algorithm

> Max score: 10

- [ ] Implement a **function**, based on the tensor algorithm, that solves the reachability problem between all pairs of vertices for a given graph and a given context-free grammar.
  - Use results from previous tasks for transforming the grammar into RSM. Explicitly describe **functions** for transforming CFG -> RSM and EBNF -> RSM.
  - Use [sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html) for matrix operations.
  - Required functions:
  ```python
  def tensor_based_cfpq(
    rsm: pyformlang.rsa.RecursiveAutomaton,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
  ) -> set[tuple[int, int]]:
    pass

  def cfg_to_rsm(cfg: pyformlang.cfg.CFG) -> pyformlang.rsa.RecursiveAutomaton:
    pass

  def ebnf_to_rsm(ebnf: str) -> pyformlang.rsa.RecursiveAutomaton:
    pass
  ```
- [ ] Add custom tests if necessary.

## Task 9. GLL-based CFPQ algorithm

> Max score: 15

- [ ] Implement a **function**, based on the Generalized LL algorithm (working with RSM), that solves the reachability problem between all pairs of vertices for a given graph and a given context-free grammar.
  - Use functions from previous tasks for working with graphs and RSM.
  - Required function:
  ```python
  def gll_based_cfpq(
        rsm: pyformlang.rsa.RecursiveAutomaton,
        graph: nx.DiGraph,
        start_nodes: set[int] = None,
        final_nodes: set[int] = None,
    ) -> set[tuple[int, int]]:
    pass
  ```
- [ ] Add custom tests if necessary.

## Task 10. Experimental Study of CFPQ algorithms

> Max score: 20

This task is dedicated to analyzing the performance of different algorithms for solving the reachability problem between all pairs of vertices with context-free constraints: the Helling's algorithm, the matrix algorithm, the tensor algorithm, and the algorithm based on GLL.
During the analysis, the following questions need to be answered:
- Which of the four algorithms has the best performance?
- Does it make sense to use CFPQ algorithms to solve the PRQ problem (since regular expressions are a special case of CFG) or is it better to use specialized algorithms for regular constraints?
- How does the grammar affect the performance of the tensor algorithm and the GLL-based algorithm?
  If we fix the language, how do the properties of the grammar (size, (non)ambiguity) affect performance?

The solution to this task should be presented as a Python notebook.
To ensure the possibility of verification, the notebook must be self-contained: it should include all actions necessary to reproduce the experiment.
The notebook should also contain a report and analysis of the results of your experiments in textual form.
The report should be accompanied by diagrams, tables, and images, if necessary, to explain the results.

The solution is not just code but a report on the experimental study, which should be a coherent text and contain (at least) the following sections:
- Problem Statement
- Description of the solutions under study
- Description of the dataset for the experiments
  - Graphs
  - Queries
- Experiment Description
  - Hardware
  - What was measured, how these measurements help answer the research questions
- Experimental Results
  - Graphs, tables
- Analysis of Experimental Results
  - Answers to the research questions, argumentation for the answers

- [ ] Create a Python notebook and include the necessary dependencies.
- [ ] Include the necessary solutions from previous tasks.
- [ ] Prepare the dataset.
  - [ ] Choose some graphs from the [set](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/index.html).
    Be sure to justify why you chose these specific graphs.
    Note that the set includes graphs and grammars for different application domains (RDF analysis, pointer analysis in C, Java program analysis).
    It is recommended to choose graphs related to different areas.
  - [ ] As queries, it is suggested to use grammars from the "Canonical grammars" section in the description of the corresponding graph ([example](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/data/taxonomy_hierarchy.html#canonical-grammars)).
    If necessary (e.g., when answering the third question), you can "optimize" the grammar by manually creating an optimal RSM, or conversely, transform it into a weak Chomsky Normal Form (wCNF), or make it (non)ambiguous.
- [ ] Define the steps of the experiment.
  What needs to be done to answer the research questions? Why?
- [ ] Conduct the necessary experiments and measurements.
- [ ] Present the experimental results.
- [ ] Analyze the results.
  - [ ] Answer the research questions.
  - [ ] Justify the answers (using the results obtained from the experiments).
- [ ] Don't forget to publish the notebook in the repository.

## Task 11. Graph Query Language

> Max score: 15

### Concrete Syntax
```
prog = stmt*

stmt = bind | add | remove | declare

declare = 'let' VAR 'is' 'graph'

bind = 'let' VAR '=' expr

remove = 'remove' ('vertex' | 'edge' | 'vertices') expr 'from' VAR

add = 'add' ('vertex' | 'edge') expr 'to' VAR

expr = NUM | CHAR | VAR | edge_expr | set_expr | regexp | select

set_expr = '[' expr (',' expr)* ']'

edge_expr = '(' expr ',' expr ',' expr ')'

regexp = CHAR | VAR | '(' regexp ')' | (regexp '|' regexp) | (regexp '^' range) | (regexp '.' regexp) | (regexp '&' regexp)

range = '[' NUM '..' NUM? ']'

select = v_filter? v_filter? 'return' VAR (',' VAR)? 'where' VAR 'reachable' 'from' VAR 'in' VAR 'by' expr

v_filter = 'for' VAR 'in' expr

VAR = [a..z] [a..z 0..9]*
NUM = 0 | ([1..9] [0..9]*)
CHAR = '"' [a..z] '"'

```

Example query:

```
let g is graph

add edge (1, "a", 2) to g
add edge (2, "a", 3) to g
add edge (3, "a", 1) to g
add edge (1, "c", 5) to g
add edge (5, "b", 4) to g
add edge (4, "b", 5) to g

let q = "a"^[1..3] . q . "b"^[2..3] | "c"

let r1 = for v in [2] return u where u reachable from v in g by q

add edge (5, "d", 6) to g

let r2 = for v in [2,3] return u,v where u reachable from v in g by (q . "d")

```

### Type Inference Rules

Constants are typed obviously.

The type of a variable is determined by the type of the expression it is bound to.
```
[b(v)] => t
_________________
[Var (v)](b) => t
```

Intersection for two CFGs is not defined.

```
[e1](b) => FA ;  [e2](b) => FA
______________________________________
[Intersect (e1, e2)](b) => FA


[e1](b) => FA ;  [e2](b) => RSM
_______________________________________
[Intersect (e1, e2)](b) => RSM


[e1](b) => RSM ;  [e2](b) => FA
_______________________________________
[Intersect (e1, e2)](b) => RSM

```

Other operations on automata are typed according to formal properties of language classes.
```
[e1](b) => FA ;  [e2](b) => FA
_____________________________________
[Concat (e1, e2)](b) => FA


[e1](b) => FA ;  [e2](b) => RSM
______________________________________
[Concat (e1, e2)](b) => RSM


[e1](b) => RSM ;  [e2](b) => FA
______________________________________
[Concat (e1, e2)](b) => RSM


[e1](b) => RSM ;  [e2](b) => RSM
______________________________________
[Concat (e1, e2)](b) => RSM

```

```
[e1](b) => FA ;  [e2](b) => FA
______________________________________
[Union (e1, e2)](b) => FA


[e1](b) => FA ;  [e2](b) => RSM
_______________________________________
[Union (e1, e2)](b) => RSM


[e1](b) => RSM ;  [e2](b) => FA
_______________________________________
[Union (e1, e2)](b) => RSM


[e1](b) => RSM ;  [e2](b) => RSM
_______________________________________
[Union (e1, e2)](b) => RSM

```

```
[e](b) => FA
______________________
[Repeat (e)](b) => FA


[e](b) => RSM
______________________
[Repeat (e)](b) => RSM

```

```
[e](b) => char
________________________
[Symbol (e)](b) => FA

```

The query returns a set (of vertices or pairs of vertices)

```
[e](b) => Set<int>
_______________________________
[VFilter (v, e)](b) => Set<int>


[q](b) => RSM, [ret](b) => int
_____________________________________________________
[Select (vf1, vf2, ret, v1, v2, g, q)](b) => Set<int>


[q](b) => FA, [ret](b) => int
_____________________________________________________
[Select (vf1, vf2, ret, v1, v2, g, q)](b) => Set<int>


[q](b) => FA, [ret](b) => int * int
____________________________________________________________
[Select (vf1, vf2, ret, v1, v2, g, q)](b) => Set<int * int>


[q](b) => RSM, [ret](b) => int * int
____________________________________________________________
[Select (vf1, vf2, ret, v1, v2, g, q)](b) => Set<int * int>

```


### Dynamic Semantics of the Query Language

Binding overrides the name.

```
[e](b1) => x,b2
_____________________________________
[Bind (v, e)](b1) => (), (b1(v) <= x)

```

The result of executing the program is a dictionary where the key is the variable name in the binding, which has a `select` on the right side, and the value is the result of computing the corresponding query.

### Task
- [ ] Using ANTLR, implement a parser for the query language defined above.
  Specifically, implement a function that takes a string and returns the parse tree.
- [ ] Implement a function that returns the number of nodes in the parse tree.
  **Make sure to use ANTLR's tree traversal mechanisms**.
- [ ] Implement a function that takes the parse tree and reconstructs the original string.
  **Ensure to use ANTLR's tree traversal mechanisms**.
- [ ] Extend the CI pipeline with a step to generate the parser from the specification. Note that the generated parser files should not be included in the repository.
  - Use standard [antlr4-tools](https://github.com/antlr/antlr4-tools) to obtain ANTLR in CI.

Required functions:
```python
# The second field indicates whether the string is correct (True if correct)
def program_to_tree(program: str) -> tuple[ParserRuleContext, bool]:
    pass

def nodes_count(tree: ParserRuleContext) -> int:
    pass

def tree_to_program(tree: ParserRuleContext) -> str:
    pass
```
## Task 12. Graph Query Language Interpreter

> Max score: 22

In this task, you need to develop an interpreter for the query language created in the previous task.
Use the algorithms implemented in the previous tasks to evaluate the queries.
In addition to the implementation, you must provide minimal documentation explaining the decisions made during the implementation process (for example, in a README).

Note that in addition to the interpreter itself, you also need to implement type inference.
This functionality should be testable in isolation.
In fact, a separate function should be implemented that, given the parse tree, outputs the types and throws an exception if the program cannot be correctly typed.

- [ ] Implement a type inference mechanism that guarantees the correctness of query construction (in particular, ensuring that the intersection of two context-free languages is not constructed, or that sets of vertices are defined with valid types).
   - The type system should follow the rules specified in the previous task.
   - Try to make error messages as user-friendly as possible.
- [ ] From the set of algorithms implemented in previous tasks for executing graph queries, choose those that will be used in the interpreter.
  Justify your choice (write it down in the documentation).
- [ ] Using the parser from the previous task, the type inference system, and the chosen algorithms, implement the interpreter for the language described in the previous task.
   - You need to implement a function that, given the parse tree provided by ANTLR, returns a dictionary containing, for all bindings where the right-hand side is `select`, the name (left-hand side of the binding) as the key, and the result of executing the corresponding query as the value.
   - Ensure that error messages are appropriate.
    This will make debugging easier for you.
   - Make the most of ANTLR's capabilities for working with the parse tree.
- [ ] Add the necessary tests.

Required functions:

```python
def typing_program(program: str) -> bool:
  pass

def exec_program(program: str) -> dict[str, set[tuple]]:
  pass
```
