# Задача 1. Инициализация рабочего окружения

* **Мягкий дедлайн**: --
* **Жёсткий дедлайн**: 26.02.2023, 23:59
* Полный балл: 5

## Задача

- [x] Сделать `fork` данного репозитория.
- [x] Добавить ссылку на ваш `fork` в [таблицу](https://docs.google.com/spreadsheets/d/14h6hUWGMfVhwkxCb9KmRc_yt4VgeecyMEIMDC6zg95c/edit#gid=0).
- [x] Добавить в совладельцы форка одного из ассистентов (чтобы узнать, кого именно, нужно посмотреть в [таблицу](https://docs.google.com/spreadsheets/d/14h6hUWGMfVhwkxCb9KmRc_yt4VgeecyMEIMDC6zg95c/edit#gid=0))
- [x] Реализовать модуль, предоставляющий перечисленные ниже возможности. Для работы с графами использовать [cfpq-data](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/tutorial.html#graphs). Данный модуль в дальнейшем будет расширяться. Функции, которые необходимо реализовать:
  - [x] По имени графа вернуть количество вершин, рёбер и перечислить различные метки, встречающиеся на рёбрах. Для получения графа по имени использовать [эту функцию](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/tutorial.html#get-a-real-graph).
  - [x] По количеству вершин в циклах и именам меток строить [граф из двух циклов](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/reference/graphs/generated/cfpq_data.graphs.generators.labeled_two_cycles_graph.html#cfpq_data.graphs.generators.labeled_two_cycles_graph) и сохранять его в указанный файл в формате DOT (использовать pydot).
- [x] Добавить необходимые тесты.
- [x] Добавить запуск тестов с помощью `pytest` в `.github/workflows/`.
