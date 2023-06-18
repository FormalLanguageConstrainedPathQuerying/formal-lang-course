grammar Gram;

prog : (statement ';')* ;

statement : bind | print | assign ;

print : '$' expr ;

bind : 'let' name '=' expr;

assign : name '=' expr;

lambda : name '->' CODE;

expr : '(' expr ')'                 #bracket
     | expr ':=' sa_state expr      #set
     | expr '+=' sa_state expr      #add
     | expr '??' get_state          #get
     | lambda '-->' expr            #map
     | lambda '?->' expr            #filter
     | '#' PATH                     #load
     | expr '++' expr               #concat
     | expr '&' expr                #intersect
     | expr '|' expr                #union
     | expr '*'                     #kleene
     | expr '==' expr               #equals
     | expr '!=' expr               #unequals
     | '<' str '>'                  #construct
     | name                         #nameAssign
     | int                          #intAssign
     | STRING                       #stringAssign
     | '[]'                         #emptyList
     | '[' expr (',' expr)* ']'     #list
     | ']' '['                      #emptySet
     | ']' expr (',' expr)* '['     #bigSet
     ;

name : LETTER (LETTER | DIGIT)* ;

str: (LETTER | DIGIT)+ ;

int: DIGIT + ;

sa_state : 'start' | 'final' ;

get_state : sa_state | 'reachable' | 'nodes' | 'edges' | 'labels' ;

CODE : '{' .*? '}' ;
PATH : 'P\'' (.)+? '\'' ;
STRING : '\'' [a-zA-Z0-9] '\'' ;
DIGIT : [0-9] ;
LETTER : [A-Za-z] ;

WS : [ \t\r\n]+ -> skip;