# Задача 2. Построение детерминированного конечного автомата по регулярному выражению и недетерминированного конечного автомата по графу

* **Жёсткий дедлайн**: 28.02.2024, 23:59
* Полный балл: 5

## Задача

- [ ] Используя возможности [pyformlang](https://pyformlang.readthedocs.io/en/latest/) реализовать **функцию** построения минимального ДКА по заданному регулярному выражению. [Формат регулярного выражения](https://pyformlang.readthedocs.io/en/latest/usage.html#regular-expression).
  - Требуемая функция:
  ```python
  def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
      pass
  ```
- [ ] Используя возможности [pyformlang](https://pyformlang.readthedocs.io/en/latest/) реализовать **функцию** построения недетерминированного конечного автомата по [графу](https://networkx.org/documentation/stable/reference/classes/multidigraph.html), в том числе по любому из графов, которые можно получить, пользуясь функциональностью, реализованной в [Задаче 1](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/blob/main/tasks/task1.md) (загруженный из набора данных по имени граф, сгенерированный синтетический граф). Предусмотреть возможность указывать стартовые и финальные вершины. Если они не указаны, то считать все вершины стартовыми и финальными.
  - Требуемая функция:
  ```python
  def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
  ) -> NondeterministicFiniteAutomaton:
      pass
  ```
- [ ] Добавить собственные тесты при необходимости.
