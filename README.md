Example use of the function :
sat('sat instance', x)
here 'sat instance' is a list of lists coded ( CNF formula ) satisfiability instance; the clauses are lists and literals (variables) are numbers with their negation represented as negative number (i.e. e.x., not '2' is '-2')
    example : 'sat instance' = [[1, -2, 3],[3,4],[2,-3,4,1,5],[5,3,1],[6,-1]]
x is optional argument set it 1 if the input length is high for optimal fast solving.
