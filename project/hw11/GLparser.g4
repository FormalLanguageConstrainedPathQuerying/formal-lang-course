grammar GLparser;
prog: EOL* (stmt EOL*)* EOF;

stmt
    : bind
    | add
    | remove
    | declare;

declare : LET VAR IS GRAPH;
bind : LET VAR EQ expr;
remove : REMOVE (VERTEX | EDGE | VERTICES) expr FROM VAR;
add : ADD (VERTEX | EDGE) expr TO VAR;
expr : NUM | CHAR | VAR | edge_expr | set_expr | regexp | select;
set_expr : LBRACE expr (COMMA expr)* RBRACE;
edge_expr : LPAREN expr COMMA expr COMMA expr RPAREN;

regexp
    : CHAR
    | VAR
    | LPAREN regexp RPAREN
    | regexp ALTERNATIVE regexp
    | regexp PATDENY range
    | regexp WILDCARD regexp
    | regexp REGAND regexp;

range : LBRACE NUM TWODOTS NUM? RBRACE;
select : v_filter? v_filter? RETURN VAR (COMMA VAR)? WHERE VAR REACHABLE FROM VAR IN VAR BY expr;
v_filter : FOR VAR IN expr;

LET: 'let' ;
IS: 'is' ;
GRAPH: 'graph' ;
REMOVE: 'remove' ;
VERTEX: 'vertex' ;
EDGE: 'edge' ;
VERTICES: 'vertices' ;
FROM: 'from' ;
ADD: 'add' ;
TO: 'to' ;
REACHABLE : 'reachable' ;
RETURN : 'return' ;
FOR : 'for' ;
WHERE: 'where' ;
IN: 'in' ;
BY: 'by' ;

AND : 'and' ;
OR : 'or' ;
NOT : 'not' ;
EQ : '=' ;
COMMA : ',' ;
SEMI : ';' ;
LPAREN : '(' ;
RPAREN : ')' ;
LCURLY : '{' ;
RCURLY : '}' ;
LBRACE : '[' ;
RBRACE : ']' ;
ALTERNATIVE : '|' ;
TWODOTS : '..' ;
REGAND : '&' ;
PATDENY : '^';
WILDCARD : '.' ;
COLON: ':' ;



VAR : [a-z][a-z0-9]* ;
NUM : '0' | ([1-9][0-9]*) ;
CHAR : '"' [a-z] '"' ;
EOL: '\n';
WS: [ \t\r] -> skip;
