grammar QueryLanguage;

program: (statement NEWLINE*)+;

statement: VARNAME EQUALS expr | 'print' LPAR expr RPAR;

expr: 
    VARNAME
    | INT
    | STR
    | BOOL
    | REGEX
    | CFG
    | LPAR expr RPAR
    | expr DOT SET_START LPAR expr RPAR
    | expr DOT SET_FINAL LPAR expr RPAR
    | expr DOT ADD_START LPAR expr RPAR
    | expr DOT ADD_FINAL LPAR expr RPAR
    | expr DOT GET_START
    | expr DOT GET_FINAL
    | expr DOT GET_REACHABLE
    | expr DOT GET_VERTICES
    | expr DOT GET_EDGES
    | expr DOT GET_LABELS
    | expr IN expr
    | MAP LPAR lambda_def COMMA expr RPAR
    | FILTER LPAR lambda_def COMMA expr RPAR
    | LOAD_DOT LPAR STR RPAR
    | LOAD_GRAPH LPAR STR RPAR
    | expr DOT INTERSECT LPAR expr RPAR
    | expr DOT CONCAT LPAR expr RPAR
    | expr DOT UNION LPAR expr RPAR
    | expr CL_STAR
    | LCBR expr (COMMA expr)* RCBR 
    ;

pattern:
    WILD
    | VARNAME
    | LPAR (pattern (COMMA  pattern)* )? RPAR
    ;

lambda_def: LCBR pattern LAM_ARROW expr RCBR;

SET_START : 'set_start';
SET_FINAL : 'set_final';
ADD_START : 'add_start';
ADD_FINAL : 'add_final';
GET_START : 'get_start';
GET_FINAL : 'get_final';
GET_EDGES : 'get_edges';

BR : '"';
IN : 'in';
WILD : '_';
MAP : 'map';
CL_STAR : '*';
UNION : 'union';
FILTER : 'filter';
CONCAT : 'concat';
LOAD_DOT : 'load_dot';
INTERSECT : 'intersect';
LOAD_GRAPH : 'load_graph';
GET_LABELS : 'get_labels';
GET_VERTICES : 'get_verices';
GET_REACHABLE : 'get_reachable';

VARNAME : [a-zA-Z_][a-zA-Z0-9_]*;
BOOL : 'true' | 'false';
INT : ('-'? [1-9][0-9]*) | '0';
STR : BR .*? BR;
REGEX : 'r' STR;
CFG : 'c' STR;
COMMA: ',';
DOT : '.';

NEWLINE : [\r\n]+ ;

LAM_ARROW : '->';
EQUALS : '=';
LPAR : '(';
RPAR : ')';
LCBR : '{';
RCBR : '}';

