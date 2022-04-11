from django.test import TestCase


# Create your tests here.


class Base:
    query_set = None

    def get_queryset(self):
        queryset = self.query_set
        return queryset


class A(Base):
    query_set = 1111

    def get(self):
        aa = self.get_queryset()
        print("aaa:", aa)


if __name__ == '__main__':
    a = A()
    a.query_set = 22
    a.get()
