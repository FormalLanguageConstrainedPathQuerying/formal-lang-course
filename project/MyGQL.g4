grammar MyGQL;

// SYNTAX

prog : ( stmt ';' )* EOF ;

stmt : bind | print ;
bind : 'let' var '=' expr ;
print : 'print' expr ;

val : valBool | valInt | valString | set;
var : ID ;
set : '{' '}'                       # emptySet  // пустое множество
     | '{' expr (',' expr )* '}'    # setElem   // множество из элементов
     | '{' valInt '...' valInt '}'  # setIntRange  // range of INTs [a, b)
     ;

expr : '(' expr ')'             #exprParentheses  // скобки указывают приоритет операций
  | var                         #exprVar // переменные
  | val                         #exprVal // константы
  | 'set_start' expr 'to' expr  #exprSetStart // задать множество стартовых состояний
  | 'set_final' expr 'to' expr  #exprSetFinal  // задать множество финальных состояний
  | 'add_start' expr 'to' expr  #exprAddStart  // добавить состояния в множество стартовых
  | 'add_final' expr 'to' expr  #exprAddFinal  // добавить состояния в множество финальных
  | 'get_start' expr            #exprGetStart // получить множество стартовых состояний
  | 'get_final' expr            #exprGetFinal // получить множество финальных состояний
  | 'get_reachable' expr        #exprGetReachable // получить все пары достижимых вершин
  | 'get_vertices' expr         #exprGetVertices // получить все вершины
  | 'get_edges' expr            #exprGetEdges // получить все рёбра
  | 'get_labels' expr           #exprGetLabels // получить все метки
  | 'map' lambda 'of' expr      #exprMap  // классический map
  | 'filter' lambda 'of' expr   #exprFilter  // классический filter
  | 'load' valString            #exprLoad   // загрузка графа
  | expr '&' expr               #exprIntersect // пересечение языков, множеств
  | expr '|' expr               #exprConcat // конкатенация языков
  | expr '+' expr               #exprUnion // объединение языков, множеств
  | '*' expr                    #exprKlini // замыкание языков (звезда Клини)
  | expr '>>' expr              #exprShift // единичный переход  symb >> lang
  | expr 'in' expr              #exprInChecking // проверка наличия в множестве
  ;

valInt : INT;
valBool : BOOL;
valString : STRING;

lambda : args '->' '{' expr '}' ;
args : var                      #argsSingle
     | '(' args (',' args)* ')' #argsGroup
     ;

// LEXIS

BOOL : 'true' | 'false' ;
INT : [0-9]+ ;

ID : NameStartChar | NameStartChar NameChar* ;

NameChar : NameStartChar
   | '0'..'9'
   | '_'
   ;

NameStartChar : 'A'..'Z' | 'a'..'z' ;

STRING : '"' ( '\\"' | . )*? '"' ;

COMMENT : '/*' .*? '*/' -> skip ;
WS : [ \r\t\n]+ -> skip ;
