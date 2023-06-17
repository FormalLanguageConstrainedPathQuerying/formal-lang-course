# Задача 13. Язык запросов к графам

## Описание абстрактного синтаксиса языка

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    Bool of bool
  | String of string
  | Int of int

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход

lambda = Lambda of List<var> * expr
```

Выразительные возможности лямбды должны позволять решать такие задачи как получение достижимых вершин, получение вершин
из которых достижимы некоторые, получение пар вершин, между которыми существует путь, удовлетворяющий ограничению.

## Описание конкретного синтаксиса

### Описание лексики

```

ID : NameStartChar NameChar*
   ;

NameChar : NameStartChar
   | '0'..'9'
   | '_'
   ;

NameStartChar
   : 'A'..'Z' | 'a'..'z'
   ;

COMMENT : '/*' .*? '*/' -> skip ;
WS : [ \r\t\n]+ -> skip ;

BOOL : 'true' | 'false' ;
INT : [0-9]+ ;
STRING : '"' ( '\\"' | . )*? '"' ;
```

### Описание синтаксиса

```
prog -> ( stmt ; | COMMENT )* EOF ;

stmt -> bind | print ;
bind -> 'let' ID '=' expr ;
print -> 'print' expr ;

val -> BOOL | INT | STRING | set;
var -> ID ;
set -> '{' '}'                    // множество
     | '{' expr (',' expr ) '}'
     | '{' INT '...' INT '}'      // range of INTs [a, b)


expr = '(' expr ')'             // скобки указывают приоритет операций
  | var                         // переменные
  | val                         // константы
  | set_start expr 'to' expr    // задать множество стартовых состояний
  | set_final expr 'to' expr    // задать множество финальных состояний
  | add_start expr 'to' expr    // добавить состояния в множество стартовых
  | add_final expr 'to' expr    // добавить состояния в множество финальных
  | get_start expr              // получить множество стартовых состояний
  | get_final expr              // получить множество финальных состояний
  | get_reachable expr          // получить все пары достижимых вершин
  | get_vertices expr           // получить все вершины
  | get_edges expr              // получить все рёбра
  | get_labels expr             // получить все метки
  | map lambda 'of' expr        // классический map
  | filter lambda 'of' expr     // классический filter
  | load  STRING                // загрузка графа
  | expr '&' expr               // пересечение языков, множеств
  | expr '|' expr               // конкатенация языков
  | expr '+' expr               // объединение языков, множеств
  | '*' expr                    // замыкание языков (звезда Клини)
  | expr >> expr                // единичный переход  symb >> lang
  | expr in expr                // проверка наличия в множестве

lambda -> args '->' '{' expr '}' ;
args -> var
      | '(' args (, args) * ')'
```

Пример запроса в конкретном синтаксисе.

```
let g' = load "wine";

let g = set_start {0...100} to (set_finals (get_vertices g') to g');

let l1 = "l1" | "l2";

let q1 = ("type" | l1)*;
let q2 = "abc" >> g;

let res1 = g & q1;
let res2 = g & q2;

print res1;

let s = get_reachable g;

let vertices1 = filter v -> {v in s} of (map ((u_g,u_q1),l,(v_g,v_q1)) -> {u_g} (get_edges res1));
let vertices2 = filter v -> {v in s} of (map ((u_g,u_q2),l,(v_g,v_q2)) -> {u_g} (get_edges res2));
let vertices = vertices1 & vertices2;

print vertices;
```

## Правила вывода типов

Константы типизируются очевидным образом.

Тип переменной определяется типом выражения, с которым она связана.

```
[b(v)] => t
_________________
[Var (v)](b) => t
```

Загрузить можно только автомат.

```
_________________________
[Load (p)](b) => FA<int>
```

Установка финальных состояний, а так же добавление стартовых и финальных типизируется аналогично типизации установки
стартовых, которая приведена ниже.

```
[s](b) => Set<t> ;  [e](b) => FA<t>
___________________________________
[Set_start (s, e)](b) => FA<t>


[s](b) => Set<t> ;  [e](b) => RSM<t>
____________________________________
[Set_start (s, e)](b) => RSM<t>
```

Получение финальных типизируется аналогично получению стартовых, правила для которого приведены ниже.

```
[e](b) => FA<t>
____________________________
[Get_start (e)](b) => Set<t>


[e](b) => RSM<t>
____________________________
[Get_start (e)](b) => Set<t>

```

```
[e](b) => FA<t>
__________________________________
[Get_reachable (e)](b) => Set<t*t>


[e](b) => RSM<t>
__________________________________
[Get_reachable (e)](b) => Set<t*t>

```

```
[e](b) => FA<t>
_______________________________
[Get_vertices (e)](b) => Set<t>


[e](b) => RSM<t>
_______________________________
[Get_vertices (e)](b) => Set<t>


[e](b) => FA<t>
______________________________________
[Get_edges (e)](b) => Set<t*string*t>


[e](b) => RSM<t>
______________________________________
[Get_edges (e)](b) => Set<t*string*t>

[e](b) => FA<t>
__________________________________
[Get_labels (e)](b) => Set<string>


[e](b) => RSM<t>
__________________________________
[Get_labels (e)](b) => Set<string>

```

Правила для ```map``` и ```filter``` традиционные.

```
[f](b) => t1 -> t2 ; [q](b) => Set<t1>
_______________________________________
[Map (f,q)](b) => Set<t2>


[f](b) => t1 -> bool ; [q](b) => Set<t1>
________________________________________
[Filter (f,q)](b) => Set<t1>
```

Пересечение для двух КС не определено.

```
[e1](b) => FA<t1> ;  [e2](b) => FA<t2>
______________________________________
[Intersect (e1, e2)](b) => FA<t1*t2>


[e1](b) => FA<t1> ;  [e2](b) => RSM<t2>
_______________________________________
[Intersect (e1, e2)](b) => RSM<t1*t2>


[e1](b) => RSM<t1> ;  [e2](b) => FA<t2>
_______________________________________
[Intersect (e1, e2)](b) => RSM<t1*t2>

```

Остальные операции над автоматами типизируются согласно формальных свойств классов языков.

```
[e1](b) => FA<t> ;  [e2](b) => FA<t>
_____________________________________
[Concat (e1, e2)](b) => FA<t>


[e1](b) => FA<t> ;  [e2](b) => RSM<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => FA<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => RSM<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>

```

```
[e1](b) => FA<t> ;  [e2](b) => FA<t>
______________________________________
[Union (e1, e2)](b) => FA<t>


[e1](b) => FA<t> ;  [e2](b) => RSM<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => FA<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => RSM<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>

```

```
[e](b) => FA<t>
______________________
[Star (e)](b) => FA<t>


[e](b) => RSM<t>
______________________
[Star (e)](b) => RSM<t>

```

```
[e](b) => string
________________________
[Smb (e)](b) => FA<int>

```

## Динамическая семантика языка запросов

Связывание переопределяет имя.

```
[e](b1) => x,b2
_____________________________________
[Bind (v, e)](b1) => (), (b1(v) <= x)

```

Загрузить можно только автомат и у него все вершины будут стартовыми и финальными.

```
[p](b1) => s,b2 ; read_fa_from_file s => fa
_____________________________________
[Load (p)](b1) => (fa | fa.start = fa.vertices, fa.final = fa.vertices), b1

```


Генерация парсера:
```shell
rm -rf parser/MyGQL*
antlr4 -o parser MyGQL.g4  -Dlanguage=Python3 -visitor
```
