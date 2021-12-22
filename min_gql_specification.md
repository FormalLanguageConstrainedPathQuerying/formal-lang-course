### Абстрактный синтаксис
```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Graph of graph
  | Labels of labels
  | Vertices of vertices
  | Edges of edges

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

lambda = Lambda of variables * expr
```
### Конкретный синтаксис
```
prog -> (stmt ; [EOL])+
stmt -> 'print' '(' expr ')'
      | var = expr
expr -> ( expr )
      | lambda
      | mapping
      | filtering
      | var
      | val
      | 'not' expr
      | expr 'in' expr
      | expr '&' expr
      | expr '.' expr
      | expr '|' expr
      | expr '*'

graph -> load_graph
       | string
       | set_start
       | set_final
       | add_start
       | add_final
       | ( graph )

load_graph -> 'load_graph' '(' path ')'
set_start -> 'set_start' '(' (graph | var) ',' (vertices | var) ')'
set_final -> 'set_final' '(' (graph | var) ',' (vertices | var) ')'
add_start -> 'add_start' '(' (graph | var) ',' (vertices | var) ')'
add_final -> 'add_start' '(' (graph | var) ',' (vertices | var) ')'

vertices -> vertex
          | range
          | vertices_set
          | select_reachable
          | select_final
          | select_start
          | select_vertices
          | '(' vertices ')'

range -> '{' INT '..' INT '}'

vertex -> INT
        | var

edges -> edge
       | edges_set
       | select_edges

edge -> '(' vertex ',' label ',' vertex ')'
      | '(' vertex ',' vertex ')'
      | var

labels -> label
        | labels_set
        | select_labels

label -> STRING

lambda -> 'fun' variables ':' expr
        | 'fun' ':' expr
        | '(' lambda ')'
mapping -> 'map' lambda expr
filtering -> 'filter' lambda expr

variables -> var [',' var]*

get_edges -> 'get_edges' '(' (graph | var) ')'
get_labels -> 'get_labels' '(' (graph | var) ')'
get_reachable -> 'get_reachable' '(' (graph | var) ')'
get_final -> 'get_final' '(' (graph | var) ')'
get_start -> 'get_start' '(' (graph | var) ')'
get_vertices -> 'get_vertices' '(' (graph | var) ')'

path -> STRING

vertices_set -> SET<vertex>
labels_set -> SET<label>
edges_set -> SET<edge>

var -> IDENT

val -> boolean
     | graph
     | edges
     | labels
     | vertices

boolean -> 'true'
         | 'false'

SET<X> -> '{' X [, X]* '}'
        | '{' '}'

NONZERO -> [1-9]
DIGIT -> [0-9]

INT -> NONZERO DIGIT*
CHAR -> [a-z] | [A-Z]
STRING -> '"' (CHAR | DIGIT | '_' | ' ')* '"'

INITIAL_LETTER -> '_' | CHAR
LETTER -> '_' | CHAR | DIGIT
IDENT -> INITIAL_LETTER LETTER*

WS -> [' '\t\r]+
EOL -> [\n]+
```
### Пример 1
```
g = load_graph("wine");
new_g = set_start(g, {1..100});
g_labels = get_labels(new_g);
common_labels = g_labels & (load_graph("pizza"));

print(common_labels);
```
### Пример 2
```
tmp = load_graph("sample");
g = set_start(set_final(tmp, get_vertices(tmp)), {1..100});
l1 = "l1" or "l2";
q1 = ("l3" | l1)*;
q2 = "l1" . "l5";
inter = g & q1;
start = get_start(g);
result = filter (fun v: v in start) (map (fun ((u_g,u_q1),l,(v_g,v_q1)): u_g) (get_edges(inter)));
print(result)
```
