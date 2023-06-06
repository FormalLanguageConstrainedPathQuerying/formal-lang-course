# Описание языка

Описание синтаксиса
```ebnf
program = (statement ";")* EOF

statement = bind | print

print = "$" expr

bind = "~" NAME = expr

lambda = NAME '->' expr

expr = "(" expr ")"
     | expr "~" 
     | expr ":=" sa_state expr
     | expr "+=" sa_state expr
     | expr "??" get_state 
     | lambda "->>" expr
     | lambda "?>>" expr
     | "#" PATH
     | "-" expr
     | expr "+" expr
     | expr "-" expr
     | expr "*" expr
     | expr "&" expr
     | expr "|" expr
     | expr "*"
     | expr "==" expr
     | expr "!=" expr
     | expr "<" expr
     | expr ">" expr
     | expr "<=" expr
     | expr "=>" expr
     | expr "&&" expr
     | expr "||" expr
     | "!" expr
     | expr "%" expr
     | expr "!%" expr
     | NAME
     | INT
     | STRING
     
sa_state = "start" | "final"

get_state = "start" | "final" | "reachable" | "nodes" | "edges" | "labels"

lit = STRING | INT
```