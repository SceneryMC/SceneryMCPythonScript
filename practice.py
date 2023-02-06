class NewClass:
    static = list(range(10))

    def __init__(self, times):
        self.local = NewClass.static * times

    def __getitem__(self, item):
        return self.local[item]

    def __len__(self):
        return len(self.local)


new_class_1 = NewClass(1)
new_class_10 = NewClass(10)
new_class_0 = NewClass(0)
print(id(new_class_1.local), id(new_class_10.local), id(new_class_0.local))
print(id(new_class_1.static), id(new_class_10.static), id(new_class_0.static))

