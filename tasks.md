# Задачи по курсу «Формальные языки»

> [!NOTE]
> English version of the tasks can be found in [tasks.en.md](tasks.en.md).

- [Задачи по курсу «Формальные языки»](#задачи-по-курсу-формальные-языки)
  - [Задача 1. Инициализация рабочего окружения](#задача-1-инициализация-рабочего-окружения)
  - [Задача 2. Построение детерминированного конечного автомата по регулярному выражению и недетерминированного конечного автомата по графу](#задача-2-построение-детерминированного-конечного-автомата-по-регулярному-выражению-и-недетерминированного-конечного-автомата-по-графу)
  - [Задача 3. Регулярные запросы для всех пар вершин](#задача-3-регулярные-запросы-для-всех-пар-вершин)
  - [Задача 4. Регулярные запросы для нескольких стартовых вершин](#задача-4-регулярные-запросы-для-нескольких-стартовых-вершин)
  - [Задача 5. Экспериментальное исследование алгоритмов для регулярных запросов](#задача-5-экспериментальное-исследование-алгоритмов-для-регулярных-запросов)
  - [Задача 6. Преобразование грамматики в ОНФХ, алгоритм Хеллингса](#задача-6-преобразование-грамматики-в-онфх-алгоритм-хеллингса)
  - [Задача 7. Матричный алгоритм решения задачи достижимости с КС ограничениями](#задача-7-матричный-алгоритм-решения-задачи-достижимости-с-кс-ограничениями)
  - [Задача 8. Тензорный алгоритм решения задачи достижимости с КС ограничениями](#задача-8-тензорный-алгоритм-решения-задачи-достижимости-с-кс-ограничениями)
  - [Задача 9. Алгоритм решения задачи достижимости с КС ограничениями, основанный на GLL](#задача-9-алгоритм-решения-задачи-достижимости-с-кс-ограничениями-основанный-на-gll)
  - [Задача 10. Экспериментальное исследование алгоритмов решения задачи достижимости с КС ограничениями](#задача-10-экспериментальное-исследование-алгоритмов-решения-задачи-достижимости-с-кс-ограничениями)
  - [Задача 11. Язык запросов к графам](#задача-11-язык-запросов-к-графам)
    - [Конкретный синтаксис](#конкретный-синтаксис)
    - [Правила вывода типов](#правила-вывода-типов)
    - [Динамическая семантика языка запросов](#динамическая-семантика-языка-запросов)
    - [Задача](#задача)
  - [Задача 12. Интерпретатор языка запросов к графам](#задача-12-интерпретатор-языка-запросов-к-графам)


## Задача 1. Инициализация рабочего окружения

Полный балл: 5

- [ ] Сделать `fork` данного репозитория.
- [ ] Добавить ссылку на ваш `fork` в [таблицу](https://docs.google.com/spreadsheets/d/1X7Hx6IyltD_NyTTphyzbN74Ag-G_LDzUu4OGcHoI8tg/edit?usp=sharing).
- [ ] Добавить в совладельцы форка одного из ассистентов (чтобы узнать, кого именно, нужно посмотреть в таблицу)
- [ ] Реализовать модуль, предоставляющий перечисленные ниже возможности. Для работы с графами использовать [cfpq-data](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/tutorial.html#graphs). Данный модуль в дальнейшем будет расширяться. Функции, которые необходимо реализовать:
  - [ ] По имени графа вернуть количество вершин, рёбер и перечислить различные метки, встречающиеся на рёбрах. Для получения графа по имени использовать [эту функцию](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/tutorial.html#load-graph).
  - [ ] По количеству вершин в циклах и именам меток строить [граф из двух циклов](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/reference/graphs/generated/cfpq_data.graphs.generators.labeled_two_cycles_graph.html#cfpq_data.graphs.generators.labeled_two_cycles_graph) и сохранять его в указанный файл в формате DOT (использовать pydot).
- [ ] Добавить необходимые тесты.


## Задача 2. Построение детерминированного конечного автомата по регулярному выражению и недетерминированного конечного автомата по графу

Полный балл: 5

- [ ] Используя возможности [pyformlang](https://pyformlang.readthedocs.io/en/latest/) реализовать **функцию** построения минимального ДКА по заданному регулярному выражению. [Формат регулярного выражения](https://pyformlang.readthedocs.io/en/latest/usage.html#regular-expression).
  - Требуемая функция:
  ```python
  def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
      pass
  ```
- [ ] Используя возможности [pyformlang](https://pyformlang.readthedocs.io/en/latest/) реализовать **функцию** построения недетерминированного конечного автомата по [графу](https://networkx.org/documentation/stable/reference/classes/multidigraph.html), в том числе по любому из графов, которые можно получить, пользуясь функциональностью, реализованной в [Задаче 1](#задача-1-инициализация-рабочего-окружения) (загруженный из набора данных по имени граф, сгенерированный синтетический граф). Предусмотреть возможность указывать стартовые и финальные вершины. Если они не указаны, то считать все вершины стартовыми и финальными.
  - Требуемая функция:
  ```python
  def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
  ) -> NondeterministicFiniteAutomaton:
      pass
  ```
- [ ] Добавить собственные тесты при необходимости.


## Задача 3. Регулярные запросы для всех пар вершин

Полный балл: 5

- [ ] Реализовать тип (`AdjacencyMatrixFA`), представляющий конечный автомат в виде разреженной матрицы смежности из [sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html) (или сразу её булевой декомпозиции) и информации о стартовых и финальных вершинах. У типа должны быть конструктор от `DeterministicFiniteAutomaton` и `NondeterministicFiniteAutomaton` (первый является подклассом второго, так что можно не различать их явно) из [Задачи 2](#задача-2-построение-детерминированного-конечного-автомата-по-регулярному-выражению-и-недетерминированного-конечного-автомата-по-графу).
- [ ] Реализовать функцию-интерпретатор для типа `AdjacencyMatrixFA`, выясняющую, принимает ли автомат заданную строку и является ли язык, задающийся автоматом, пустым. Для реализации последней функции рекомендуется использовать транзитивное замыкание матрицы смежности.
  - Требуемые функции:
     ```python
    def accepts(self, word: Iterable[Symbol]) -> bool:
      pass
    def is_empty(self) -> bool:
      pass
    ```
- [ ] Используя [разреженные матрицы из sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html) реализовать **функцию** пересечения двух конечных автоматов через тензорное произведение.
  - Требуемая функция:
     ```python
    def intersect_automata(automaton1: AdjacencyMatrixFA,
             automaton2: AdjacencyMatrixFA) -> AdjacencyMatrixFA:
        pass
    ```
- [ ] На основе предыдущей функции реализовать **функцию** выполнения регулярных запросов к графам: по графу с заданными стартовыми и финальными вершинами и регулярному выражению вернуть те пары вершин из заданных стартовых и финальных, которые связанны путём, формирующем слово из языка, задаваемого регулярным выражением.
  - Требуемая функция:
     ```python
    def tensor_based_rpq(regex: str, graph: MultiDiGraph, start_nodes: set[int],
           final_nodes: set[int]) -> set[tuple[int, int]]:
        pass
    ```

  - Для конструирования регулярного запроса и преобразований графа использовать результаты [Задачи 2](#задача-2-построение-детерминированного-конечного-автомата-по-регулярному-выражению-и-недетерминированного-конечного-автомата-по-графу).
- [ ] Добавить собственные тесты при необходимости.

## Задача 4. Регулярные запросы для нескольких стартовых вершин

Полный балл: 8

- [ ] Используя [разреженные матрицы из sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html) реализовать **функцию** достижимости с регулярными ограничениями с несколькими стартовыми вершинами (алгоритм на основе multiple source BFS через линейную алгебру).
  - Для конструирования регулярного запроса и графа использовать [Задачи 2](#задача-2-построение-детерминированного-конечного-автомата-по-регулярному-выражению-и-недетерминированного-конечного-автомата-по-графу).
  - Требуемая функция:
  ```python
  def ms_bfs_based_rpq(regex: str, graph: MultiDiGraph, start_nodes: set[int],
           final_nodes: set[int]) -> set[tuple[int, int]]:
    pass
  ```
- [ ] Добавить собственные тесты при необходимости.

## Задача 5. Экспериментальное исследование алгоритмов для регулярных запросов

Полный балл: 25

Обратите внимание, что это максимальный балл. Реальная оценка может быть снижена, в том числе по результатам презентации.

Задача посвящена анализу производительности  алгоритма решения задачи достижимости между всеми парами вершин и с заданным множеством стартовых вершин с регулярными ограничениями.

Исследуются следующие задачи достижимости, решаемые в предыдущих работах.
- Достижимость между всеми парами вершин.
- Достижимость для каждой из заданного множества стартовых вершин.

Вопросы, на которые необходимо ответить в ходе исследования.
- Какое представление разреженных матриц и векторов лучше подходит для каждой из решаемых задач?
- Начиная с какого размера стартового множества выгоднее решать задачу для всех пар и выбирать нужные?

Решение данной задачи оформляется как Python notebook. Для того, чтобы обеспечить возможность проверки, необходимо сделать notebook самодостаточным: в него должны быть включены все действия, необходимые для воспроизведения эксперимента. Также в notebook размещается отчет и анализ результатов ваших экспериментов в текстовом виде. Отчет сопровождается диаграммами, таблицами, картинками, если это необходимо для объяснения результатов.

Решением является не просто код, но отчёт об экспериментальном исследовании, оформленный в виде презентации, который должен являться связанным рассказом и содержать (как минимум) следующие разделы:
- Постановка задачи
- Описание исследуемых решений
- Описание набора данных для экспериментов
  - Графы
  - Запросы
- Описание эксперимента
  - Оборудование
  - Что и как замерялось, как эти измерения должны помочь ответить на поставленные вопросы
- Результаты экспериментов
  - Графики, таблицы
- Анализ результатов экспериментов
  - Ответы на поставленные вопросы, **аргументация ответов**. Обратите внимание, что "мне кажется", "я думаю" и прочие подобные формулировки аргументами не являются. Необходимы результаты замеров, профилирования, другие цифры.

При постановке экспериментов и базовом анализе результатов не лишним будет воспользоваться [советами отсюда](https://github.com/spbu-se/measurements/blob/main/measurements_cheat_sheet.pdf).
При написании отчёта можно попробовать вдохновиться рекомендациями [отсюда](https://github.com/spbu-se/matmex-diploma-template/blob/master/040_experiment.tex).

- [ ] Создать Python notebook, подключить необходимые зависимости.
- [ ] Подключить решения из предыдущих работ.
- [ ] Сформировать набор данных.
  - [ ] Выбрать некоторые графы из [набора](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/index.html). Не забудьте обосновать, почему выбрали именно эти графы.
  - [ ] Используя функцию из первой домашней работы узнать метки рёбер графов и на основе этой информации сформулировать не менее четырёх различных запросов к каждому графу. Лучше использовать наиболее часто встречающиеся метки. Требования к запросам:
      - Запросы ко всем графам должны следовать некоторому общему шаблону. Например, если есть графы ```g1``` и ```g2``` с различными наборами меток, то ожидается, что запросы к ним будут выглядеть, например, так:
        - ```g1```:
          - ```(l1 | l2)* l3```
          - ```(l3 | l4)+ l1*```
          - ```l1 l2 l3 (l4|l1)*```
        - ```g2```:
          - ```(m1 | m3)* m2```
          - ```(m1 | m3)+ m2*```
          - ```m1 m2 m3 (m3|m1)*```
      - В запросах должны использоваться все общепринятые конструкции регулярных выражений  (замыкание, конкатенация, альтернатива). То есть хотя бы в одном запросе к каждому графу должна быть каждая из этих конструкций.
  - [ ] Для генерации множеств стартовых вершин воспользоваться [этой функцией](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/reference/graphs/generated/cfpq_data.graphs.utils.multiple_source_utils.html#cfpq_data.graphs.utils.multiple_source_utils.generate_multiple_source). Не забывайте, что от того, как именно устроено стартовое множество, сильно зависит время вычисления запроса.
- [ ] Сформулировать этапы эксперимента. Что нужно сделать, чтобы ответить на поставленные вопросы? Почему?
- [ ] Провести необходимые эксперименты, замеры.
- [ ] Оформить результаты экспериментов.
- [ ] Провести анализ результатов.
  - [ ] Ответить на поставленные вопросы.
  - [ ] Аргументировать ответы (пользуясь полученными результатами экспериментов).
- [ ] Не забыть опубликовать notebook в репозитории.
- [ ] Не забыть подготовить презентацию и выступить с докладом. Проверьте требования из релевантных инструкций. Например, разделы "Требования к презентации" и "7.3.4. Чеклист по презентации" из [этого документа](https://github.com/yurii-litvinov/courses/blob/master/additional/practices-guide/practices.pdf). Обратите внимание, что в вашей презентации фокус на экспериментах.
- [ ] Не забыть выложить презентацию в репозиторий.

## Задача 6. Преобразование грамматики в ОНФХ, алгоритм Хеллингса

Полный балл: 10

- [ ] Используя [возможности pyformlang для работы с контекстно-свободными грамматиками](https://pyformlang.readthedocs.io/en/latest/usage.html#context-free-grammar) реализовать **функцию** преобразования контекстно-свободной грамматики в ослабленную нормальную форму Хомского (ОНФХ).
  ```python
  def cfg_to_weak_normal_form(cfg: pyformlang.cfg.CFG) -> pyformlang.cfg.CFG:
      pass
  ```
- [ ] Реализовать **функцию**, основанную на алгоритме Хеллингса, решающую задачу достижимости между всеми парами вершин для заданного графа и заданной КС грамматики (не обязательно в ОНФХ).
  - Для работы с графом использовать функции из предыдущих задач.
  ```python
  def hellings_based_cfpq(
    cfg: pyformlang.cfg.CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
  ) -> set[tuple[int, int]]:
     pass
  ```
- [ ] Добавить собственные тесты при необходимости.

## Задача 7. Матричный алгоритм решения задачи достижимости с КС ограничениями

Полный балл: 10

- [ ] Реализовать **функцию**, основанную на матричном алгоритме, решающую задачу достижимости между всеми парами вершин для заданного графа и заданной КС грамматики.
  - Для преобразования грамматики в ОНФХ использовать результаты предыдущих работ.
  - Для реализации матричных операций использовать [sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html).
    ```python
    def matrix_based_cfpq(
        cfg: pyformlang.cfg.CFG,
        graph: nx.DiGraph,
        start_nodes: Set[int] = None,
        final_nodes: Set[int] = None,
    ) -> set[tuple[int, int]]:
      pass
    ```
- [ ] Добавить собственные тесты при необходимости.

## Задача 8. Тензорный алгоритм решения задачи достижимости с КС ограничениями

Полный балл: 10

- [ ] Реализовать **функцию**, основанную на тензорном алгоритме, решающую задачу достижимости между всеми парами вершин для заданного графа и заданной КС грамматики.
  - Для преобразования грамматики в RSM использовать результаты предыдущих работ. Явно опишите **функции** преобразования CFG -> RSM и EBNF -> RSM
  - Для реализации матричных операций использовать [sciPy](https://docs.scipy.org/doc/scipy/reference/sparse.html).
  - Необходимые функции:
  ```python
  def tensor_based_cfpq(
    rsm: pyformlang.rsa.RecursiveAutomaton,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
  ) -> set[tuple[int, int]]:
    pass


  def cfg_to_rsm(cfg: pyformlang.cfg.CFG) -> pyformlang.rsa.RecursiveAutomaton:
    pass


  def ebnf_to_rsm(ebnf: str) -> pyformlang.rsa.RecursiveAutomaton:
    pass
  ```
- [ ] Добавить собственные тесты при необходимости.

## Задача 9. Алгоритм решения задачи достижимости с КС ограничениями, основанный на GLL

Полный балл: 15

- [ ] Реализовать **функцию**, основанную на алгоритме Generalized LL (работающего с RSM), решающую задачу достижимости между всеми парами вершин для заданного графа и заданной КС грамматики.
  - Для работы с графами и RSM использовать функции из предыдущих задач.
  - Требуемая функция:
  ```python
  def gll_based_cfpq(
        rsm: pyformlang.rsa.RecursiveAutomaton,
        graph: nx.DiGraph,
        start_nodes: set[int] = None,
        final_nodes: set[int] = None,
    ) -> set[tuple[int, int]]:
    pass
  ```
- [ ] Добавить собственные тесты при необходимости.

## Задача 10. Экспериментальное исследование алгоритмов решения задачи достижимости с КС ограничениями

Полный балл: 30

Обратите внимание, что это максимальный балл. Реальная оценка может быть снижена, в том числе по результатам презентации.

Задача посвящена анализу производительности различных алгоритмов решения задачи достижимости между всеми парами вершин с контекстно-свободными ограничениями: алгоритма Хеллингса, матричного алгоритма, тензорного алгоритма, алгоритма на основе GLL. В ходе анализа необходимо ответить на следующие вопросы.
- Какой из трёх указанных алгоритмов обладает лучшей производительностью?
- Имеет ли смысл для решения задачи достижимости с регулярными ограничениями использовать алгоритмы для КС ограничений (ведь регулярные --- частный случай КС) или всё же лучше использовать специализированные алгоритмы для регулярных ограничений?
- Как влияет грамматика на производительность тензорного алгоритма и алгоритма на основе GLL? Если зафиксировать язык, то как свойства грамматики (размер, (не)однозначность) влияют на производительность.

Решение данной задачи оформляется как Python notebook. Для того, чтобы обеспечить возможность проверки, необходимо сделать notebook самодостаточным: в него должны быть включены все действия, необходимые для воспроизведения эксперимента. Также в notebook размещается отчет и анализ результатов ваших экспериментов в текстовом виде. Отчет сопровождается диаграммами, таблицами, картинками, если это необходимо для объяснения результатов.

Решением является не просто код, но отчёт об экспериментальном исследовании, оформленный в виде презентации, который должен являться связанным рассказом и содержать (как минимум) следующие разделы:
- Постановка задачи (исследовательские вопросы)
- Описание исследуемых решений
- Описание набора данных для экспериментов
  - Графы
  - Запросы
- Описание эксперимента
  - Оборудование
  - Что и как замерялось, как эти измерения должны помочь ответить на поставленные вопросы
- Результаты экспериментов
  - Графики, таблицы
- Анализ результатов экспериментов
  - Ответы на поставленные вопросы, **аргументация, обоснование ответов**. Обратите внимание, что "мне кажется", "я думаю" и прочие подобные формулировки аргументами не являются. Необходимы результаты замеров, профилирования, другие цифры.

- [ ] Создать Python notebook, подключить необходимые зависимости.
- [ ] Подключить необходимые решения из предыдущих работ.
- [ ] Сформировать набор данных.
  - [ ] Выбрать некоторые графы из [набора](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/index.html). Не забудьте обосновать, почему выбрали именно эти графы. Обратите внимание, что в наборе есть графы и грамматики для различных прикладных задач (анализ RDF, анализ указателей в С, анализ Java-программ). Рекомендуется выбирать графы, относящиеся к различным областям.
  - [ ] В качестве запросов предлагается использовать грамматики из раздела "Canonical grammars" в описании соответствующего графа ([пример](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/data/taxonomy_hierarchy.html#canonical-grammars)). При необходимости (например, при ответе на третий вопрос), можно "оптимизировать" грамматику, вручную создав оптимальную RSM. Или же наоборот, преобразовать её в ОНФХ, или сделать её (не)однозначной.
- [ ] Сформулировать этапы эксперимента. Что нужно сделать, чтобы ответить на поставленные вопросы? Почему?
- [ ] Провести необходимые эксперименты, замеры
- [ ] Оформить результаты экспериментов
- [ ] Провести анализ результатов
  - [ ] Ответить на поставленные вопросы
  - [ ] Аргументировать ответы (пользуясь полученными результатами экспериментов)
- [ ] Не забыть опубликовать notebook в репозитории
- [ ] Не забыть подготовить презентацию и выступить с докладом. Проверьте требования из релевантных инструкций. Например, разделы "Требования к презентации" и "7.3.4. Чеклист по презентации" из [этого документа](https://github.com/yurii-litvinov/courses/blob/master/additional/practices-guide/practices.pdf). Обратите внимание, что в вашей презентации фокус на экспериментах.
- [ ] Не забыть выложить презентацию в репозиторий.

## Задача 11. Язык запросов к графам

Полный балл: 15

### Конкретный синтаксис
```
prog = stmt*

stmt = bind | add | remove | declare

declare = 'let' VAR 'is' 'graph'

bind = 'let' VAR '=' expr

remove = 'remove' ('vertex' | 'edge' | 'vertices') expr 'from' VAR

add = 'add' ('vertex' | 'edge') expr 'to' VAR

expr = NUM | CHAR | VAR | edge_expr | set_expr | regexp | select

set_expr = '[' expr (',' expr)* ']'

edge_expr = '(' expr ',' expr ',' expr ')'

regexp = CHAR | VAR | '(' regexp ')' | (regexp '|' regexp) | (regexp '^' range) | (regexp '.' regexp) | (regexp '&' regexp)

range = '[' NUM '..' NUM? ']'

select = v_filter? v_filter? 'return' VAR (',' VAR)? 'where' VAR 'reachable' 'from' VAR 'in' VAR 'by' expr

v_filter = 'for' VAR 'in' expr

VAR = [a..z] [a..z 0..9]*
NUM = 0 | ([1..9] [0..9]*)
CHAR = '"' [a..z] '"'

```

Пример запроса.

```
let g is graph

add edge (1, "a", 2) to g
add edge (2, "a", 3) to g
add edge (3, "a", 1) to g
add edge (1, "c", 5) to g
add edge (5, "b", 4) to g
add edge (4, "b", 5) to g

let q = "a"^[1..3] . q . "b"^[2..3] | "c"

let r1 = for v in [2] return u where u reachable from v in g by q

add edge (5, "d", 6) to g

let r2 = for v in [2,3] return u,v where u reachable from v in g by (q . "d")

```

### Правила вывода типов

Константы типизируются очевидным образом.

Тип переменной определяется типом выражения, с которым она связана.
```
[b(v)] => t
_________________
[Var (v)](b) => t
```

Пересечение для двух КС не определено.

```
[e1](b) => FA ;  [e2](b) => FA
______________________________________
[Intersect (e1, e2)](b) => FA


[e1](b) => FA ;  [e2](b) => RSM
_______________________________________
[Intersect (e1, e2)](b) => RSM


[e1](b) => RSM ;  [e2](b) => FA
_______________________________________
[Intersect (e1, e2)](b) => RSM

```

Остальные операции над автоматами типизируются согласно формальных свойств классов языков.
```
[e1](b) => FA ;  [e2](b) => FA
_____________________________________
[Concat (e1, e2)](b) => FA


[e1](b) => FA ;  [e2](b) => RSM
______________________________________
[Concat (e1, e2)](b) => RSM


[e1](b) => RSM ;  [e2](b) => FA
______________________________________
[Concat (e1, e2)](b) => RSM


[e1](b) => RSM ;  [e2](b) => RSM
______________________________________
[Concat (e1, e2)](b) => RSM

```

```
[e1](b) => FA ;  [e2](b) => FA
______________________________________
[Union (e1, e2)](b) => FA


[e1](b) => FA ;  [e2](b) => RSM
_______________________________________
[Union (e1, e2)](b) => RSM


[e1](b) => RSM ;  [e2](b) => FA
_______________________________________
[Union (e1, e2)](b) => RSM


[e1](b) => RSM ;  [e2](b) => RSM
_______________________________________
[Union (e1, e2)](b) => RSM

```

```
[e](b) => FA
______________________
[Repeat (e)](b) => FA


[e](b) => RSM
______________________
[Repeat (e)](b) => RSM

```

```
[e](b) => char
________________________
[Symbol (e)](b) => FA

```

Запрос возвращает множество (вершин или пар вершин)

```
[e](b) => Set<int>
_______________________________
[VFilter (v, e)](b) => Set<int>


[q](b) => RSM, [ret](b) => int
_____________________________________________________
[Select (vf1, vf2, ret, v1, v2, g, q)](b) => Set<int>


[q](b) => FA, [ret](b) => int
_____________________________________________________
[Select (vf1, vf2, ret, v1, v2, g, q)](b) => Set<int>


[q](b) => FA, [ret](b) => int * int
____________________________________________________________
[Select (vf1, vf2, ret, v1, v2, g, q)](b) => Set<int * int>


[q](b) => RSM, [ret](b) => int * int
____________________________________________________________
[Select (vf1, vf2, ret, v1, v2, g, q)](b) => Set<int * int>

```


### Динамическая семантика языка запросов

Связывание переопределяет имя.

```
[e](b1) => x,b2
_____________________________________
[Bind (v, e)](b1) => (), (b1(v) <= x)

```

Результатом исполнения программы является словарь, где ключ --- имя переменной в связывании, у которого в правой части select, а значение --- результат вычисления соответствующего запроса.

### Задача
- [ ] С использованием ANTLR реализовать синтаксический анализатор предложенного выше языка. А именно, реализовать функцию, которая принимает строку и возвращает дерево разбора.
- [ ] Реализовать функцию, которая по дереву разбора возвращает количество узлов в нём. Для работы **обязательно** использовать механизмы обхода дерева, предоставляемые ANTLR.
- [ ] Реализовать функцию, которая по дереву разбора строит ранее разобранную строку. Для работы **обязательно** использовать механизмы обхода дерева, предоставляемые ANTLR.
- [ ] Расширить CI шагом генерации парсера по спецификации. Обратите внимание, что генерируемые по спецификации файлы не выкладываются в репозиторий.
  - [Grammarinator](https://github.com/renatahodovan/grammarinator), используемый нами для генерации тестов, подтягивает вместе с собой [ANTLeRinator](https://github.com/renatahodovan/antlerinator), который можно использовать для получения исполняемого файла ANTLR
  - Либо можно использовать более стандартные [antlr4-tools](https://github.com/antlr/antlr4-tools)

Требуемые функции:
```python
# Второе поле показывает корректна ли строка (True, если корректна)
def program_to_tree(program: str) -> tuple[ParserRuleContext, bool]:
    pass

def nodes_count(tree: ParserRuleContext) -> int:
    pass

def tree_to_program(tree: ParserRuleContext) -> str:
    pass
```

## Задача 12. Интерпретатор языка запросов к графам

Полный балл: 22

В данной задаче необходимо разработать интерпретатор языка запросов, разработанного в предыдущей работе. Для исполнения запросов использовать алгоритмы, реализованные в предыдущих работах. Кроме реализации необходимо предоставить минимальную документацию, поясняющую принятые в процессе реализации решения (например, в readme).

Обратите внимание, что кроме непосредственно интерпретатора необходимо реализовать вывод типов. Тестирование данной функциональности должно быть возможно в изоляции. Фактически, должна быть реализована отдельная функция, которая по дереву разбора выводит типы и кидает исключение, если программа не можете быть типизирована корректно.

 - [ ] Реализовать механизм вывода типов, гарантирующий корректность построения запросов (в частности, что не строится пересечение двух контекстно-свободных языков, или что множества вершин задаются значениями допустимых типов).
   - Работа системы типов должна соответствовать правилам, указанным предыдущей задаче.
   - Постарайтесь сделать сообщения об ошибках максимально дружественными к пользователю.
 - [ ] Из множества реализованных в предыдущих работах алгоритмов выполнения запросов к графам выбрать те, которые будут использоваться в интерпретаторе. Обосновать свой выбор (зафиксировать в документации).
 - [ ] Используя парсер из предыдущей работы, разработанную систему вывода типов, выбранные алгоритмы, реализовать интерпретатор языка, описанного в предыдущей задаче.
   - Требуется реализовать функцию, которая по дереву разбора, предоставленному ANTLR, вернёт словарь, содержащий для всех связываний, где в правой части `select`, имя (левую часть связывания) в качестве ключа, а в качестве значения --- результат выполнения соответствующего запроса.
   - Проследите за адекватностью сообщений об ошибках. Вам же проще отлаживаться будет.
   - Постарайтесь максимально использовать возможности ANTLR по работе с деревом разбора.
 - [ ] Добавить необходимые тесты.

Требуемые функции:

```python
def typing_program(program: str) -> bool:
  pass

def exec_program(program: str) -> dict[str, set[tuple]]:
  pass
```
