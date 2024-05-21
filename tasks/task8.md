# Задача 8. Тензорный алгоритм решения задачи достижимости с КС ограничениями

* **Жёсткий дедлайн**: 24.04.2024, 23:59
* Полный балл: 14

## Задача

- [ ] Реализовать **функцию**, основанную на тензорном алгоритме, решающую задачу достижимости между всеми парами вершин для заданного графа и заданной КС грамматики.
  - Для преобразования грамматики в RSM использовать результаты предыдущих работ. Явно опишите **функции** преобразования CFG -> RSM и EBNF -> RSM
  - Для реализации матричных операций использовать [sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html).
  - Необходимые функции:
  ```python
  def cfpq_with_tensor(
    rsm: pyformlang.rsa.RecursiveAutomaton,
    graph: nx.DiGraph,
    final_nodes: set[int] = None,
    start_nodes: set[int] = None,
  ) -> set[tuple[int, int]]:
    pass


  def cfg_to_rsm(cfg: pyformlang.cfg.CFG) -> pyformlang.rsa.RecursiveAutomaton:
    pass


  def ebnf_to_rsm(ebnf: str) -> pyformlang.rsa.RecursiveAutomaton:
    pass
  ```
- [ ] Добавить необходимые тесты.
