# Язык запросов к графам

## Абстрактный синтаксис

```
prog = List<stmt>

stmt =
    Bind of var * expr
  | Print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Regex of string
  | Cfg of string

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of expr * expr     // задать множество стартовых состояний
  | Set_final of expr * expr     // задать множество финальных состояний
  | Add_start of expr * expr     // добавить состояния в множество стартовых
  | Add_final of expr * expr     // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load_dot of path             // загрузка графа из дот файла
  | Load_graph of string         // загрузка графа из базы данных
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Contains of expr * expr      // вхождение элемента в множество
  | Set of List<expr>            // классическое ножество

pattern =
    PatVar of var
  | PatWild 
  | PatTuple of List<pattern>

lambda = List<pattern> * expr
```

## Конкретный синтаксис

```
prog -> (statement EOL)*

stmt ->
      var '=' expr
    | 'print' expr

expr ->
      var
    | val
    | bool
    | set
    | '(' expr ')'

graph ->
      var
    | REGEX
    | CFG
    | graph '.' 'set_starts' '(' set? ')'
    | graph '.' 'set_finals' '(' set? ')'
    | graph '.' 'add_starts' '(' set ')'
    | graph '.' 'add_finals' '(' set ')'
    | 'load_dot' '(' (var | STR) ')'
    | 'load_graph' '(' (var | STR) ')'
    | 'intersect(' graph ',' graph ')'      // Intersect
    | 'concat(' graph ',' graph ')'         // Concat
    | 'union(' graph ',' graph ')'          // Union
    | graph '*'                             // Star
    | '(' graph ')'

bool ->
      var
    | 'true' | 'false'
    | expr 'in' expr                       // Contains

set ->
      var
    | '{' (expr (','  expr)* )? '}'        // Set
    | graph '.' 'starts'
    | graph '.' 'finals'
    | graph '.' 'reachables'
    | graph '.' 'nodes'
    | graph '.' 'edges'
    | graph '.' 'labels'
    | 'map' '(' lambda ',' set ')'
    | 'filter' '(' lambda ',' set ')'
    | '(' set ')'

pattern ->
      var
    | '(' (pattern (','  pattern)* )? ')'
    | '_'

lambda -> '{' pattern '->' expr '}'

var -> [a-zA-Z_][a-zA-Z_0-9]*

val ->
    STR
  | INT
  | bool
  | REGEX
  | CFG

STR -> '"' [^"\n]* '"'
INT -> '-'? [1-9][0-9]*
REGEX -> 'r' STR
CFG -> 'c' STR
EOL -> [\n]+
```

## Примеры

```
g = load_graph("graph").set_starts({0 .. 10}) // Получение графа
res = map({(_, f) -> f}, g.reachables)        // Получение достижимых вершин данного множества
```

```
cfg = c"S -> a S b | a b";                    // Создание cfg
reg = r"a b"                                  // Создание regex
intersection = intersect(cfg, reg)            // Пересечение
res = map({((u, _), (v, _)) -> (u, v)}, intersection.reachables) // Вершины, между которыми существует путь, удовлетворяющий ограничению
print res                                     // Печать результата
```

```
g_1 = load_graph("graph1")                        // Загрузка графа
g_2 = load_graph("graph2")                        // Загрузка графа
cl = filter({l -> l in g_w.labels}, g_p.labels)   // Получение общих меток
print cl                                          // Печать результата
```
