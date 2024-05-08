# Задача 11. Язык запросов к графам

* **Жёсткий дедлайн**: 15.05.2024, 23:59
* Полный балл: 10

## Конкретный синтаксис
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

Пример запроса.

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

## Правила вывода типов

Константы типизируются очевидным образом.

Тип переменной определяется типом выражения, с которым она связана.
```
[b(v)] => t
_________________
[Var (v)](b) => t
```

Пересечение для двух КС не определено.

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

Остальные операции над автоматами типизируются согласно формальных свойств классов языков.
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

Запрос возвращает множество (вершин или пар вершин)

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


## Динамическая семантика языка запросов

Связывание переопределяет имя.

```
[e](b1) => x,b2
_____________________________________
[Bind (v, e)](b1) => (), (b1(v) <= x)

```

Результатом исполнения программы является словарь, где ключ --- имя переменной в связывании, у которого в правой части select, а значение --- результат вычисления соответствующего запроса.

## Задача
- [ ] С использованием ANTLR реализовать синтаксический анализатор предложенного выше языка. А именно, реализовать функцию, которая принимает строку и возвращает дерево разбора.
- [ ] Реализовать функцию, которая по дереву разбора возвращает количество узлов в нём.
- [ ] Реализовать функцию, которая по дереву разбора строит ранее разобранную строку.
- [ ] Расширить CI шагом генерации парсера по спецификации. Обратите внимание, что генерируемые по спецификации файлы не выкладываются в репозиторий.
  - [Grammarinator](https://github.com/renatahodovan/grammarinator), используемый нами для генерации тестов, подтягивает вместе с собой [ANTLeRinator](https://github.com/renatahodovan/antlerinator), который можно использовать для получения исполняемого файла ANTLR
  - Либо можно использовать более стандартные [antlr4-tools](https://github.com/antlr/antlr4-tools)

Требуемые функции:
```python
# Второе поле показывает корректна ли строка (True, если корректна)
def prog_to_tree(program: str) -> tuple[ParserRuleContext, bool]:
    pass

def nodes_count(tree: ParserRuleContext) -> int:
    pass

def tree_to_prog(tree: ParserRuleContext) -> str:
    pass
```
