# Задача 13. Язык запросов к графам

* **Мягкий дедлайн**: 24.10.2021, 23:59
* **Жёсткий дедлайн**: 27.10.2021, 23:59
* Полный балл: 5

## Описание абстрактного синтаксиса языка

```
prog = List<stmt>

stmt =

bind of var*expr

expr =
    Var of var
  | Val of val
  | Set_start of Set<int> * expr
  | Set_final of Set<int> * expr
  | Add_start of Set<int> * expr
  | Add_final of Set<int> * expr
  | Load of path // только для графов
  | Intersect of expr * expr
  | Concat of expr * expr
  | Union of expr * expr
  | Star of expr
```

## Задача

В дополнение к существующему в pyformalng формату описания КС грамматик зафиксируем следующий формат.
- Для каждого нетерминала существует ровно одно правило.
- На одной строке содержится ровно одно правило.
- Правило --- это нетерминал и регулярное выражение над терминалами и нетерминалами, принимаемое pyformalng, разделенные ``` -> ```. Например: ``` S -> a | b* S ```

- [ ] Реализовать тип для представления рекурсивных конечных автоматов. В качестве составных частей можно использовать типы из pyformlang (например, [конечные автоматы](https://pyformlang.readthedocs.io/en/latest/usage.html#finite-automata)). При проектировании этого типа необходимо помнить, что рекурсивные конечные автоматы будут использоваться в алгоритмах КС достижимости, основанных на линейной алгебре, а значит необходимо будет строить матрицы смежности. Здесь могут быть полезны результаты домашних работ по конечным автоматам.
- [ ] Используя [возможности pyformlang для работы с контекстно-свободными грамматиками](https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html), [регулярными выражениями](https://pyformlang.readthedocs.io/en/latest/usage.html#regular-expression) и [конечными автоматами](https://pyformlang.readthedocs.io/en/latest/usage.html#finite-automata), реализовать **функцию** преобразования контекстно-свободной грамматики в стандартном формате pyformlang в рекурсивный конечный автомат.
- [ ] Используя [возможности pyformlang для работы с контекстно-свободными грамматиками](https://pyformlang.readthedocs.io/en/latest/modules/context_free_grammar.html), [регулярными выражениями](https://pyformlang.readthedocs.io/en/latest/usage.html#regular-expression) и [конечными автоматами](https://pyformlang.readthedocs.io/en/latest/usage.html#finite-automata), реализовать **функцию** преобразования контекстно-свободной грамматики в новом формате (с регулярными выражениями в правых частях правил) в рекурсивный конечный автомат.
- [ ] Реализовать **функцию** минимизации рекурсивного конечного автомата.
- [ ] Добавить необходимые тесты.
