# Задача 6. Преобразование грамматики в ОНФХ

* **Жёсткий дедлайн**: 03.04.2024, 23:59
* Полный балл: 14

## Задача

- [ ] Используя [возможности pyformlang для работы с контекстно-свободными грамматиками](https://pyformlang.readthedocs.io/en/latest/usage.html#context-free-grammar) реализовать **функцию** преобразования контекстно-свободной грамматики в ослабленную нормальную форму Хомского (ОНФХ).
  ```python
  def cfg_to_weak_normal_form(cfg: pyformlang.cfg.CFG) -> pyformlang.cfg.CFG:
      pass
  ```
- [ ] Реализовать **функцию**, основанную на алгоритме Хеллингса, решающую задачу достижимости между всеми парами вершин для заданного графа и заданной КС грамматики.
  - Для работы с графом использовать функции из предыдущих задач.
  ```python
  def cfpq_with_hellings(
    cfg: pyformlang.cfg.CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
  ) -> set[Tuple[int, int]]:
     pass
  ```
- [ ] Добавить необходимые тесты.
