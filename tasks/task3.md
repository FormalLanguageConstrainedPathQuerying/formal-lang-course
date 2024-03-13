# Задача 3. Регулярные запросы для всех пар вершин

* **Жёсткий дедлайн**: 06.03.2024, 23:59
* Полный балл: 5

## Задача

  - Требуемые функции:
     ```python
    def accepts(self, word: Iterable[Symbol]) -> bool:
      pass
    def is_empty(self) -> bool:
      pass
    ```
- [x] Используя [разреженные матрицы из sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html) реализовать **функцию** пересечения двух конечных автоматов через тензорное произведение.
  - Требуемая функция:
     ```python
    def intersect_automata(automaton1: FiniteAutomaton,
             automaton2: FiniteAutomaton) -> FiniteAutomaton:
        pass
    ```
- [x] На основе предыдущей функции реализовать **функцию** выполнения регулярных запросов к графам: по графу с заданными стартовыми и финальными вершинами и регулярному выражению вернуть те пары вершин из заданных стартовых и финальных, которые связанны путём, формирующем слово из языка, задаваемого регулярным выражением.
  - Требуемая функция:
     ```python
    def paths_ends(graph: MultiDiGraph, start_nodes: set[int],
           final_nodes: set[int], regex:str) -> list[tuple[NodeView, NodeView]]:
        pass
    ```

  - Для конструирования регулярного запроса и преобразований графа использовать результаты [Задачи 2](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/blob/main/tasks/task2.md).
- [ ] Добавить необходимые тесты.
