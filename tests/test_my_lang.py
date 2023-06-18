from project.my_lang.main import *
import unittest


class MyTestCase(unittest.TestCase):

    def assertNotRaises(self, f, p):
        try:
            f(p)
        except:
            self.assertTrue(False)

    def test_bind(self):
        self.assertRaises(BindEx, execute_code, 'let a = 1; let a = 2;')
        self.assertNotRaises(execute_code, 'let a = 1; let b = 2;')

    def test_assign(self):
        self.assertRaises(AssignEx, execute_code, 'a = 1;')
        self.assertNotRaises(execute_code, 'let a = 1; let b = 2;')

    def test_print(self):
        self.assertNotRaises(execute_code, 'let a = 1; # a;')
        self.assertNotRaises(execute_code, '$ 1;')
        self.assertNotRaises(execute_code, '$ ([1, 2] ++ [3, 4]);')

    def test_union(self):
        self.assertRaises(UnionEx, execute_code, 'let a = 1 | [1, 2, 3]')
        self.assertNotRaises(execute_code, 'let a = [1, 2] | [1, 2, 3]')
        self.assertNotRaises(execute_code, 'let a = ]1, 2[ | ]1, 2, 3[')
        self.assertNotRaises(execute_code, 'let a = <abcd> | <efg>')
        self.assertRaises(UnionEx, execute_code, 'let a = ]1, 2[ | [1, 2, 3]')

    def test_intersect(self):
        self.assertRaises(IntersectEx, execute_code, 'let a = 1 & [1, 2, 3]')
        self.assertNotRaises(execute_code, 'let a = [1, 2] & [1, 2, 3]')
        self.assertNotRaises(execute_code, 'let a = ]1, 2[ & ]1, 2, 3[')
        self.assertNotRaises(execute_code, 'let a = <abcd> & <efg>')
        self.assertRaises(IntersectEx, execute_code, 'let a = ]1, 2[ & [1, 2, 3]')

    def test_concat(self):
        self.assertRaises(ConcatEx, execute_code, 'let a = 1 ++ [1, 2, 3]')
        self.assertNotRaises(execute_code, 'let a = [1, 2] ++ [1, 2, 3]')
        self.assertNotRaises(execute_code, 'let a = ]1, 2[ ++ ]1, 2, 3[')
        self.assertNotRaises(execute_code, 'let a = <abcd> ++ <efg>')
        self.assertRaises(ConcatEx, execute_code, 'let a = ]1, 2[ ++ [1, 2, 3]')

    def test_filter(self):
        self.assertRaises(IterableEx, execute_code, 'let a = x -> {x < 2} ?-> 1;')
        self.assertNotRaises(execute_code, 'let a = x -> {x < 2} ?-> [1, 2];')

    def test_map(self):
        self.assertRaises(IterableEx, execute_code, 'let a = x -> {x ** 2} --> 1;')
        self.assertNotRaises(execute_code, 'let a = x -> {x ** 2} --> [1, 2];')

    def test_launch(self):
        self.assertRaises(Exception, do, 'project/my_lang/my_code1.txt')
        self.assertNotRaises(do, 'project/my_lang/my_code.txt')

    def test_load(self):
        self.assertNotRaises(execute_code, 'let a = # P\'bzip\'')
        self.assertRaises(Exception, execute_code, 'let a = # P\'bzik\'')

    def test_construct(self):
        self.assertNotRaises(execute_code, 'let a = <lol>;')

    def test_int_assign(self):
        self.assertNotRaises(execute_code, 'let a = 1;')

    def test_add(self):
        self.assertNotRaises(execute_code, 'let a = <a>; let b = a += start [0];')
        self.assertRaises(IterableEx, execute_code, 'let a = <a>; let b = a += start 1;')
        self.assertRaises(MyEx, execute_code, 'let a = 1; let b = a += start [0];')

    def test_set(self):
        self.assertNotRaises(execute_code, 'let a = <a>; let b = a := final [0];')
        self.assertRaises(IterableEx, execute_code, 'let a = <a>; let b = a := final 1;')
        self.assertRaises(MyEx, execute_code, 'let a = 1; let b = a += final [0];')

    def test_get(self):
        self.assertNotRaises(execute_code, 'let a = <a>; let b = a ?? reachable;')
        self.assertRaises(MyEx, execute_code, 'let a = 1; let b = a ?? reachable [0];')

    def test_string_assign(self):
        self.assertNotRaises(execute_code, 'let a = \'1\';')

    def test_name_assign(self):
        self.assertNotRaises(execute_code, 'let a = 1; let b = a;')

    def test_bracket_assign(self):
        self.assertNotRaises(execute_code, 'let a = (1);')

    def test_kleene_assign(self):
        self.assertNotRaises(execute_code, 'let a = <a>; let b = a *;')
        self.assertRaises(MyEx, execute_code, 'let a = 1; let b = a *;')

    def test_equals(self):
        self.assertNotRaises(execute_code, 'let a = 1; let b = 1; $ a == b;')
        self.assertNotRaises(execute_code, 'let a = <a>; let b = <b>; $ a == b;')
        self.assertRaises(DifferentTypesEx, execute_code, 'let a = <a>; let b = 1; $ a == b;')

    def test_unequals(self):
        self.assertNotRaises(execute_code, 'let a = 1; let b = 1; $ a != b;')
        self.assertNotRaises(execute_code, 'let a = <a>; let b = <b>; $ a != b;')
        self.assertRaises(DifferentTypesEx, execute_code, 'let a = <a>; let b = 1; $ a != b;')

    def test_list_struct(self):
        self.assertNotRaises(execute_code, 'let a = [];')
        self.assertNotRaises(execute_code, 'let a = [1];')
        self.assertNotRaises(execute_code, 'let a = [1, 2];')

    def test_set_struct(self):
        self.assertNotRaises(execute_code, 'let a = ][;')
        self.assertNotRaises(execute_code, 'let a = ]1[;')
        self.assertNotRaises(execute_code, 'let a = ]1, 2[;')

    def test_complex_code(self):
        self.assertNotRaises(execute_code, '$ (((<a> *) & <b>) += start x -> {x // 2} --> ]1, 2, 3[);')
        self.assertNotRaises(execute_code, '$ (((<a> *) & <b>) += start x -> {x // 2} --> [1, 2, 3]);')
        self.assertNotRaises(execute_code, '$ (((<a> *) & <b>) += start x -> {x % 2 == 0} ?-> ]1, 2, 3[);')
        self.assertNotRaises(execute_code, '$ ((<a> * & <b>) += start x -> {x // 2} --> ]1, 2, 3[);')
        self.assertNotRaises(execute_code, '$ (((<a> *) & <b>) := start x -> {x // 2} --> ]1, 2, 3[);')
        self.assertNotRaises(execute_code, '$ (((<a> *) & <b>) += final x -> {x // 2} --> ]1, 2, 3[);')
        self.assertNotRaises(execute_code, '$ (((<a> *) | <b>) += start x -> {x // 2} --> ]1, 2, 3[);')
        self.assertNotRaises(execute_code, '$ (((<a> *) ++ <b>) += start x -> {x // 2} --> ]1, 2, 3[);')
        self.assertNotRaises(execute_code, '$ ((<a> & <b>) += start x -> {x // 2} --> ]1, 2, 3[);')
