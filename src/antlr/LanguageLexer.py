# Generated from /Users/spoton/Studia/pg/genetic-programming/src/antlr/Language.g4 by ANTLR 4.13.1
from antlr4 import *
from io import StringIO
import sys
from typing import TextIO


def serializedATN():
    return [
        4,0,34,235,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,
        13,7,13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,
        19,2,20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,
        26,7,26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,
        32,2,33,7,33,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,4,1,4,1,5,1,5,1,6,
        1,6,1,7,1,7,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,1,11,1,12,1,12,1,
        12,1,13,1,13,1,14,1,14,1,14,1,14,1,15,1,15,1,15,1,15,1,16,4,16,109,
        8,16,11,16,12,16,110,1,16,1,16,1,17,1,17,1,17,1,17,5,17,119,8,17,
        10,17,12,17,122,9,17,1,17,1,17,1,18,1,18,1,18,1,18,5,18,130,8,18,
        10,18,12,18,133,9,18,1,18,1,18,1,18,1,18,1,18,1,19,1,19,1,19,1,20,
        1,20,1,20,1,20,1,20,1,21,1,21,1,21,1,21,1,21,1,21,1,22,1,22,1,22,
        1,22,1,23,1,23,1,23,1,23,1,24,1,24,1,24,1,25,1,25,1,25,1,25,1,26,
        1,26,1,26,1,26,1,26,1,26,1,27,1,27,1,27,1,27,1,27,1,28,1,28,1,28,
        1,28,1,28,1,28,1,29,1,29,1,29,1,29,1,29,1,30,1,30,1,30,1,30,1,30,
        1,30,1,30,1,30,1,30,3,30,200,8,30,1,31,1,31,1,31,5,31,205,8,31,10,
        31,12,31,208,9,31,1,31,3,31,211,8,31,1,31,1,31,4,31,215,8,31,11,
        31,12,31,216,3,31,219,8,31,1,32,1,32,1,32,5,32,224,8,32,10,32,12,
        32,227,9,32,3,32,229,8,32,1,33,4,33,232,8,33,11,33,12,33,233,1,131,
        0,34,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,12,25,
        13,27,14,29,15,31,16,33,17,35,18,37,19,39,20,41,21,43,22,45,23,47,
        24,49,25,51,26,53,27,55,28,57,29,59,30,61,31,63,32,65,33,67,34,1,
        0,5,1,0,32,32,2,0,10,10,13,13,1,0,48,57,1,0,49,57,2,0,95,95,97,122,
        245,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,
        0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,
        0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,0,27,1,0,0,0,0,29,1,0,0,0,
        0,31,1,0,0,0,0,33,1,0,0,0,0,35,1,0,0,0,0,37,1,0,0,0,0,39,1,0,0,0,
        0,41,1,0,0,0,0,43,1,0,0,0,0,45,1,0,0,0,0,47,1,0,0,0,0,49,1,0,0,0,
        0,51,1,0,0,0,0,53,1,0,0,0,0,55,1,0,0,0,0,57,1,0,0,0,0,59,1,0,0,0,
        0,61,1,0,0,0,0,63,1,0,0,0,0,65,1,0,0,0,0,67,1,0,0,0,1,69,1,0,0,0,
        3,71,1,0,0,0,5,73,1,0,0,0,7,75,1,0,0,0,9,77,1,0,0,0,11,79,1,0,0,
        0,13,81,1,0,0,0,15,83,1,0,0,0,17,85,1,0,0,0,19,87,1,0,0,0,21,89,
        1,0,0,0,23,91,1,0,0,0,25,94,1,0,0,0,27,97,1,0,0,0,29,99,1,0,0,0,
        31,103,1,0,0,0,33,108,1,0,0,0,35,114,1,0,0,0,37,125,1,0,0,0,39,139,
        1,0,0,0,41,142,1,0,0,0,43,147,1,0,0,0,45,153,1,0,0,0,47,157,1,0,
        0,0,49,161,1,0,0,0,51,164,1,0,0,0,53,168,1,0,0,0,55,174,1,0,0,0,
        57,179,1,0,0,0,59,185,1,0,0,0,61,199,1,0,0,0,63,218,1,0,0,0,65,228,
        1,0,0,0,67,231,1,0,0,0,69,70,5,59,0,0,70,2,1,0,0,0,71,72,5,123,0,
        0,72,4,1,0,0,0,73,74,5,125,0,0,74,6,1,0,0,0,75,76,5,40,0,0,76,8,
        1,0,0,0,77,78,5,41,0,0,78,10,1,0,0,0,79,80,5,43,0,0,80,12,1,0,0,
        0,81,82,5,45,0,0,82,14,1,0,0,0,83,84,5,42,0,0,84,16,1,0,0,0,85,86,
        5,47,0,0,86,18,1,0,0,0,87,88,5,60,0,0,88,20,1,0,0,0,89,90,5,62,0,
        0,90,22,1,0,0,0,91,92,5,61,0,0,92,93,5,61,0,0,93,24,1,0,0,0,94,95,
        5,33,0,0,95,96,5,61,0,0,96,26,1,0,0,0,97,98,5,61,0,0,98,28,1,0,0,
        0,99,100,7,0,0,0,100,101,1,0,0,0,101,102,6,14,0,0,102,30,1,0,0,0,
        103,104,5,9,0,0,104,105,1,0,0,0,105,106,6,15,0,0,106,32,1,0,0,0,
        107,109,7,1,0,0,108,107,1,0,0,0,109,110,1,0,0,0,110,108,1,0,0,0,
        110,111,1,0,0,0,111,112,1,0,0,0,112,113,6,16,0,0,113,34,1,0,0,0,
        114,115,5,47,0,0,115,116,5,47,0,0,116,120,1,0,0,0,117,119,8,1,0,
        0,118,117,1,0,0,0,119,122,1,0,0,0,120,118,1,0,0,0,120,121,1,0,0,
        0,121,123,1,0,0,0,122,120,1,0,0,0,123,124,6,17,0,0,124,36,1,0,0,
        0,125,126,5,47,0,0,126,127,5,42,0,0,127,131,1,0,0,0,128,130,9,0,
        0,0,129,128,1,0,0,0,130,133,1,0,0,0,131,132,1,0,0,0,131,129,1,0,
        0,0,132,134,1,0,0,0,133,131,1,0,0,0,134,135,5,42,0,0,135,136,5,47,
        0,0,136,137,1,0,0,0,137,138,6,18,0,0,138,38,1,0,0,0,139,140,5,105,
        0,0,140,141,5,102,0,0,141,40,1,0,0,0,142,143,5,101,0,0,143,144,5,
        108,0,0,144,145,5,115,0,0,145,146,5,101,0,0,146,42,1,0,0,0,147,148,
        5,119,0,0,148,149,5,104,0,0,149,150,5,105,0,0,150,151,5,108,0,0,
        151,152,5,101,0,0,152,44,1,0,0,0,153,154,5,110,0,0,154,155,5,111,
        0,0,155,156,5,116,0,0,156,46,1,0,0,0,157,158,5,97,0,0,158,159,5,
        110,0,0,159,160,5,100,0,0,160,48,1,0,0,0,161,162,5,111,0,0,162,163,
        5,114,0,0,163,50,1,0,0,0,164,165,5,105,0,0,165,166,5,110,0,0,166,
        167,5,116,0,0,167,52,1,0,0,0,168,169,5,102,0,0,169,170,5,108,0,0,
        170,171,5,111,0,0,171,172,5,97,0,0,172,173,5,116,0,0,173,54,1,0,
        0,0,174,175,5,98,0,0,175,176,5,111,0,0,176,177,5,111,0,0,177,178,
        5,108,0,0,178,56,1,0,0,0,179,180,5,112,0,0,180,181,5,114,0,0,181,
        182,5,105,0,0,182,183,5,110,0,0,183,184,5,116,0,0,184,58,1,0,0,0,
        185,186,5,114,0,0,186,187,5,101,0,0,187,188,5,97,0,0,188,189,5,100,
        0,0,189,60,1,0,0,0,190,191,5,116,0,0,191,192,5,114,0,0,192,193,5,
        117,0,0,193,200,5,101,0,0,194,195,5,102,0,0,195,196,5,97,0,0,196,
        197,5,108,0,0,197,198,5,115,0,0,198,200,5,101,0,0,199,190,1,0,0,
        0,199,194,1,0,0,0,200,62,1,0,0,0,201,202,3,65,32,0,202,206,5,46,
        0,0,203,205,7,2,0,0,204,203,1,0,0,0,205,208,1,0,0,0,206,204,1,0,
        0,0,206,207,1,0,0,0,207,219,1,0,0,0,208,206,1,0,0,0,209,211,5,48,
        0,0,210,209,1,0,0,0,210,211,1,0,0,0,211,212,1,0,0,0,212,214,5,46,
        0,0,213,215,7,2,0,0,214,213,1,0,0,0,215,216,1,0,0,0,216,214,1,0,
        0,0,216,217,1,0,0,0,217,219,1,0,0,0,218,201,1,0,0,0,218,210,1,0,
        0,0,219,64,1,0,0,0,220,229,5,48,0,0,221,225,7,3,0,0,222,224,7,2,
        0,0,223,222,1,0,0,0,224,227,1,0,0,0,225,223,1,0,0,0,225,226,1,0,
        0,0,226,229,1,0,0,0,227,225,1,0,0,0,228,220,1,0,0,0,228,221,1,0,
        0,0,229,66,1,0,0,0,230,232,7,4,0,0,231,230,1,0,0,0,232,233,1,0,0,
        0,233,231,1,0,0,0,233,234,1,0,0,0,234,68,1,0,0,0,12,0,110,120,131,
        199,206,210,216,218,225,228,233,1,6,0,0
    ]

class LanguageLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    SPACE = 15
    TAB = 16
    NEWLINE = 17
    LINECOMMENT = 18
    BLOCKCOMMENT = 19
    If = 20
    Else = 21
    While = 22
    Not = 23
    And = 24
    Or = 25
    Int = 26
    Float = 27
    Bool = 28
    Print = 29
    Read = 30
    BOOLEAN_VAL = 31
    FLOAT_VAL = 32
    INT_VAL = 33
    VARIABLE_NAME = 34

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "'{'", "'}'", "'('", "')'", "'+'", "'-'", "'*'", "'/'", 
            "'<'", "'>'", "'=='", "'!='", "'='", "'\\t'", "'if'", "'else'", 
            "'while'", "'not'", "'and'", "'or'", "'int'", "'float'", "'bool'", 
            "'print'", "'read'" ]

    symbolicNames = [ "<INVALID>",
            "SPACE", "TAB", "NEWLINE", "LINECOMMENT", "BLOCKCOMMENT", "If", 
            "Else", "While", "Not", "And", "Or", "Int", "Float", "Bool", 
            "Print", "Read", "BOOLEAN_VAL", "FLOAT_VAL", "INT_VAL", "VARIABLE_NAME" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "SPACE", "TAB", "NEWLINE", "LINECOMMENT", "BLOCKCOMMENT", 
                  "If", "Else", "While", "Not", "And", "Or", "Int", "Float", 
                  "Bool", "Print", "Read", "BOOLEAN_VAL", "FLOAT_VAL", "INT_VAL", 
                  "VARIABLE_NAME" ]

    grammarFileName = "Language.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


