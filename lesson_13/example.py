class A:
    def __init__(self, class_type):
        self.type = class_type

    # 1. метод публичен в родительском классе А и публичен в его потомке B    
    def get_type(self):
        return self.type

    # 4. метод скрыт в родительском классе А и скрыт в его потомке B
    def __inner_method_for_A(self):
        pass
    
    # 2. метод публичен в родительском классе А и скрыт в его потомке B
    def _outer_method_for_A_not_for_B(self):
        pass

class B(A):
    def __init__(self, class_type):
        super().__init__(class_type)
        pass
