grammar Language;


// PRIMARY EXPRESSION
program
   : statements? EOF
   ;

statements
    : statement+
    ;

statement
	: line ';'
	| conditionalStatement
	| loopStatement
	| compoundStatement
	;

line
    : expression
	| declaration
	| assignment
	| printStatement
	| readStatement
    ;


// STATEMENTS
conditionalStatement
    : If expression compoundStatement ( Else compoundStatement )?
    ;

loopStatement
	: While expression compoundStatement
	;

compoundStatement
    : '{' (statements)? '}'
    ;


// EXPRESSIONS
expression
    :   booleanUnaryOperator expression
    |   numericUnaryOperator expression
    |   expression multiplicationOperator expression
    |   expression additionOperator expression
    |   expression comparisonOperator expression
    |   expression andOperator expression
    |   expression orOperator expression
    |   '(' expression ')'
    |   atom
    ;

booleanUnaryOperator
    : Not
    ;

numericUnaryOperator
    : '+'
    | '-'
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

atom
    : VARIABLE_NAME
    | literal
    ;


// VARIABLES AND TYPES
declaration
	: varType VARIABLE_NAME
	;

varType
    : Int
    | Bool
    ;

assignment
    : declaration '=' expression
    | VARIABLE_NAME '=' expression
    ;

literal
    : BOOLEAN_VAL
    | INT_VAL
    ;


// IO
printStatement
    : Print expression
    ;

readStatement
    : Read VARIABLE_NAME
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

Int: 'int';
Bool: 'bool';

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

VARIABLE_NAME
    : 'v' [0-9]*
    ;

