class Document:
    def __init__(self, type, owner):
        self.type = type
        self.owner = owner
    
    def signature(self):
        print(f'подписан документ типа {self.type}')

class Contract(Document):
    def __init__(self, type, owner, parties):
        super().__init__(type, owner)
        self.parties = parties
    
    # наследник расширяет базовый класс родителя -> расширение класса-родителя
    def stamp(self):
        print('согласовано - поставлена печать')

# приложеие к трудовому-договору
class Annex:
    def __init__(self, benefits):
        self.benefits = benefits

# условия труда
class WorkingConditions:
    def __init__(self, salary, working_hours, operating_mode):
        self.salary = salary
        self.working_hours = working_hours
        self.operating_mode = operating_mode

# расширение: трудовой договор дополнен методом, приложением к договору и рабочими условиями
# специализация: трудовой договор подтип контракта
class EmploymentContract(Contract):
    def __init__(self, type, owner, parties, conditions : WorkingConditions, annex : Annex):
        super().__init__(type, owner)
        self.parties = parties
        self.conditions = conditions
        self.annex = annex
    
    def stamp(self):
        print('согласовано - поставлена печать')