grammar Test;

prog: stmt* EOF;

stmt: declare
    | bind
    | add
    | remove
    ;

declare: 'let' VAR 'is' 'graph' ;

bind: 'let' VAR '=' expr ;

remove: 'remove' ('vertex' | 'edge' | 'vertices') expr 'from' VAR ;

add: 'add' ('vertex' | 'edge') expr 'to' VAR ;

expr: NUM
    | CHAR
    | VAR
    | edge_expr
    | set_expr
    | regexp
    | select
    ;

set_expr: '[' expr (',' expr)* ']' ;

edge_expr: '(' expr ',' expr ',' expr ')' ;

regexp: CHAR
      | VAR
      | '(' regexp ')'
      | regexp '|' regexp
      | regexp '^' range
      | regexp '.' regexp
      | regexp '&' regexp
      ;

range: '[' NUM '..' NUM? ']' ;

select: v_filter? v_filter? 'return' VAR (',' VAR)? 'where' VAR 'reachable' 'from' VAR 'in' VAR 'by' expr ;

v_filter: 'for' VAR 'in' expr ;

WS: [ \r\n\t]+ -> skip;

VAR: [a-z] [a-z_"0-9]*;
NUM: '0' | ([1-9][0-9]*);
CHAR: '\u0022' [a-z] '\u0022';
