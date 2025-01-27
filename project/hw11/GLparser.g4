grammar GLparser;
prog: stmt*;

stmt
    : bind
    | add
    | remove
    | declare;

declare : LET var_p IS GRAPH;
bind : LET var_p EQ expr;
remove : REMOVE (VERTEX | EDGE | VERTICES) expr FROM var_p;

add : ADD (VERTEX | EDGE) expr TO var_p;
expr : num_p | char_p | var_p | edge_expr | set_expr | regexp | select;
set_expr : LBRACE expr (COMMA expr)* RBRACE;
edge_expr : LPAREN expr COMMA expr COMMA expr RPAREN;

regexp
    : char_p
    | var_p
    | LPAREN regexp RPAREN
    | regexp PATDENY range
    | regexp REGAND regexp
    | regexp WILDCARD regexp
    | regexp ALTERNATIVE regexp;

range : LBRACE num_p TWODOTS? num_p? RBRACE;
select : v_filter? v_filter? RETURN var_p (COMMA var_p)? WHERE var_p REACHABLE FROM var_p IN var_p BY expr;
v_filter : FOR var_p IN expr;
var_p : VAR;
char_p : CHAR;
num_p : NUM;
LET: 'let';
IS: 'is';
FROM: 'from';
TO: 'to';
IN: 'in';
BY: 'by';
RETURN: 'return';
FOR: 'for';
WHERE: 'where';
REACHABLE: 'reachable';
GRAPH: 'graph';
VERTEX: 'vertex';
VERTICES: 'vertices';
EDGE: 'edge';
ADD: 'add';
REMOVE: 'remove';
EQ: '=';
LPAREN: '(';
RPAREN: ')';
LBRACE: '[';
RBRACE: ']';
COMMA: ',';
REGAND: '&'; // intersect
ALTERNATIVE: '|';
WILDCARD: '.';
TWODOTS: '..';
PATDENY: '^';
VAR: [a-z][a-z0-9]*;
NUM: '0' | [1-9][0-9]*;
CHAR: '"'[a-z]'"';
WS : [ \t\r\n\f]+ -> skip ;
