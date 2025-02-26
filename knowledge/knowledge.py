from abc import ABC , abstractmethod
from itertools import product

class Symbol:
    def __init__(self , name , discription , state):
        self.name = name
        self.state = state
        self.discription = discription

    def __str__(self):
        return self.name

class Operator(ABC):
    @abstractmethod
    def formula(self):
        pass
    def truth_value(self): 
        pass
    def get_symbols(self):
        pass

class And(Operator):
    def __init__(self , *statements):
        self.statements = statements

    def formula(self):
        result = [str(self.statements[0])]
        for i in range(len(self.statements)):
            if i != 0:
                result.append(f" ∧ {str(self.statements[i])}" if not isinstance(self.statements[i] , Operator) else f" ∧ ({str(self.statements[i])})")
        return "".join(result)

    def truth_value(self):
        for statement in self.statements:
            result = statement.state if not isinstance(statement , Operator) else statement.truth_value()
            
            if result == None:
                return None
            
            if not result:
                return False

        return True

    def get_symbols(self):
        symbols = set()
        for statement in self.statements:
            if isinstance(statement , Symbol):
                symbols.add(statement)
            else:
                symbols.update(statement.get_symbols())
        return symbols
        
    def __str__(self):
        return self.formula()

class Or(Operator):
    def __init__(self , *statements):
        self.statements = statements

    def formula(self):
        result = [str(self.statements[0])]
        for i in range(len(self.statements)):
            if i != 0:
                result.append(f" ∨ {str(self.statements[i])}" if not isinstance(self.statements[i] , Operator) else f" ∨ ({str(self.statements[i])})")
        return "".join(result)

    def truth_value(self):
        for statement in self.statements:
            result = statement.state if not isinstance(statement , Operator) else statement.truth_value()
            
            if result == None:
                return None
            
            if result:
                return True

        return False

    def get_symbols(self):
        symbols = set()
        for statement in self.statements:
            if isinstance(statement , Symbol):
                symbols.add(statement)
            else:
                symbols.update(statement.get_symbols())
        return symbols
        
    def __str__(self):
        return self.formula()

class Not(Operator):
    def __init__(self , statement):
        self.statement = statement

    def formula(self):
        return "¬"+str(self.statement) if not isinstance(self.statement , Operator) else "¬("+f"{self.statement})"

    def truth_value(self):
        if self.statement == None:
            return None
        return not self.statement.state if not isinstance(self.statement , Operator) else not self.statement.truth_value()

    def get_symbols(self):
        symbols = set()
        if isinstance(self.statement , Symbol):
            symbols.add(self.statement)
        else:
            symbols.update(self.statement.get_symbols())
        return symbols

    def __str__(self):
        return self.formula()

class Implicate(Operator):
    def __init__(self , statement1 , statement2):
        self.s_statement = statement1
        self.r_statement = statement2

    def formula(self):
        return str(self.s_statement if not isinstance(self.s_statement , Operator) else f"({self.s_statement})") + " => " + str(self.r_statement if not isinstance(self.r_statement , Operator) else f"({self.r_statement})")

    def truth_value(self):
        if self.s_statement == None or self.r_statement == None:
            return None
        return not (self.s_statement.state if not isinstance(self.s_statement , Operator) else self.s_statement.truth_value()) or (self.r_statement.state if not isinstance(self.r_statement , Operator) else self.r_statement.truth_value())

    def get_symbols(self):
        symbols = set()
        if isinstance(self.s_statement , Symbol):
            symbols.add(self.s_statement)
        else:
            symbols.update(self.s_statement.get_symbols())

        if isinstance(self.r_statement , Symbol):
            symbols.add(self.r_statement)
        else:
            symbols.update(self.r_statement.get_symbols())
        return symbols

    def __str__(self):
        return self.formula()

def check_knowlege(knowledge):
    symbols = list(knowledge.get_symbols())
    combinations = list(product([True , False] , repeat=len(symbols)))
    valid_worlds = []

    for comb in combinations:
        valid_comb = []
        for i in range(len(symbols)):
            symbols[i].state = comb[i]
            valid_comb.append([symbols[i] , comb[i]])
        
        if knowledge.truth_value():
            valid_worlds.append(valid_comb.copy())

    return valid_worlds
    
def check_query(knowledge , query):
    valid_worlds = check_knowlege(knowledge)
    if len(check_knowlege(knowledge)) > 0:
        for world in valid_worlds:
            for config in world:
                config[0].state = config[1]
            if not knowledge.truth_value():
                return False
        return query.state if isinstance(query , Symbol) else query.truth_value()
    else:
        raise Exception("The knowledge is not valid")

mustard = Symbol("mustard" , None , None)
plum = Symbol("plum" , None , None)
scarlet = Symbol("scarlet" , None , None)
ballroom = Symbol("ballroom" , None , None)
kitchen = Symbol("kitchen" , None , None)
library = Symbol("library" , None , None)
knife = Symbol("knife" , None , None)
revolver = Symbol("revolver" , None , None)
wrench = Symbol("wrench" , None , None)


kb = And(
    Or(mustard , plum , scarlet),
    Or(ballroom , kitchen , library),
    Or(knife , revolver , wrench),
    Not(mustard),
    Not(kitchen),
    Not(revolver),
    Or(Not(scarlet) , Not(library) , Not(wrench)),
    Not(plum),
    Not(ballroom),
)

valid_worlds = check_knowlege(kb)

suspects = {
    mustard : True,
    plum : True,
    scarlet : True,
    ballroom : True,
    library : True,
    kitchen : True,
    knife : True,
    revolver : True,
    wrench : True,
}

for world in valid_worlds:
    for sym in world:
        if sym[1]:
            suspects[sym[0]] = suspects[sym[0]] and True
        else:
            suspects[sym[0]] = suspects[sym[0]] and False


for key in suspects.keys():
    print(key.name , suspects[key])