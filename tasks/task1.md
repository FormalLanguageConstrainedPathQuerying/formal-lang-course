# Задача 1. Инициализация рабочего окружения

* **Мягкий дедлайн**: 05.09.2021, 23:59
* **Жёсткий дедлайн**: 08.09.2021, 23:59
* Полный балл: 5

## Задача

- [ ] Сделать публичный `fork` данного репозитория.
- [ ] Добавить ссылку на ваш `fork` в [таблицу](https://docs.google.com/spreadsheets/d/18DhYG5CuOrN4A5b5N7-mEDfDkc-7BuXF3Qsu6HD-lks/edit?usp=sharing).
- [ ] Добавить в совладельцы форка одного из ассистентов (чтобы узнать, кого именно, нужно посмотреть в [таблицу](https://docs.google.com/spreadsheets/d/18DhYG5CuOrN4A5b5N7-mEDfDkc-7BuXF3Qsu6HD-lks/edit?usp=sharing))
- [ ] Реализовать консольное приложение, предоставляющее перечисленные ниже возможности. Для работы с графами использовать [cfpq-data](https://jetbrains-research.github.io/CFPQ_Data/tutorial.html#graphs). Данное приложение в дальнейшем будет расширяться. Функции приложения, которые необходимо реализовать:
  - [ ] По имени графа вернуть количество вершин, рёбер и перечислить различные метки, встречающиеся на рёбрах. Для получения графа по имени использовать [эту функцию](https://jetbrains-research.github.io/CFPQ_Data/tutorial.html#get-a-real-graph).
  - [ ] По количеству вершин в циклах и именам меток строить [граф из двух циклов](https://jetbrains-research.github.io/CFPQ_Data/reference/graphs/generated/cfpq_data.graphs.generators.labeled_two_cycles_graph.html#cfpq_data.graphs.generators.labeled_two_cycles_graph) и сохранять его в указанный файл в формате DOT (использовать pydot).
- [ ] Добавить необходимые тесты.
- [ ] Добавить запуск тестов с помощью `pytest` в `.github/workflows/`.
