[![Check code style](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/actions/workflows/code_style.yml/badge.svg)](https://github.com/FormalLanguageConstrainedPathQuerying/formal-lang-course/actions/workflows/code_style.yml)
[![Code style](https://img.shields.io/badge/Code%20style-black-000000.svg)](https://github.com/psf/black)
---
# Formal Language Course

> [!NOTE]
> English version of the README can be found in [README.en.md](README.en.md).

Курс по формальным языкам: шаблон структуры репозитория для выполнения домашних работ,
а также материалы курса и другая сопутствующая информация.

Актуальное:
- [Список задач](tasks.md)
- [Стиль кода как референс](https://www.python.org/dev/peps/pep-0008/)
- [О достижимости с ограничениями в терминах формальных языков](https://github.com/FormalLanguageConstrainedPathQuerying/FormalLanguageConstrainedReachability-LectureNotes)
- Классика по алгоритмам синтаксического анализа: [Dick Grune, Ceriel J. H. Jacobs, "Parsing Techniques A Practical Guide"](https://link.springer.com/book/10.1007/978-0-387-68954-8#bibliographic-information)
- Классика по теории формальных языков: [M. A. Harrison. 1978. "Introduction to Formal Language Theory"](https://dl.acm.org/doi/book/10.5555/578595)
- Свежее по теории автоматов и их применению в различных областях: [Editors: Jean-Éric Pin. 2021. "Handbook of Automata Theory"](https://ems.press/books/standalone/172)
- [Инструмент для конструирования и симуляции различных распознователей](https://github.com/spbu-se/KotlinAutomataConstructor)

Технологии:
- Python 3.12
- Pytest для unit тестирования
- GitHub Actions для CI
- Python notebook для постановки и оформления экспериментов
- Управление зависимостями с помощью [Rye](https://rye.astral.sh/)
- Английский язык для документации или самодокументирующийся код

## Содержание

- [Formal Language Course](#formal-language-course)
  - [Содержание](#содержание)
  - [Из чего складывается оценка за курс](#из-чего-складывается-оценка-за-курс)
    - [Летучки](#летучки)
    - [Домашние практические работы](#домашние-практические-работы)
  - [Работа с проектом](#работа-с-проектом)
  - [Домашние практические работы](#домашние-практические-работы-1)
    - [Выполнение домашнего задания](#выполнение-домашнего-задания)
    - [Получение оценки за домашнюю работу](#получение-оценки-за-домашнюю-работу)
  - [Код](#код)
  - [Тесты](#тесты)
  - [Эксперименты](#эксперименты)
  - [Структура репозитория](#структура-репозитория)
  - [Разработчики курса](#разработчики-курса)
  - [Вместо введения](#вместо-введения)

## Из чего складывается оценка за курс

Оценка за курс складывается из баллов, полученных за работу в семестре. Баллы начисляются за следующее.
 - За домашние работы (балл за каждую задачу указывается отдельно).
 - За летучки (короткие, 5-10 минут, контрольные работы). Летучка оценивается от 1 до 0 баллов. Баллы за летучки служат для корректировки баллов за домашние работы.
 - За дополнительные задания от преподавателя, такие как оформление материалов по курсу, реализация демонстрационных алгоритмов и т.д. Оценивается на усмотрение преподавателя но не более 30 баллов за всё.

Итоговая оценка за курс --- это взвешенная сумма баллов за задачи и дополнительные задания, где вес --- баллы за ближайшую справа (в хронологическом порядке) летучку.
Можно думать, что курс разбит на блоки и в каждом блоке есть сколько-то задач и летучка, которая будет весом для этих задач.
Пусть, например, в курсе было два блока по 2 задачи и 2 летучки.
Пусть за первые две задачи получено 4 и 5 баллов, за оставшиеся две 2.5 и 3 балла соответственно. При этом за первую летучку 0.25 балла, за вторую --- 0.75 балла.
Тогда итоговая оценка за курс: $(4+5)*0.25 + (2.5+3)*0.75 = 6.375.$

Баллы конвертируются в оценки следующим образом:

|    Балл     | ECTS  | Классика |
| :---------: | :---: | :------: |
| (90 -- 100] |   A   |    5     |
| (80 -- 90]  |   B   |    4     |
| (70 -- 80]  |   C   |    4     |
| (60 -- 70]  |   D   |    3     |
| (50 -- 60]  |   E   |    3     |
|  [0 -- 50]  |   F   |    2     |

### Летучки

Летучка --- маленькая контрольная работа (на 5-10 минут) которая пишется на паре (обычно в самом начале).
Типичное количество летучек за курс --- 2--3.
Во время написания летучки можно пользоваться любыми материалами, но время написания жёстко ограниченно.
Летучки можно переписывать (переписывания обычно централизованные в конце семестра), но при каждом переписывании максимально возможный балл за летучку падает в два раза.
То есть если за написанную с первой попытки летучку можно получить максимум 1 балл, то за идеально написанную со второй попытки уже только 0.5 балла и т.д.
Боле того, в качестве оценки за летучку засчитывается балл с последней попытки (а не максимум по всем попыткам, например).

Типичные вопросы на летучке:
- Постройте левосторонний вывод данной цепочки в данной грамматике.
- Постройте конечный автомат, задающий тот же язык, что и данное регулярное выражение.
- Какова пространственная сложность алгоритма X?
- Дайте определение рекурсивного конечного автомата.
- В чём отличие НФХ от ОНФХ?

### Домашние практические работы

Работы бывают двух типов:
- С полностью автоматической проверкой. Подразумевается, что к этим задачам известны название и сигнатуры функций, а также набор тестов; если тесты проходят, то задача засчитывается. Количество баллов за такие задачи не менее 60. То есть написав все летучки и сдав все такие задачи можно гарантированно получить 3 (E-D) за курс.
- Требующие проверки преподавателем или ассистентом. Как правило, это задачи на постановку экспериментов или разработку относительно нетривиальных решений. Они основаны на задачах предыдущего типа, потому решать их в изоляции затруднительно.

## Работа с проектом

- Для выполнения домашних практических работ необходимо сделать `fork` этого репозитория к себе в `GitHub`.
- Рекомендуется установить [`pre-commit`](https://pre-commit.com/#install) для поддержания проекта в адекватном состоянии.
  - Установить `pre-commit` можно выполнив следующую команду в корне вашего проекта:
    ```shell
    pre-commit install
    ```
  - Отформатировать код в соответствии с принятым стилем можно выполнив следующую команду в корне вашего проекта:
    ```shell
    pre-commit run --all-files
    ```
- Ссылка на свой `fork` репозитория размещается в таблице курса с результатами.
- В свой репозиторий необходимо добавить проверяющих с `admin` правами на чтение, редактирование и проверку `pull-request`'ов.

## Домашние практические работы

У всех задач есть дедлайн (как правило --- неделя с момента, когда она была задана) после которого максимальный балл за задачу падает в два раза.

Количество проверок ограничено тремя. Единица проверки --- запрос ревью на ПР. После трёх попыток баллы за задачу сгорают.
Первый запрос ревью должен быть ДО дедлайна.
**Обратите внимание**, что коммитов между запросом ревью и самой проверкой быть не должно. То есть сперва убеждаетесь, что всё готово, потом запрашиваете проверку. Если же после запроса и до проверки есть ещё коммиты, то баллы за задачу уменьшаются в два раза.

Обратите внимание, что если проверка запрошена, но выполнены не все требования к решению (не проходит CI, не все пункты задачи выполнены, ответили не на все поставленные вопросы, не соблюли все требования к отчёту), то детальной проверки задачи не проводится, а попытка сдачи сгорает. Скорее всего, в таком случае единственным результатом проверки будет что-то в духе "задача решена не полностью". Потому качественно сделать задание --- ответственность обучающегося.

### Выполнение домашнего задания
При работе необходимо пользоваться GitHub Flow ([подробнее раз](https://githubflow.github.io/),[подробнее два](https://habr.com/ru/articles/346066/)).
Дополнительно, нужно следить за следующими моментами.
- Каждое домашнее задание выполняется в отдельной ветке. Ветка должна иметь осмысленное консистентное название.
- Ветка должна содержать только коммиты сдающего и только те коммиты, которые непосредственно относятся к решению задачи.
- Название файла должно отражать его содержимое (например, название алгоритма).
- Автоматические тесты изменять нельзя. За исключением случаев явно оговоренных в постановке задачи.
- Текст коммитов (commit message) должен быть адекватным и отражать суть происходящего.
- При выполнении домашнего задания в новой ветке необходимо открыть соответствующий `pull-request` в `main` вашего `fork`.
- Обратите внимание, что проходить должны все тесты, а не только для той задачи, которая сдается в данном реквесте.
- `Pull-request` снабдить понятным названием и описанием с соответствующими пунктами прогресса.
- Проверка заданий осуществляется посредством `review` вашего `pull-request` (через заполнение поля Reviewers). Даже если сдаётся задача, не требующая проверки преподавателем, необходимо запросить ревью.
- Как только вы считаете, что задание выполнено, вы можете запросить `review` у проверяющего.
  - Чтобы рассчитывать на полный балл за задачу, `review` должно быть запрошено **до дедлайна**.
- Когда проверка будет пройдена, и задание **зачтено**, его необходимо `merge` в `main` вашего `fork`.
- Результаты выполненных заданий будут повторно использоваться в последующих домашних работах.

### Получение оценки за домашнюю работу

- Если ревью было запрошено _до_ **дедлайна** _и_ задача зачтена с **с первой попытки** _и_ после запроса ревью и до самого ревью в ветку не было коммитов, то вы получаете **полный балл за домашнюю работу**.
- Все остальные варианты --- меньшее количество баллов. Частые случаи:
  - Если проверка запрошена _после_ **дедлайна** _и_ **потрачено не больше трёх попыток**, то вы получаете **половину полного балла за домашнюю работу**.
  - Если проверка запрошена _до_ **дедлайна** _но_ **потрачено больше одной и не больше трёх попыток**, то вы получаете **половину полного балла за домашнюю работу**.
    - Для задач на постановку экспериментов и последней задачи (разработка интерпретатора) в данном случае получаете **3/4 от полного балла (75%)**.
  - Если исчерпано количество попыток сдать задачу (больше трёх), то за неё получаете **0 баллов**.
- Если после запроса ревью и до самого ревью в ветку были ещё коммиты, то за задачу можно получить **максимум половину баллов**. То есть в предыдущих пунктах заменяем **полный балл** на **половину полного балла**.

## Код

- Исходный код практических задач по программированию размещайте в папке `project`.
- Файлам и модулям даем осмысленные имена, в соответствии с официально принятым стилем.
- Структурируем код, используем как классы, так и отдельно оформленные функции. Чем понятнее код, тем быстрее его проверять и тем больше у вас будет шансов получить полный балл.

## Тесты

Тесты бывают двух видов: заготовленные преподавателем и ваши собственные.

Заготовленные тесты существуют в папке `tests/autotests` и используются для проверки задач с полностью автоматической проверкой.
При работе с ними следует соблюдать следующие правила:
- В данных тестах обычно можно изменять только одно --- блок
  ```python
  try:
      from project.task2 import regex_to_dfa, graph_to_nfa
  except ImportError:
      pytestmark = pytest.mark.skip("Task 2 is not ready to test!")
  ```
  В нём необходимо указать из какого(их) модуля(ей) импортировать требуемые функции, в ином случае тесты пропускаются.
- В случае, если вы нашли ошибку **И** готовы её исправить, файл можно изменять, а затем отправлять изменение с помощью Pull Request в основной репозиторий.
- Если же вы нашли ошибку и не готовы заниматься её исправлением, то об этом нужно срочно сообщить преподавателю и не предпринимать других действий!

К вашим собственным тестам применяются следующие правила:
- Тесты для домашних заданий размещайте в папке `tests`.
- Формат именования файлов с тестами `test_[какой модуль\класс\функцию тестирует].py`.
- Для работы с тестами использовать [`pytest`](https://docs.pytest.org/en/6.2.x/).
- Для запуска тестов необходимо из корня проекта выполнить следующую команду:
  ```shell
  python ./scripts/run_tests.py
  ```

## Эксперименты

Эксперимент (настройка, замеры, результаты, анализ результатов) оформляется как Python-ноутбук, который публикуется на GitHub.

- Для выполнения экспериментов потребуется не только код, но окружение и некоторая его настройка. Соответственно, сдаваемое решение должно сопровождаться инструкциями по настройке окружения и воспроизведению экспериментов. В идеале, это всё должно содержаться в ноутбуке.
- Эксперименты должны быть воспроизводимыми (например, проверяющими).
- В ноутбуке выполняется вся настройка, пишется код для экспериментов, подготовки отчетов и графиков.
- Ноутбук снабжается связанным текстом, описывающим цели эксперимента, методику их проведения, анализ результатов, ответы на поставленные вопросы.
  - Ответы на вопросы должны быть обоснованы (экспериментами), наблюдаемое поведение проанализировано и обосновано.
- Результаты экспериментов представляются в виде презентации в отдельно оговоренный день. На рассказ 5 минут. На вопросы и ответы на них --- 3 минуты.
  - Финальная за задачу оценка выставляется по результатам презентации и ответов на вопросы.
  - Ровно одна попытка сделать презентацию.
  - Качество презентации влияет на итоговую оценку. Рекомендуется, например, изучить разделы "Требования к презентации" и "7.3.4. Чеклист по презентации" из [этого документа](https://github.com/yurii-litvinov/courses/blob/master/additional/practices-guide/practices.pdf).

## Структура репозитория

```text
.
├── .github - файлы для настройки CI и проверок
├── docs - текстовые документы и материалы по курсу
├── project - исходный код домашних работ
├── scripts - вспомогательные скрипты для автоматизации разработки
├── tests - директория для unit-тестов домашних работ
│   └── autotests - директория с автотестами для домашних работ
├── pyproject.toml - зависимости для настройки репозитория
├── README.md - основная информация о проекте
└── tasks.md - файл с описанием домашних заданий
```

## Разработчики курса

- Семен Григорьев [@gsvgit](https://github.com/gsvgit)
- Николай Пономарев [@wowaster](https://github.com/WoWaster)
- Ефим Кубышкин [@kubef](https://github.com/KubEF)
- Егор Орачев [@EgorOrachyov](https://github.com/EgorOrachyov)
- Вадим Абзалов [@vdshk](https://github.com/vdshk)
- Рустам Азимов [@rustam-azimov](https://github.com/rustam-azimov)
- Екатерина Шеметова [@katyacyfra](https://github.com/katyacyfra)

## Вместо введения

Данный курс является прикладным. Основная задача --- показать, что формальные языки возникают и могут применяться в разных областях. Примеры таких областей:

- Синтаксический анализ языков программирования: в компиляторах, интерпертаторах, средах разработки, других инстументах.
- Анализ естественных языков. Активность в этой области несколько спала, так как на передний план сейчас вышли различные методы машинного обучения.
  Однако и в этой области ведуться работы.Например, [International Conference on Parsing Technologies](http://www.wikicfp.com/cfp/program?id=1853).
- Статический анализ кода.
  - Различные задачи межпроцедурного анализа. Основной подход --- language reachability. Основоположник --- Томас Репс. Примеры работ.
    - Thomas Reps. 1997. Program analysis via graph reachability. In Proceedings of the 1997 international symposium on Logic programming (ILPS ’97). MIT Press, Cambridge, MA, USA, 5–19.
    - Qirun Zhang and Zhendong Su. 2017. Context-sensitive data-dependence analysis via linear conjunctive language reachability. In Proceedings of the 44th ACM SIGPLAN Symposium on Principles of Programming Languages (POPL 2017). Association for Computing Machinery, New York, NY, USA, 344–358. DOI:https://doi.org/10.1145/3009837.3009848
    - Kai Wang, Aftab Hussain, Zhiqiang Zuo, Guoqing Xu, and Ardalan Amiri Sani. 2017. Graspan: A Single-machine Disk-based Graph System for Interprocedural Static Analyses of Large-scale Systems Code. In Proceedings of the Twenty-Second International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS ’17). Association for Computing Machinery, New York, NY, USA, 389–404. DOI:https://doi.org/10.1145/3037697.3037744
    - Lu Y., Shang L., Xie X., Xue J. (2013) An Incremental Points-to Analysis with CFL-Reachability. In: Jhala R., De Bosschere K. (eds) Compiler Construction. CC 2013. Lecture Notes in Computer Science, vol 7791. Springer, Berlin, Heidelberg
  - Интерливинг (или шафл) языков для верификаци многопоточных программ.
    - [Approximating the Shuffle of Context-free Languages to Find Bugs in Concurrent Recursive Programs](http://uu.diva-portal.org/smash/get/diva2:442518/FULLTEXT01.pdf)
    - Flick N.E. (2015) Quotients of Unbounded Parallelism. In: Leucker M., Rueda C., Valencia F. (eds) Theoretical Aspects of Computing - ICTAC 2015. ICTAC 2015. Lecture Notes in Computer Science, vol 9399. Springer, Cham

  - Система типов Java: [Radu Grigore, Java Generics are Turing Complete](https://arxiv.org/abs/1605.05274).

- Графовые базы данных. Поиск путей с ограничениями.
    - Maurizio Nolé and Carlo Sartiani. 2016. Regular Path Queries on Massive Graphs. In Proceedings of the 28th International Conference on Scientific and Statistical Database Management (SSDBM ’16). Association for Computing Machinery, New York, NY, USA, Article 13, 1–12. DOI:https://doi.org/10.1145/2949689.2949711
    - Jochem Kuijpers, George Fletcher, Nikolay Yakovets, and Tobias Lindaaker. 2019. An Experimental Study of Context-Free Path Query Evaluation Methods. In Proceedings of the 31st International Conference on Scientific and Statistical Database Management (SSDBM ’19). Association for Computing Machinery, New York, NY, USA, 121–132. DOI:https://doi.org/10.1145/3335783.3335791
    - [Jelle Hellings. Querying for Paths in Graphs using Context-Free Path Queries.](https://arxiv.org/abs/1502.02242)

- Биоинформатика. В основном это анализ геномных и белковых последовательностей.
    - [Witold Dyrka, Mateusz Pyzik, Francois Coste, and Hugo Talibart. Estimating probabilistic context-free grammars for proteins using contact map constraints.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6428041/)
    - [James WJ Anderson, Paula Tataru, Joe Staines, Jotun Hein, and Rune Lyngso. Evolving stochastic context-free grammars for RNA secondary structure prediction.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3464655/)
    - [Ryan Zier-Vogel. Predicting RNA secondary structure using a stochastic conjunctive grammar.](https://www.semanticscholar.org/paper/Predicting-RNA-secondary-structure-using-a-grammar-Zier-Vogel/90bb312cb1a0f61eddb7a8b5b782bb40630894dd).

- Машинное обучение.
   - [Matt J. Kusner, Brooks Paige, José Miguel Hernández-Lobato. Grammar Variational Autoencoder](https://arxiv.org/abs/1703.01925). Опубликована в 2017 году и уже [больше 950 цитирований.](https://scholar.google.com/scholar?cites=4080460899049502885&as_sdt=2005&sciodt=0,5&hl=ru)
   - [TAG Parsing with Neural Networks and Vector Representations of Supertags](https://www.aclweb.org/anthology/D17-1180.pdf). К разговору об оброаботке естественных языков.
   - [Jungo Kasai, Robert Frank, Pauli Xu, William Merrill, Owen Rambow. End-to-end Graph-based TAG Parsing with Neural Networks.](https://arxiv.org/abs/1804.06610)

- Языки --- это не только про строки.
  - Языки деревьев: [Tree Automata Techniques and Applications](http://tata.gforge.inria.fr/).
  - Языки графов:
     - [Graph Grammars](http://www.its.caltech.edu/~matilde/GraphGrammarsLing.pdf)
     - [HYPEREDGE REPLACEMENT GRAPH GRAMMARS](https://people.cs.umu.se/drewes/biblio/ps-files/hrg.pdf)
     - [(Re)introducing Regular Graph Languages](https://www.aclweb.org/anthology/W17-3410.pdf)
     - [Hyperedge Replacement: Grammars and Languages](https://www.springer.com/gp/book/9783540560050)
  - $\ldots$
- Теория групп. Как правило, это проблема слов группы или дополнение к ней.
   - Anisimov, A.V. Group languages. Cybern Syst Anal (1971) 7: 594.
   - David E. Muller, Paul E. Schupp, Groups, the Theory of ends, and context-free languages, Journal of Computer and System Sciences, Volume 26, Issue 3, 1983, Pages 295-310, ISSN 0022-0000
   - HOLT, D., REES, S., ROVER, C., \& THOMAS, R. (2005). GROUPS WITH CONTEXT-FREE CO-WORD PROBLEM. Journal of the London Mathematical Society, 71(3), 643-657. doi:10.1112/S002461070500654X
   - [Groups with Context-Free Co-Word Problem and Embeddings into Thompson's Group V](https://arxiv.org/abs/1407.7745)
   - [Kropholler, R. \& Spriano, D. (2019). Closure properties in the class of multiple context-free groups. Groups Complexity Cryptology, 11(1), pp. 1-15. Retrieved 13 Feb. 2020, from doi:10.1515/gcc-2019-2004](https://www.degruyter.com/view/j/gcc.2019.11.issue-1/gcc-2019-2004/gcc-2019-2004.xml)
   - [Word problems of groups, formal languages and decidability](https://personalpages.manchester.ac.uk/staff/Mark.Kambites/events/nbsan/nbsan17_thomas.pdf)

- Прочая интересная математика.
  - Немного топологии в теории формальных языков: [Salvati S. On is an n-MCFL. – 2018.](https://hal.archives-ouvertes.fr/hal-01771670/)
  - Salvati S. MIX is a 2-MCFL and the word problem in Z2 is captured by the IO and the OI hierarchies //Journal of Computer and System Sciences. -- 2015. -- Т. 81. -- \textnumero. 7. -- С. 1252-1277.
  - О том, как задачи из теории графов связаны с теорией формальных языков: Abboud, Amir \& Backurs, Arturs \& Williams, Virginia. (2015). If the Current Clique Algorithms are Optimal, So is Valiant's Parser. 98-117. 10.1109/FOCS.2015.16.
  - [A context-free grammar for the Ramanujan-Shor polynomials](https://www.sciencedirect.com/science/article/abs/pii/S0196885819300739)
