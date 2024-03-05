# Задача 4. Регулярные запросы для нескольких стартовых вершин

* **Мягкий дедлайн**: 16.03.2023, 23:59
* **Жёсткий дедлайн**: 19.03.2023, 23:59
* Полный балл: 5

## Задача

- [ ] Используя [разреженные матрицы из sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html) реализовать **функцию** достижимости с регулярными ограничениями.
  - Для конструирования регулярного запросов и графа использовать [Задачи 2](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/blob/main/tasks/task2.md).
  - Для всех стартовых вывести множество достижимых.
  - Требуемая функция:
  ```python
  def reachability_with_constraints(fa: FiniteAutomaton,
                           constraints_fa: FiniteAutomaton) -> dict[int, set[int]]:
    pass
  ```
- [ ] Добавить необходимые тесты.
