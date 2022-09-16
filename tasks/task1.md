# Задача 1. Инициализация рабочего окружения

* **Мягкий дедлайн**: 11.09.2022, 23:59
* **Жёсткий дедлайн**: 14.09.2022, 23:59
* Полный балл: 5

## Задача

- [ ] Сделать **приватный** `fork` данного репозитория.
- [ ] Добавить ссылку на ваш `fork` в [таблицу](https://docs.google.com/spreadsheets/d/1IXeAhVb_cRRQf0UwHjw2AeBqNwpcY-XcnVs3-t9HBYc/edit#gid=0).
- [ ] Добавить в совладельцы форка одного из ассистентов (чтобы узнать, кого именно, нужно посмотреть в [таблицу](https://docs.google.com/spreadsheets/d/1IXeAhVb_cRRQf0UwHjw2AeBqNwpcY-XcnVs3-t9HBYc/edit#gid=0))
- [ ] Реализовать модуль, предоставляющий перечисленные ниже возможности. Для работы с графами использовать [cfpq-data](https://jetbrains-research.github.io/CFPQ_Data/tutorial.html#graphs). Данный модуль в дальнейшем будет расширяться. Функции, которые необходимо реализовать:
  - [ ] По имени графа вернуть количество вершин, рёбер и перечислить различные метки, встречающиеся на рёбрах. Для получения графа по имени использовать [эту функцию](https://jetbrains-research.github.io/CFPQ_Data/tutorial.html#get-a-real-graph).
  - [ ] По количеству вершин в циклах и именам меток строить [граф из двух циклов](https://jetbrains-research.github.io/CFPQ_Data/reference/graphs/generated/cfpq_data.graphs.generators.labeled_two_cycles_graph.html#cfpq_data.graphs.generators.labeled_two_cycles_graph) и сохранять его в указанный файл в формате DOT (использовать pydot).
- [ ] Добавить необходимые тесты.
- [ ] Добавить запуск тестов с помощью `pytest` в `.github/workflows/`.
