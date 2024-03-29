# Задача 16. Интерпретатор языка запросов к графам

* **Мягкий дедлайн**: <за неделю перед экзаменом>, 23:59
* **Жёсткий дедлайн**: <день консультации перед экзаменом>, 23:59
* Полный балл: 20


## Задача
В данной задаче необходимо разработать интерпретатор языка запросов согласно спецификации, разработанной в работе 13. Интерпретатор должен быть консольной утилитой и принимать на вход файл, исполнять его, сообщать в консоль о статусе исполнения (завершилось успешно, завершилось с ошибкой). Обратите внимание, что для "публикации" результатов вычислений в языке предусмотрена функция ```print```. Также обратите внимание на адекватность сообщений об исключительных ситуациях (некорректный вход, проблемы с типизацией и т.д.)

Так как интерпретатор --- достаточно сложный проект, для него необходима документация. Частью документации будет спецификация языка из работы 13. Дополнительно необходимо задокументировать особенности системы типов, используемые алгоритмы запросов.

Прежде чем писать код, продумайте его архитектуру. Предусмотрите возможности для тестирования отдельных функций, отдельной функциональности (скажем, тестирование системы типов).

 - [ ] Разработать и описать (в документации) механизм вывода или проверки типов, гарантирующий корректность построения запросов (в частности, что не строится пересечение двух контекстно-свободных языков, или что состояния автоматов задаются значениями допустимых типов).
   - Типизация должна быть строгой.
   - Типизация может быть как статической, так и динамической.
   - Можно использовать как вывод типов, так и проверку типов.
   - Работа системы типов должна соответствовать правилам, указанным в постановке задачи 13 и в вашем её решении (возможны тонкости с частями, абстрактный синтаксис для которых требовалось придумать самостоятельно).
   - Постарайтесь сделать сообщения об ошибках максимально дружественными к пользователю.
 - [ ] Из множества реализованных в предыдущих работах алгоритмов выполнения запросов к графам выбрать те, которые будут использоваться в интерпретаторе. Обосновать свой выбор (зафиксировать в документации).
 - [ ] Используя парсер из работы 14, разработанную систему вывода или проверки типов, выбранные алгоритмы, реализовать интерпретатор языка, описанного в работе 13.
   - Хотя конечное решение и должно быть консольной утилитой, предусмотрите возможности для тестирования. Например, сделайте так, чтобы вход можно было получить из строки и, например, "перехватить" результаты вычислений для их проверки в тестах.
   - Проследите за адекватностью сообщений об ошибках.
   - Постарайтесь максимально использовать возможности ANTLR по работе с деревом разбора.
 - [ ] Добавить необходимые тесты. Тут, как и с парсером, тестов много не бывает. И, как и с парсером, они должны быть атомарными. При этом и на сложных входах надо не забыть протестировать.
