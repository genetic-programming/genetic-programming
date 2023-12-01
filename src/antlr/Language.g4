grammar Language;


// PRIMARY EXPRESSION
statements
    : statement*
    ;

statement
	: line ';'
	| conditionalStatement
	| loopStatement
	| compoundStatement
	;

line
    : expression
	| assignment
	| printStatement
    ;

assignment
    : VARIABLE_NAME '=' expression
    ;


// STATEMENTS
conditionalStatement
    : If expression compoundStatement ( Else compoundStatement )?
    ;

loopStatement
	: While expression compoundStatement
	;

compoundStatement
    : '{' statements '}'
    ;

printStatement
    : Print expression
    ;


// EXPRESSIONS
expression
    : booleanUnaryOperator expression
    | numericUnaryOperator expression
    | expression multiplicationOperator expression
    | expression additionOperator expression
    | expression comparisonOperator expression
    | expression andOperator expression
    | expression orOperator expression
    | nestedExpression
    | VARIABLE_NAME
    | literal
    | Read
    ;

nestedExpression
    : '(' expression ')'
    ;

literal
    : BOOLEAN_VAL
    | INT_VAL
    | STRING_VAL
    ;

booleanUnaryOperator
    : Not
    ;

numericUnaryOperator
    : '-'
    ;

multiplicationOperator
    : '*'
    | '/'
    ;

additionOperator
    : '+'
    | '-'
    ;

comparisonOperator
    : '>'
    | '=='
    | '!='
    ;

andOperator
    : And
    ;

orOperator
    : Or
    ;


// KEYWORDS AND OTHER LEXER VARIABLES

SPACE: [ ] -> skip;
TAB: '\t' -> skip;
NEWLINE: [\r\n]+ -> skip;
LINECOMMENT: '//' ~[\r\n]* -> skip;
BLOCKCOMMENT: '/*' .*? '*/' -> skip;

If: 'if';
Else: 'else';
While: 'while';

Not: 'not';
And: 'and';
Or: 'or';

Print: 'print';
Read: 'read';

BOOLEAN_VAL
    : 'true'
    | 'false'
    ;

INT_VAL
    : '0'
    | [1-9][0-9]*
    ;

STRING_VAL
    : '"' .*? '"'
    ;

VARIABLE_NAME
    : 'v' INT_VAL
    ;
