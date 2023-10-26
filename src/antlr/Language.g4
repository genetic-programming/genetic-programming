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
	| conditional_statement
	| loop_statement
	| compound_statement
	;

line
    : expression
	| declaration
	| assignment
	| printStatement
	| readStatement
    ;


// STATEMENTS
conditional_statement
    : If expression compound_statement ( Else compound_statement )?
    ;

loop_statement
	: While expression compound_statement
	;

compound_statement
    : '{' (statements)? '}'
    ;


// EXPRESSIONS
expression
    :   boolean_unary_operator expression
    |   numeric_unary_operator expression
    |   expression multiplication_operator expression
    |   expression addition_operator expression
    |   expression comparison_operator expression
    |   expression and_operator expression
    |   expression or_operator expression
    |   '(' expression ')'
    |   atom
    ;

boolean_unary_operator
    : Not
    ;

numeric_unary_operator
    : '+'
    | '-'
    ;

multiplication_operator
    : '*'
    | '/'
    ;

addition_operator
    : '+'
    | '-'
    ;

comparison_operator
    : '<'
    | '>'
    | '=='
    | '!='
    ;

and_operator
    : And
    ;

or_operator
    : Or
    ;

atom
    : VARIABLE_NAME
    | literal
    ;


// VARIABLES AND TYPES
declaration
	: var_type VARIABLE_NAME
	;

var_type
    : Int
    | Float
    | Bool
    ;

assignment
    : declaration '=' expression
    | VARIABLE_NAME '=' expression
    ;

literal
    : BOOLEAN_VAL
    | FLOAT_VAL
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
Float: 'float';
Bool: 'bool';

Print: 'print';
Read: 'read';

BOOLEAN_VAL
    : 'true'
    | 'false'
    ;

FLOAT_VAL  // accepts: 10.11 and 10 and 10. and .01
    :  INT_VAL '.' [0-9]*
    | '0'? '.' [0-9]+
    ;

INT_VAL
    : '0'
    | [1-9][0-9]*
    ;

VARIABLE_NAME
    : [a-z_]+
    ;

