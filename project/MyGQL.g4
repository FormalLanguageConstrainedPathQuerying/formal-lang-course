grammar MyGQL;

// SYNTAX

prog : ( stmt ';' )* EOF ;

stmt : bind | print ;
bind : 'let' ID '=' expr ;
print : 'print' expr ;

val : BOOL | INT | STRING | set;
var : ID ;
set : '{' '}'                    // множество
     | '{' expr (',' expr )* '}'
     | '{' INT '...' INT '}'      // range of INTs [a, b)
     ;

expr : '(' expr ')'               // скобки указывают приоритет операций
  | var                         // переменные
  | val                         // константы
  | 'set_start' expr  expr      // задать множество стартовых состояний
  | 'set_final' expr 'to' expr    // задать множество финальных состояний
  | 'add_start' expr 'to' expr    // добавить состояния в множество стартовых
  | 'add_final' expr 'to' expr    // добавить состояния в множество финальных
  | 'get_start' expr            // получить множество стартовых состояний
  | 'get_final' expr            // получить множество финальных состояний
  | 'get_reachable' expr        // получить все пары достижимых вершин
  | 'get_vertices' expr         // получить все вершины
  | 'get_edges' expr            // получить все рёбра
  | 'get_labels' expr           // получить все метки
  | 'map' lambda 'of' expr        // классический map
  | 'filter' lambda 'of' expr     // классический filter
  | 'load' STRING               // загрузка графа
  | expr '&' expr               // пересечение языков, множеств
  | expr '|' expr               // конкатенация языков
  | expr '+' expr               // объединение языков, множеств
  | '*' expr                    // замыкание языков (звезда Клини)
  | expr '>>' expr              // единичный переход  symb >> lang
  | expr 'in' expr              // проверка наличия в множестве
  ;

lambda : args '->' '{' expr '}' ;
args : var
     | '(' args (',' args)* ')';

// LEXIS

BOOL : 'true' | 'false' ;
INT : [0-9]+ ;

//LET : 'let';
//PRINT : 'print';
//TO : 'to';
//OF : 'of';

//LP : '(';
//RP : ')';
//LBRC : '{';
//RBRC : '}';
//COMMA : ',';


ID : NameStartChar | NameStartChar NameChar* ;

NameChar : NameStartChar
   | '0'..'9'
   | '_'
   ;

NameStartChar : 'A'..'Z' | 'a'..'z' ;

STRING : '"' ( '\\"' | . )*? '"' ;

COMMENT : '/*' .*? '*/' -> skip ;
WS : [ \r\t\n]+ -> skip ;
