# Задача 3. Регулярные запросы для всех пар вершин

* **Жёсткий дедлайн**: 28.02.2024, 23:59
* Полный балл: 5

## Задача

- [ ] Реализовать тип (FiniteAutomaton), представляющий конечный автомат в виде разреженной матрицы смежности из [sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html) и информации о стартовых и финальных вершинах. У типа должны быть конструкторы от DeterministicFiniteAutomaton и NondeterministicFiniteAutomaton из [Задачи 2](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/blob/main/tasks/task2.md).
- [ ] Реализовать функцию-интерпретатор для типа FiniteAutomaton, выясняющую, принимает ли автомат заданную строку.
  - Требуемая функция:
     ```python
    def accept(self, word: Iterable[Symbol]) -> bool:
      pass
    ```
- [ ] Используя [разреженные матрицы из sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html) реализовать **функцию** пересечения двух конечных автоматов через тензорное произведение.
  - Требуемая функция:
     ```python
    def intersect_automata(automaton1: FiniteAutomaton,
             automaton2: FiniteAutomaton) -> FiniteAutomaton:
        pass
    ```
- [ ] На основе предыдущей функции реализовать **функцию** выполнения регулярных запросов к графам: по графу с заданными стартовыми и финальными вершинами и регулярному выражению вернуть те пары вершин из заданных стартовых и финальных, которые связанны путём, формирующем слово из языка, задаваемого регулярным выражением.
  - Требуемая функция:
     ```python
    def paths_ends(graph: MultiDiGraph,
            regex:str) -> list[tuple[NodeView, NodeView]]:
        pass
    ```

  - Для конструирования регулярного запроса и преобразований графа использовать результаты [Задачи 2](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/blob/main/tasks/task2.md).
- [ ] Добавить необходимые тесты.
