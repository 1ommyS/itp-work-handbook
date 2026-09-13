# 50 классических задач LeetCode

Этот список помогает отработать основные паттерны для алгоритмического интервью. Идите по порядку внутри блока: сначала распознайте паттерн, затем научитесь объяснять решение и только потом ускоряйте написание кода.

!!! info "Что означает «топ-50»"
    Это **редакционная подборка**, а не доказанный рейтинг популярности на российских или международных собеседованиях. В неё вошли классические задачи из тематического поля официальных планов [LeetCode 75](https://leetcode.com/studyplan/leetcode-75/) и [Top Interview 150](https://leetcode.com/studyplan/top-interview-150/). Состав конкретного интервью зависит от компании, команды и уровня кандидата.

Все названия, ссылки и сложности сверены с официальными карточками LeetCode 13 сентября 2026 года. Все выбранные задачи доступны без Premium на дату проверки.

## Как работать со списком

Для первой попытки поставьте лимит 30–45 минут. До кода проговорите входные данные, простой подход и ожидаемую сложность. После попытки зафиксируйте причину затруднения: не распознали паттерн, не вывели алгоритм, ошиблись в реализации или пропустили крайний случай.

Задача считается пройденной, если вы можете без подсказки:

- объяснить идею и её корректность;
- написать решение на основном языке интервью;
- назвать временную и пространственную сложность;
- проверить решение на минимальном, обычном и граничном примерах.

## Массивы, hash map и префиксные вычисления

| № | Задача | Сложность | Паттерн | Что тренирует |
| ---: | --- | :---: | --- | --- |
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | Hash map | Поиск дополнения за один проход |
| 2 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Easy | Hash set | Проверку уникальности без вложенных циклов |
| 3 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Easy | Счётчик частот | Сравнение мультимножеств символов |
| 4 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | Канонический ключ | Группировку объектов по вычисляемому признаку |
| 5 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Medium | Prefix / suffix | Повторное использование накопленных вычислений |
| 6 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | Частоты + heap / buckets | Выбор лучших `k` без полной сортировки |
| 7 | [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Medium | Hash set | Поиск начала последовательности и линейный обход |
| 8 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Prefix sum + hash map | Подсчёт подмассивов через разность префиксов |

## Два указателя и скользящее окно

| № | Задача | Сложность | Паттерн | Что тренирует |
| ---: | --- | :---: | --- | --- |
| 9 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Easy | Two pointers | Синхронный проход с двух концов |
| 10 | [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Medium | Two pointers | Использование упорядоченности входа |
| 11 | [3Sum](https://leetcode.com/problems/3sum/) | Medium | Сортировка + two pointers | Дедупликацию и сведение задачи к паре |
| 12 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | Two pointers | Доказательство безопасного сдвига указателя |
| 13 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | Один проход | Поддержание лучшего состояния на префиксе |
| 14 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Sliding window | Окно с ограничением на частоты |
| 15 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Hard | Sliding window | Минимальное окно с несколькими требованиями |

## Стек и монотонный стек

| № | Задача | Сложность | Паттерн | Что тренирует |
| ---: | --- | :---: | --- | --- |
| 16 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | Stack | Сопоставление вложенных пар |
| 17 | [Min Stack](https://leetcode.com/problems/min-stack/) | Medium | Вспомогательное состояние | Проектирование структуры с операциями `O(1)` |
| 18 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | Monotonic stack | Поиск следующего большего элемента |
| 19 | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Hard | Monotonic stack | Границы действия элемента и инвариант стека |

## Бинарный поиск

| № | Задача | Сложность | Паттерн | Что тренирует |
| ---: | --- | :---: | --- | --- |
| 20 | [Binary Search](https://leetcode.com/problems/binary-search/) | Easy | Binary search | Инвариант границ и условие завершения |
| 21 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | Binary search | Поиск упорядоченной половины |
| 22 | [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | Medium | Binary search | Поиск точки разрыва порядка |
| 23 | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Medium | Binary search по ответу | Монотонный предикат и подбор минимального значения |

## Связные списки

| № | Задача | Сложность | Паттерн | Что тренирует |
| ---: | --- | :---: | --- | --- |
| 24 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | Перенаправление ссылок | Безопасное изменение списка на месте |
| 25 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | Dummy node | Сборку результата без особого случая для головы |
| 26 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Easy | Fast / slow pointers | Обнаружение цикла с `O(1)` памяти |
| 27 | [Reorder List](https://leetcode.com/problems/reorder-list/) | Medium | Поиск середины + reverse + merge | Композицию нескольких операций со списком |
| 28 | [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Medium | Два указателя | Фиксированный разрыв между указателями |
| 29 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | Hash map + doubly linked list | Совмещение индекса и порядка использования |

## Деревья и BST

| № | Задача | Сложность | Паттерн | Что тренирует |
| ---: | --- | :---: | --- | --- |
| 30 | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Easy | DFS / BFS | Базовый обход дерева |
| 31 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Easy | Рекурсия | Локальное преобразование каждого узла |
| 32 | [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | Easy | DFS post-order | Возврат одного значения и накопление другого |
| 33 | [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | Easy | DFS post-order | Ранний выход и вычисление высоты |
| 34 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Medium | BFS | Обход дерева по уровням |
| 35 | [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Medium | Границы / inorder | Глобальный инвариант бинарного дерева поиска |
| 36 | [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | Medium | Свойство BST | Навигацию без полного обхода дерева |

## Графы и обход сетки

| № | Задача | Сложность | Паттерн | Что тренирует |
| ---: | --- | :---: | --- | --- |
| 37 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | DFS / BFS по сетке | Поиск компонент связности |
| 38 | [Clone Graph](https://leetcode.com/problems/clone-graph/) | Medium | DFS / BFS + map | Копирование циклической структуры |
| 39 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | Topological sort | Обнаружение цикла в ориентированном графе |
| 40 | [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Medium | Обратный обход | Поиск от множества источников |
| 41 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Medium | Multi-source BFS | Распространение состояния по слоям |

## Интервалы, heap и greedy

| № | Задача | Сложность | Паттерн | Что тренирует |
| ---: | --- | :---: | --- | --- |
| 42 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Medium | Сортировка интервалов | Слияние пересекающихся диапазонов |
| 43 | [Insert Interval](https://leetcode.com/problems/insert-interval/) | Medium | Интервалы | Разбиение прохода на участки до, внутри и после |
| 44 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | Heap / quickselect | Поиск порядковой статистики |
| 45 | [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Medium | Greedy + частоты | Планирование при ограничении на повтор |
| 46 | [Jump Game](https://leetcode.com/problems/jump-game/) | Medium | Greedy | Поддержание максимально достижимой границы |

## Динамическое программирование и backtracking

| № | Задача | Сложность | Паттерн | Что тренирует |
| ---: | --- | :---: | --- | --- |
| 47 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Easy | 1D dynamic programming | Состояние, переход и базовые случаи |
| 48 | [House Robber](https://leetcode.com/problems/house-robber/) | Medium | 1D dynamic programming | Выбор между действием и пропуском |
| 49 | [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | Dynamic programming | Оптимум по префиксу состояний |
| 50 | [Combination Sum](https://leetcode.com/problems/combination-sum/) | Medium | Backtracking | Выбор, откат состояния и отсечение ветвей |

## План прохождения

| Этап | Задачи | Режим |
| --- | --- | --- |
| 1. База | 1–19 | По одному блоку за раз; после каждой задачи записывайте паттерн и сложность |
| 2. Структуры | 20–36 | Чередуйте новую задачу и повтор вчерашней без просмотра кода |
| 3. Обходы | 37–41 | Рисуйте граф или сетку и проговаривайте состояние очереди/стека |
| 4. Выбор и оптимизация | 42–50 | Сначала формулируйте состояние или greedy-инвариант, затем пишите код |
| 5. Смешанная проверка | 10 задач из списка случайно | Решайте с таймером и объяснением вслух, как на интервью |

Не пытайтесь запомнить готовый код. Если решение посмотрено, закройте его и воспроизведите через день, затем ещё раз через неделю. В журнале достаточно пяти полей: задача, дата, причина ошибки, итоговая сложность, дата повтора.

## Что сделать прямо сейчас

- [ ] Выберите язык, на котором будете проходить весь список.
- [ ] Решите задачи 1 и 9 без подсказок как диагностику.
- [ ] Создайте журнал ошибок и назначьте первый повтор через два дня.
- [ ] Попросите рекрутера уточнить, есть ли алгоритмическая секция и какой у неё формат.

## Официальные источники

- [LeetCode 75 — официальный study plan](https://leetcode.com/studyplan/leetcode-75/)
- [Top Interview 150 — официальный study plan](https://leetcode.com/studyplan/top-interview-150/)
- [Top Interview Questions — официальный список задач](https://leetcode.com/problem-list/top-interview-questions/)
- [LeetCode QuickStart Guide](https://support.leetcode.com/hc/en-us/articles/360012067053-LeetCode-QuickStart-Guide)
