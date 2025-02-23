from abc import ABC , abstractmethod

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
        result = self.statements[0].state if not isinstance(self.statements[0] , Operator) else self.statements[0].truth_value()
        if result == None:
            return None
        for i in range(len(self.statements)):
            result = result and self.statements[i].state if not isinstance(self.statements[i] , Operator) else self.statements[i].truth_value()
        return result
        
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
        result = self.statements[0].state if not isinstance(self.statements[0] , Operator) else self.statements[0].truth_value()
        if result == None:
            return None
        for i in range(len(self.statements)):
            result = result or self.statements[i].state if not isinstance(self.statements[i] , Operator) else self.statements[i].truth_value()
        return result
        
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
        
    def __str__(self):
        return self.formula()




rain = Symbol("rain" , None , True)
outside = Symbol("ouside" , None , True)
die = Symbol("die" , None , True)
run = Symbol("run" , None , False)
cook = Symbol("cook" , None , True)


kb = And(
    Implicate(And(outside , rain) , die),
    Implicate(cook , Not(run)),
    Or(outside , run),
    Not(And(outside , run)),
    rain,
    cook,
)


print(kb.truth_value())