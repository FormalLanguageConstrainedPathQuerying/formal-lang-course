grammar Gram;

prog : (statement ';')* ;

statement : bind | print ;

print : '$' NAME ;

bind : 'let' NAME '=' expr;

lambda : NAME '->' expr;

expr : '(' expr ')'
     | expr '~'
     | expr ':=' sa_state expr
     | expr '+=' sa_state expr
     | expr '??' get_state
     | lambda '->>' expr
     | lambda '?>>' expr
     | '#' PATH
     | '-' expr
     | expr '+' expr
     | expr '-' expr
     | expr '*' expr
     | expr '&' expr
     | expr '|' expr
     | expr '*'
     | expr '==' expr
     | expr '!=' expr
     | expr '<' expr
     | expr '>' expr
     | expr '<=' expr
     | expr '=>' expr
     | expr '&&' expr
     | expr '||' expr
     | '!' expr
     | expr '%' expr
     | expr '!%' expr
     | NAME
     | INT
     | STRING;


sa_state : 'start' | 'final' ;

get_state : sa_state | 'reachable' | 'nodes' | 'edges' | 'labels' ;

INT : [0-9]+ ;
PATH : 'P\'' (.)+? '\'' ;
NAME : LETTER [0-9A-Za-z]* ;
STRING : '\'' [0-9A-Za-z]+ '\'' ;
DIGIT : [0-9] ;
LETTER : [A-Za-z] ;

WS : [ \t\r\n]+ -> skip;