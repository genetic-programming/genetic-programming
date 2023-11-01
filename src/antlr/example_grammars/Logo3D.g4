grammar Logo3D;

prog
   : (line? EOL) * line? EOF
   ;

line
   : cmd + comment?
   | comment
   | procedureDeclaration
   ;

block
   : EOL? '{' ((blockLine? EOL) + blockLine? | blockLine EOL? )  '}'
   ;

blockLine
   : cmd + comment?
   | returnStatement comment?
   | comment
   ;

cmd
   : move
   | moveTo
   | rotateX
   | rotateY
   | rotateZ
   | color
   | sleep
   | procedureInvocation
   | variableDefinition
   | variableDeclaration
   | repeat
   | while
   | ife
   | print
   ;

procedureInvocation
   : procedureName '(' parameterInvocation ')'
   ;

parameterInvocation
   : value (',' parameterInvocation)*
   ;

procedureDeclaration
   : procedureType 'function' procedureName '(' parameterDeclarations ')' block
   ;

parameterDeclarations
   : type name (',' parameterDeclarations)*
   ;

returnStatement
   : 'return' value 
   ;

procedureName
   : name
   ;

repeat
   : 'repeat' expression block
   ;

while
   : 'while' logicalExpression block
   ;

ife
   : 'if' logicalExpression block
   ;

print
   : 'print' (value | quotedString)
   ;

quotedString
   : '"' (~ '"')* '"'
   ;

variableDeclaration
   : type variableDefinition
   ;

variableDefinition
   : name '=' value
   ;

variable
   : name
   ;

parent
   : 'parent' '[' name ']' 
   ;

node_name
   : STRING
   ;

procedureType
   : INTTYPE
   | BOOLTYPE
   | FLOATTYPE
   | VOIDTYPE
   ;

type
   : INTTYPE
   | BOOLTYPE
   | FLOATTYPE
   ;

value
   : variable
   | expression
   | logicalExpression
   ;

comparison
   : expression comparisonOperator expression
   ;

comparisonOperator
   : '>='
   | '<='
   | '=='
   | '!='
   | '<'
   | '>'
   ;

numericAtomValue
   : procedureInvocation
   | parent
   | variable
   | number
   ;

factor
   : '(' expression ')'
   | ('+' | '-')? numericAtomValue
   ;

term
   : factor (('*' | '/') factor)*
   ;

expression
   : term (('+' | '-') term)*
   ;

logicalAtomValue
   : procedureInvocation
   | parent
   | variable
   | atom
   | comparison
   ;

logicalFactor
   : ('not' | '~')? '(' logicalExpression ')'
   | ('not' | '~')? logicalAtomValue
   ;

logicalComparison
   :  logicalFactor (('==' | '!=') logicalFactor)* 
   ;

logicalTerm
   :  logicalComparison (('and' | '&&') logicalComparison)*
   ;

logicalExpression
   :  logicalTerm (('or' | '||') logicalTerm)*
   ;

move
   : 'move' expression
   ;

moveTo
   : ('moveTo' | 'moveto') expression expression expression
   ;

rotateX
   : ('rotateX' | 'rotatex') expression
   ;

rotateY
   : ('rotateY' | 'rotatey') expression
   ;

rotateZ
   : ('rotateZ' | 'rotatez') expression
   ;

color
   : 'color' expression expression expression
   ;

sleep
   : 'sleep' expression
   ;

number
   : NUMBERINT
   | NUMBERFLOAT
   ;

atom
   : TRUE
   | FALSE
   ;

comment
   : COMMENT
   ;

INTTYPE
   : 'int'
   ;

BOOLTYPE
   : 'bool'
   ;

FLOATTYPE
   : 'float'
   ;

VOIDTYPE
   : 'viod'
   ;

TRUE
   : 'true'
   ;

FALSE
   : 'false'
   ;

STRING
   : [a-zA-Z] [a-zA-Z0-9_]*
   ;

NUMBERINT
   : [0-9]+
   ;

NUMBERFLOAT
   : [0-9]+ '.' [0-9]*
   ;

COMMENT
   : '//' ~ [\r\n]*
   ;

EOL
   : '\r'? '\n'
   ;

WS
   : [ \t\r\n]-> channel(HIDDEN)
   ;