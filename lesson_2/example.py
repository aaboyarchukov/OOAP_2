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

class TaxBill(Document):
    def __init__(self, type, owner, departament):
        super().__init__(type, owner)
        self.departament = departament
    
    # наследник переопределяет родительский метод подписи, специализируя класс
    # -> специализация класса-родителя
    def signature(self):
        print('подписано электронной подписью')