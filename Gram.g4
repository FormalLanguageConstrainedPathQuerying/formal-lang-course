grammar Gram;

prog : (statement ';')* ;

statement : bind | print ;

print : '$' name ;

bind : 'let' name '=' expr;

lambda : name '->' expr;

expr : '(' expr ')'                 #brackets_expr
     | expr ':=' sa_state expr      #assign_state_expr
     | expr '+=' sa_state expr      #add_state_expr
     | expr '??' get_state          #get_state_expr
     | lambda '->>' expr            #map_expr
     | lambda '?>>' expr            #filter_expr
     | '#' PATH                     #load_expr
     | expr '++' expr               #concat_expr
     | expr '*' expr                #bistar_expr
     | expr '&' expr                #intersection_expr
     | expr '|' expr                #union_expr
     | expr '*'                     #unistar_expr
     | expr '==' expr               #equality_expr
     | expr '!=' expr               #unequality_expr
     | '<' str '>'                  #one_symbol_expr
     | name                         #name_expr
     | int                          #int_expr
     | STRING                       #string_expr
     ;

name : LETTER (LETTER | DIGIT)* ;

str: (LETTER | DIGIT)+ ;

int: DIGIT + ;

sa_state : 'start' | 'final' ;

get_state : sa_state | 'reachable' | 'nodes' | 'edges' | 'labels' ;

PATH : 'P\'' (.)+? '\'' ;
STRING : '\'' [a-zA-Z0-9] '\'' ;
DIGIT : [0-9] ;
LETTER : [A-Za-z] ;

WS : [ \t\r\n]+ -> skip;