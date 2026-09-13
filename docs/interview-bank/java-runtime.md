# Java Runtime и concurrency: вопросы 81–160

Продолжение банка Java-вопросов для углублённой подготовки. Здесь проверяются не определения из Java Core, а понимание выполнения байткода, модели памяти, сборщиков мусора, конкурентных примитивов и диагностики JVM.

## Навигация

- [Загрузка классов и байткод](#class-loading-bytecode) — вопросы 81–94
- [Память JVM и Java Memory Model](#jvm-memory-jmm) — вопросы 95–108
- [GC: сборщики, настройка и диагностика](#gc-tuning-diagnostics) — вопросы 109–124
- [Потоки, locks, atomics и async API](#concurrency-runtime) — вопросы 125–146
- [Virtual threads и structured concurrency](#virtual-threads-structured-concurrency) — вопросы 147–154
- [Performance и профилирование](#performance-profiling) — вопросы 155–160
- [Официальные источники](#official-sources)

## Загрузка классов и байткод { #class-loading-bytecode }

<a id="q81-class-loading-lifecycle"></a>
**81. Из каких этапов состоит жизненный цикл класса в JVM?** · middle
**Ориентир:** JVM последовательно выполняет loading, linking — verification, preparation и при необходимости resolution — и initialization. На initialization исполняются статические инициализаторы, а загрузка класса сама по себе ещё не гарантирует их запуск.

<a id="q82-parent-delegation"></a>
**82. Как работает parent delegation у загрузчиков классов?** · middle
**Ориентир:** Загрузчик сначала просит родителя найти класс и только затем ищет его сам; это защищает базовые классы платформы и уменьшает дублирование. Некоторые контейнеры и модульные системы намеренно используют child-first или другие схемы, что важно учитывать при конфликтах зависимостей.

<a id="q83-class-identity"></a>
**83. Почему одинаковые `.class`-файлы могут представлять разные типы?** · middle
**Ориентир:** Идентичность класса определяется парой «бинарное имя + определивший ClassLoader». Поэтому объект класса, загруженного одним loader, нельзя привести к одноимённому классу другого loader.

<a id="q84-bootstrap-platform-application-loaders"></a>
**84. За что отвечают bootstrap, platform и application class loaders?** · junior/middle
**Ориентир:** Bootstrap загружает ключевые классы Java Runtime, platform — классы платформы вне bootstrap-набора, application — классы из class path или module path приложения. Конкретные реализации и внутренние имена loader'ов не являются частью стабильного прикладного контракта.

<a id="q85-class-initialization-triggers"></a>
**85. Какие действия инициируют инициализацию класса?** · middle
**Ориентир:** Обычно это создание экземпляра, вызов статического метода, обращение к неконстантному статическому полю или некоторые операции reflection/method handles. Чтение compile-time constant может быть встроено в вызывающий байткод и не запустить инициализацию владельца.

<a id="q86-initialization-failure"></a>
**86. Что произойдёт, если статический инициализатор завершится исключением?** · middle
**Ориентир:** Первый активный вызов обычно получает `ExceptionInInitializerError`, а класс остаётся ошибочно инициализированным для данного loader. Последующие попытки использовать его приводят к `NoClassDefFoundError`, поэтому причину ищут в самом первом исключении.

<a id="q87-class-unloading"></a>
**87. Когда JVM может выгрузить класс?** · senior
**Ориентир:** Класс может быть выгружен, когда определивший его ClassLoader недостижим вместе со всеми загруженными им классами и их экземплярами. Утечки loader'ов часто вызывают статические кэши, `ThreadLocal`, зарегистрированные callbacks и потоки контейнера.

<a id="q88-bytecode-verification"></a>
**88. Зачем JVM проверяет байткод перед исполнением?** · middle
**Ориентир:** Verification проверяет структурную корректность, типобезопасность операндов, допустимость переходов и доступов. Это позволяет JVM доверять ряду инвариантов даже для байткода, созданного не `javac`.

<a id="q89-stack-machine-bytecode"></a>
**89. Почему JVM называют стековой машиной и что это значит для байткода?** · middle
**Ориентир:** Большинство инструкций берут операнды из operand stack текущего frame и кладут результат обратно, а локальные значения хранятся в local variable array. Это модель class file; JIT затем свободно переводит её в регистровый машинный код.

<a id="q90-invocation-opcodes"></a>
**90. Чем отличаются `invokestatic`, `invokevirtual`, `invokeinterface`, `invokespecial` и `invokedynamic`?** · senior
**Ориентир:** Они выражают разные правила связывания вызова: статический, виртуальный, интерфейсный, специальный для конструкторов/private/super и динамически настраиваемый call site. `invokedynamic` применяется, например, для реализации лямбд и может связываться bootstrap-методом во время выполнения.

<a id="q91-constant-pool"></a>
**91. Что хранит runtime constant pool класса?** · middle
**Ориентир:** Он создаётся из constant pool в class file и содержит литералы и символические ссылки на типы, поля и методы. Resolution превращает символические ссылки в доступные JVM сущности сразу или лениво.

<a id="q92-descriptors-signatures-erasure"></a>
**92. Чем descriptor метода отличается от generic signature?** · senior
**Ориентир:** Descriptor задаёт реальные JVM-типы параметров и результата после erasure и участвует в linkage. Generic signature — дополнительный metadata-атрибут для компилятора и reflection, поэтому JVM может исполнять класс и без него.

<a id="q93-jar-hell-linkage-errors"></a>
**93. Как отличить `ClassNotFoundException`, `NoClassDefFoundError` и `NoSuchMethodError`?** · middle
**Ориентир:** Первое checked-исключение обычно возникает при явной динамической загрузке, второе — когда JVM не может определить ранее доступный класс, а третье означает несовместимость с фактически загруженной версией API. Для диагностики проверяют class path/module path, дерево зависимостей и источник загруженного класса.

<a id="q94-java-agents-instrumentation"></a>
**94. Как Java agent и Instrumentation меняют классы?** · senior
**Ориентир:** Agent подключается при старте или динамически и регистрирует transformer, который меняет class bytes при загрузке или retransformation. Возможности ограничены спецификацией Instrumentation, а ошибки трансформации влияют на startup, отладку и совместимость инструментов.

## Память JVM и Java Memory Model { #jvm-memory-jmm }

<a id="q95-object-layout"></a>
**95. Из чего обычно состоит объект в HotSpot?** · middle
**Ориентир:** Обычно это header, поля экземпляра и padding для выравнивания; точный layout зависит от JVM, платформы и настроек compressed ordinary object pointers/class pointers. Размер следует измерять подходящим инструментом, а не вычислять только по сумме полей.

<a id="q96-compressed-oops"></a>
**96. Что дают compressed oops и compressed class pointers?** · senior
**Ориентир:** HotSpot может хранить ссылки и указатели на метаданные класса в сжатом виде, уменьшая heap footprint и трафик памяти. Эффект и доступность зависят от размера heap и размещения памяти, поэтому проверяют фактические VM flags.

<a id="q97-tlab-allocation"></a>
**97. Зачем нужны TLAB и fast-path allocation?** · middle
**Ориентир:** Thread-local allocation buffer позволяет большинству потоков выделять небольшие объекты сдвигом локального указателя без общего lock. Исчерпание TLAB, крупные объекты и особенности сборщика переводят аллокацию на более дорогой путь.

<a id="q98-escape-analysis"></a>
**98. Что JIT может сделать благодаря escape analysis?** · senior
**Ориентир:** Если объект не покидает метод или поток, JIT может устранить аллокацию через scalar replacement и убрать некоторые locks. Это оптимизация компилятора, а не гарантия размещения объекта на стеке.

<a id="q99-direct-memory"></a>
**99. Чем direct buffers отличаются от heap buffers?** · middle
**Ориентир:** `ByteBuffer.allocateDirect` использует off-heap native memory, удобную для некоторых I/O-операций без дополнительного копирования. Освобождение связано с reachability и cleaner, а лимит и утечки диагностируются отдельно от Java heap.

<a id="q100-metaspace"></a>
**100. Что хранится в Metaspace и почему он может закончиться?** · middle
**Ориентир:** В native memory хранятся метаданные классов, а объём растёт с числом загруженных классов и loader'ов. `OutOfMemoryError: Metaspace` часто указывает на бесконечную генерацию классов или утечку ClassLoader, а не на обычную утечку объектов в heap.

<a id="q101-native-memory-tracking"></a>
**101. Как исследовать расход native memory JVM?** · senior
**Ориентир:** Native Memory Tracking вместе с `jcmd VM.native_memory` показывает категории зарезервированной и committed memory, если NMT был включён при старте. Данные JVM сопоставляют с RSS процесса, direct buffers, thread stacks и нативными библиотеками.

<a id="q102-jmm-reordering"></a>
**102. Какие переупорядочивания допускает Java Memory Model?** · senior
**Ориентир:** Компилятор, JIT и CPU могут менять порядок, если однопоточное поведение сохраняется и не нарушены отношения synchronization order/happens-before. В программе с data race другой поток может наблюдать порядок, которого не следует ожидать по исходному коду.

<a id="q103-safe-publication"></a>
**103. Какие способы безопасной публикации объекта вы знаете?** · middle
**Ориентир:** Публикацию обеспечивают, например, передача через правильно синхронизированную структуру, запись в `volatile`, освобождение monitor и статическая инициализация. Просто присвоить ссылку обычному общему полю недостаточно для видимости всего состояния.

<a id="q104-final-field-semantics"></a>
**104. Какие гарантии JMM даёт `final`-полям?** · senior
**Ориентир:** При корректном конструировании поток, получивший ссылку на объект, видит значения его `final`-полей, записанные в конструкторе, и достижимое через них состояние на момент завершения конструктора. Гарантия ломается, если `this` утекает до окончания конструктора, и не делает вложенные объекты неизменяемыми.

<a id="q105-this-escape"></a>
**105. Чем опасна утечка `this` из конструктора?** · middle
**Ориентир:** Другой код или поток может увидеть частично сконструированный объект до установки инвариантов и final-field freeze. Типичные причины — регистрация listener, запуск потока или вызов переопределяемого метода из конструктора.

<a id="q106-double-checked-locking"></a>
**106. Почему double-checked locking требует `volatile`?** · middle/senior
**Ориентир:** Без `volatile` публикация ссылки может наблюдаться до завершения инициализации объекта из-за допустимых reorderings. Volatile write/read создают требуемый happens-before, хотя initialization-on-demand holder часто проще.

<a id="q107-false-sharing"></a>
**107. Что такое false sharing?** · senior
**Ориентир:** Независимые часто изменяемые поля разных потоков могут попасть в одну cache line и вызывать постоянную инвалидацию кэшей. Подтверждают проблему профилированием и hardware counters, а layout/padding меняют только после измерений.

<a id="q108-varhandle-memory-order"></a>
**108. Какие режимы доступа предоставляет `VarHandle`?** · senior
**Ориентир:** Помимо plain и volatile доступны opaque и acquire/release режимы с разной силой ordering-гарантий, а также атомарные compare-and-set и update операции. Более слабый режим требует точного доказательства корректности и обычно встречается в библиотечном low-level коде.

## GC: сборщики, настройка и диагностика { #gc-tuning-diagnostics }

<a id="q109-generational-hypothesis"></a>
**109. На какой гипотезе основана generational collection?** · middle
**Ориентир:** Большинство объектов живёт недолго, поэтому young generation выгодно собирать чаще и дешевле, а пережившие объекты продвигать. Профиль конкретного приложения может отличаться, поэтому важны allocation rate и возраст объектов.

<a id="q110-gc-roots"></a>
**110. Какие категории GC roots важны при анализе утечки?** · middle
**Ориентир:** Среди корней — активные thread stacks, статические поля загруженных классов, JNI handles и внутренние ссылки JVM. В heap dump полезно искать путь от подозрительного объекта до root и retained size владельца графа.

<a id="q111-strong-soft-weak-phantom"></a>
**111. Чем отличаются strong, soft, weak и phantom references?** · middle/senior
**Ориентир:** Strong удерживает объект, weak допускает сборку при следующем подходящем GC, soft зависит от давления памяти, phantom используется с `ReferenceQueue` после определения phantom reachability. Soft references не дают предсказуемой политики кэширования, а finalization следует избегать.

<a id="q112-card-table-remembered-set"></a>
**112. Зачем сборщикам card table и remembered sets?** · senior
**Ориентир:** Они помогают находить ссылки между регионами или поколениями без полного сканирования heap. Write barriers обновляют эти структуры при присваиваниях, добавляя небольшой overhead к работе приложения.

<a id="q113-safepoint"></a>
**113. Что такое safepoint и почему пауза может быть длиннее работы GC?** · senior
**Ориентир:** В safepoint прикладные потоки находятся в состоянии, где JVM безопасно выполняет глобальную операцию. Время включает достижение safepoint всеми нужными потоками и саму VM operation, поэтому причину уточняют по safepoint/GC log и JFR.

<a id="q114-serial-parallel-g1"></a>
**114. Когда рассматривать Serial, Parallel и G1 GC?** · middle
**Ориентир:** Serial подходит небольшим heap и простым однопроцессорным сценариям, Parallel оптимизирует throughput, G1 балансирует throughput и предсказуемость пауз на региональном heap. Выбор проверяют на workload и SLO, а не по универсальному рейтингу.

<a id="q115-zgc-shenandoah"></a>
**115. Для каких задач рассматривают ZGC и Shenandoah?** · senior
**Ориентир:** Это low-latency collectors, выполняющие большую часть тяжёлой работы конкурентно с приложением и рассчитанные на короткие паузы при больших heap. Доступность, generational mode и детали настройки зависят от конкретной JDK/distribution, поэтому сверяются с её документацией.

<a id="q116-g1-regions"></a>
**116. Как региональная модель G1 влияет на сборку?** · senior
**Ориентир:** Heap делится на регионы, которые динамически играют роли Eden, Survivor, Old и Humongous; collector выбирает набор регионов для паузы. Это позволяет собирать наиболее выгодные регионы и планировать паузы, но цель паузы остаётся ориентиром, а не SLA.

<a id="q117-humongous-objects"></a>
**117. Почему humongous allocations важны для G1?** · senior
**Ориентир:** Объекты размером не менее половины региона занимают последовательность humongous-регионов и могут усиливать fragmentation и давление на GC. В логах и JFR проверяют их частоту, а затем уменьшают аллокации либо оценивают region size только по измерениям.

<a id="q118-concurrent-mode-failure"></a>
**118. Что означает, что concurrent collector не успевает за приложением?** · senior
**Ориентир:** Если concurrent cycle не освобождает память быстрее, чем mutators её заполняют, JVM может перейти к более дорогой stop-the-world сборке или получить allocation failure. Исследуют запас heap, allocation/promotion rate, старт цикла и доступные CPU.

<a id="q119-xms-xmx-containers"></a>
**119. Как выбирать `-Xms` и `-Xmx` в контейнере?** · middle/senior
**Ориентир:** Heap должен оставлять лимит для metaspace, code cache, thread stacks, direct/native memory и самого контейнера. Равные `Xms/Xmx` дают более стабильный heap, но резервируют бюджет; решение принимают по нагрузке и общему memory limit.

<a id="q120-gc-pause-goal"></a>
**120. Почему `MaxGCPauseMillis` не гарантирует максимальную паузу?** · middle
**Ориентир:** Это цель, которую collector использует в эвристиках, а не жёсткое ограничение. На паузы влияют live set, remembered sets, allocation spikes, CPU и другие VM operations.

<a id="q121-unified-gc-logging"></a>
**121. Что включить в GC logging и как читать результат?** · middle
**Ориентир:** Unified logging `-Xlog` позволяет записать события GC, heap changes, phases и safepoints с timestamps и ротацией. Смотрят не одну паузу, а тренды allocation rate, frequency, reclaimed memory, promotion и full/degenerate cycles.

<a id="q122-heap-dump-analysis"></a>
**122. Чем shallow size отличается от retained size в heap dump?** · middle
**Ориентир:** Shallow size — память самого объекта, retained size — память объектов, которые станут недостижимы вместе с ним. Dominator tree и пути до GC roots обычно полезнее простого списка самых многочисленных классов.

<a id="q123-allocation-profiling"></a>
**123. Когда allocation profiling полезнее heap dump?** · senior
**Ориентир:** Heap dump показывает преимущественно живое состояние в момент снимка, а allocation profiling — где и с какой скоростью создаются объекты, включая быстро умершие. Для высокой GC-нагрузки без роста live set JFR или async-profiler allocation обычно дают более прямой ответ.

<a id="q124-gc-tuning-process"></a>
**124. Как выглядит безопасный процесс GC tuning?** · senior
**Ориентир:** Сначала фиксируют SLO и baseline на репрезентативной нагрузке, затем меняют один параметр или collector и сравнивают latency, throughput, CPU и memory. Случайный набор flags без гипотезы усложняет обновление JDK и часто маскирует проблему приложения.

## Потоки, locks, atomics и async API { #concurrency-runtime }

<a id="q125-thread-states"></a>
**125. Чем состояния `BLOCKED`, `WAITING` и `TIMED_WAITING` отличаются в thread dump?** · junior/middle
**Ориентир:** `BLOCKED` означает ожидание monitor entry, `WAITING` — бессрочное ожидание другого события, `TIMED_WAITING` — ожидание с пределом времени. Состояние интерпретируют вместе со stack trace, владельцем lock и динамикой нескольких dump.

<a id="q126-interruption"></a>
**126. Как устроено прерывание потока и почему нельзя проглатывать `InterruptedException`?** · middle
**Ориентир:** `interrupt()` выставляет флаг и заставляет некоторые блокирующие методы завершиться с `InterruptedException`, часто очищая флаг. Если метод не может завершить работу, он обычно восстанавливает флаг через `Thread.currentThread().interrupt()` и передаёт управление выше.

<a id="q127-monitor-wait-notify"></a>
**127. Какие правила действуют для `wait`, `notify` и `notifyAll`?** · middle
**Ориентир:** Их вызывают, владея тем же monitor; `wait` освобождает monitor и должен находиться в цикле проверки условия из-за spurious wakeups. `notifyAll` безопаснее при нескольких логических условиях, хотя higher-level synchronizers обычно проще.

<a id="q128-reentrant-lock"></a>
**128. Когда `ReentrantLock` полезнее `synchronized`?** · middle
**Ориентир:** Он даёт interruptible/timed acquisition, несколько `Condition`, polling через `tryLock` и опциональную fairness. Lock обязательно освобождают в `finally`, а дополнительная гибкость оправдана только реальной потребностью.

<a id="q129-read-write-lock"></a>
**129. Когда `ReadWriteLock` может не дать выигрыша?** · senior
**Ориентир:** При коротких секциях, частых записях или умеренной конкуренции его coordination overhead может быть выше обычного lock. Выигрыш проверяют benchmark'ом на реальном соотношении чтений и записей.

<a id="q130-stamped-lock"></a>
**130. Как работает optimistic read у `StampedLock`?** · senior
**Ориентир:** Чтение получает stamp без блокировки, копирует данные и затем вызывает `validate`; при неуспехе повторяет чтение под read lock. `StampedLock` не reentrant, а optimistic read нельзя использовать без валидации согласованного snapshot.

<a id="q131-cas-aba"></a>
**131. Что такое CAS и проблема ABA?** · senior
**Ориентир:** Compare-and-set атомарно меняет значение, только если оно всё ещё равно ожидаемому. При ABA значение успело измениться и вернуться, поэтому одного сравнения недостаточно; применяют version stamp или структуру, где ABA безопасна по доказанному алгоритму.

<a id="q132-long-adder"></a>
**132. Когда `LongAdder` лучше `AtomicLong`?** · middle
**Ориентир:** При высокой конкуренции за счёт распределённых cells он лучше масштабирует частые инкременты. `sum()` не является атомарным snapshot относительно параллельных обновлений, поэтому для sequence или строгого счётчика выбирают `AtomicLong`.

<a id="q133-lock-free-wait-free"></a>
**133. Чем lock-free отличается от wait-free?** · senior
**Ориентир:** Lock-free гарантирует системный прогресс: хотя бы один поток завершает операцию; wait-free гарантирует завершение каждой операции за ограниченное число шагов. Наличие CAS ещё не доказывает ни одну из этих гарантий.

<a id="q134-concurrent-hash-map-atomicity"></a>
**134. Какие ограничения у атомарных методов `ConcurrentHashMap`?** · middle
**Ориентир:** `compute`, `merge` и `putIfAbsent` атомарны для соответствующего ключа, но не превращают операции над несколькими ключами в транзакцию. Mapping function должна быть короткой и не должна рекурсивно менять ту же map непредсказуемым образом.

<a id="q135-copy-on-write-array-list"></a>
**135. Для какой нагрузки подходит `CopyOnWriteArrayList`?** · middle
**Ориентир:** Для маленьких коллекций с очень частым чтением, редкими изменениями и snapshot-итерацией без locks. Каждая запись копирует массив, поэтому write-heavy сценарий создаёт CPU и allocation overhead.

<a id="q136-blocking-queues-backpressure"></a>
**136. Как bounded `BlockingQueue` помогает реализовать backpressure?** · middle
**Ориентир:** Ограниченная очередь заставляет producer ждать, отказывать или применять заданную политику, когда consumer не успевает. Размер очереди выбирают из допустимой задержки и burst, иначе большая очередь лишь скрывает перегрузку.

<a id="q137-synchronizers"></a>
**137. Когда применять `CountDownLatch`, `CyclicBarrier`, `Semaphore` и `Phaser`?** · middle
**Ориентир:** Latch ждёт одноразового завершения набора действий, barrier синхронизирует повторяемый этап фиксированных участников, semaphore ограничивает число одновременных разрешений, phaser поддерживает многофазность и динамических участников. Выбор должен отражать протокол, а не только возможность «подождать».

<a id="q138-thread-pool-sizing"></a>
**138. Как оценить размер пула для CPU-bound и blocking задач?** · middle/senior
**Ориентир:** CPU-bound пул обычно близок к числу доступных cores, а blocking workload допускает больше concurrency с учётом отношения ожидания к вычислению и лимитов downstream. Формула даёт стартовую гипотезу, которую проверяют latency, queue time, saturation и throughput.

<a id="q139-thread-pool-queue-rejection"></a>
**139. Как связаны размер пула, очередь и `RejectedExecutionHandler`?** · senior
**Ориентир:** У `ThreadPoolExecutor` новая задача сначала использует core threads, затем очередь, затем расширение до maximum, после чего срабатывает rejection policy. Неограниченная очередь фактически делает maximumPoolSize нерабочим для роста и переносит overload в задержку/память.

<a id="q140-executor-shutdown"></a>
**140. Как корректно завершить `ExecutorService`?** · junior/middle
**Ориентир:** Сначала вызывают `shutdown`, ограниченно ждут `awaitTermination`, затем при необходимости используют `shutdownNow` и сохраняют interrupt status. Задачи должны сами корректно реагировать на interrupt, иначе принудительное завершение не сработает.

<a id="q141-fork-join-work-stealing"></a>
**141. Как работает work stealing в `ForkJoinPool`?** · senior
**Ориентир:** Worker обычно берёт задачи из собственной deque, а при простое крадёт их у других workers, что хорошо для рекурсивного разбиения CPU-задач. Неконтролируемые blocking operations могут истощить параллелизм; для известных блокировок существует `ManagedBlocker`, но архитектуру всё равно надо оценивать.

<a id="q142-completable-future-executor"></a>
**142. В каком потоке выполняются этапы `CompletableFuture`?** · middle
**Ориентир:** Не-async continuation может выполниться потоком, который завершает предыдущий stage, а async-вариант без executor обычно использует common `ForkJoinPool`. Для blocking I/O и изоляции нагрузки executor лучше задавать явно.

<a id="q143-completable-future-errors"></a>
**143. Чем `handle`, `exceptionally` и `whenComplete` различаются?** · middle
**Ориентир:** `handle` преобразует и успех, и ошибку; `exceptionally` восстанавливается только после ошибки; `whenComplete` выполняет наблюдаемый side effect и обычно сохраняет исходный результат. Следует также понимать обёртки `CompletionException` и поведение ошибок callback.

<a id="q144-completable-future-cancellation"></a>
**144. Почему cancellation и timeout у `CompletableFuture` не гарантируют остановку работы?** · senior
**Ориентир:** Они могут завершить stage исключением, но underlying task или I/O продолжит выполняться, если его отдельно не отменить и он не поддерживает cooperative cancellation. Нужны timeouts на самом ресурсе, propagation сигнала и освобождение capacity.

<a id="q145-thread-local-leaks"></a>
**145. Почему `ThreadLocal` может утекать в thread pool?** · middle
**Ориентир:** Долгоживущий worker удерживает значения между задачами, даже если логический request завершён; ключи в `ThreadLocalMap` слабые, а значения остаются сильными до очистки. Используйте `remove()` в `finally` и предпочитайте явную передачу контекста.

<a id="q146-concurrency-diagnostics"></a>
**146. Как диагностировать deadlock, starvation и lock contention?** · senior
**Ориентир:** Снимают несколько thread dumps/JFR, ищут циклы владения locks, долго ожидающие потоки, hot monitors и распределение parked/blocked time. Deadlock — цикл ожидания, starvation — систематическая нехватка доступа к ресурсу, contention — конкуренция, которая может быть высокой и без взаимной блокировки.

## Virtual threads и structured concurrency { #virtual-threads-structured-concurrency }

<a id="q147-virtual-thread-status"></a>
**147. Каков статус virtual threads в Java 25?** · junior/middle
**Ориентир:** Virtual threads — финальная стандартная возможность платформы с Java 21 (JEP 444), поэтому в Java 25 для них не нужен `--enable-preview`. Они реализуют `Thread` API и предназначены прежде всего для большого числа блокирующих задач.

<a id="q148-virtual-carrier-mounting"></a>
**148. Что означают mounting и unmounting virtual thread?** · middle
**Ориентир:** JVM монтирует virtual thread на platform carrier для выполнения и обычно размонтирует его при поддерживаемой блокировке, освобождая carrier. Связь не постоянна: нельзя полагаться на identity или `ThreadLocal` carrier-потока.

<a id="q149-virtual-thread-pinning"></a>
**149. Что такое pinning virtual thread в Java 25?** · middle/senior
**Ориентир:** Virtual thread остаётся смонтированным при некоторых операциях, которые JVM не может размонтировать; длительный pinning снижает scalability. Начиная с JDK 24 блокировка внутри `synchronized` больше не pin'ит virtual thread (JEP 491), но native/foreign вызовы и другие случаи всё ещё требуют измерения через JFR.

<a id="q150-no-virtual-thread-pooling"></a>
**150. Почему virtual threads обычно не объединяют в пул?** · middle
**Ориентир:** Они дешёвы и рассчитаны на модель «новый поток на задачу», а pooling теряет простоту и может искусственно ограничивать concurrency. Дефицитный ресурс ограничивают отдельно через semaphore, connection pool или rate limiter.

<a id="q151-virtual-thread-threadlocal"></a>
**151. Какие риски создаёт массовое использование `ThreadLocal` с virtual threads?** · senior
**Ориентир:** Значение хранится для каждого virtual thread, поэтому дорогой объект на сотнях тысяч потоков расходует много памяти и усложняет наследование контекста. В Java 25 финальные Scoped Values (JEP 506) дают неизменяемую ограниченную областью альтернативу для передачи контекста.

<a id="q152-structured-concurrency-status"></a>
**152. Каков точный статус structured concurrency в Java 25?** · middle/senior
**Ориентир:** Structured Concurrency в JDK 25 — пятая preview-версия API по JEP 505, а не финальная возможность; для компиляции и запуска нужен `--enable-preview` вместе с release/runtime 25. API может измениться в следующем выпуске, что нужно учитывать для production-кода и библиотек.

<a id="q153-structured-task-scope"></a>
**153. Какую проблему решает `StructuredTaskScope`?** · senior
**Ориентир:** Он связывает lifetime дочерних concurrent-задач с лексической областью родителя, упрощая join, отмену, обработку ошибок и наблюдаемость. Выход из области не должен оставлять бесконтрольно работающие дочерние задачи.

<a id="q154-structured-joiner-policy"></a>
**154. Как выбирать политику завершения structured task scope?** · senior
**Ориентир:** Политика должна следовать бизнес-смыслу: ждать все результаты, завершаться при первой успешной задаче или отменять siblings при первой ошибке. В preview API Java 25 поведение задаётся через `Joiner`, поэтому отдельно продумывают частичные результаты, deadline и cleanup.

## Performance и профилирование { #performance-profiling }

<a id="q155-jmh"></a>
**155. Почему Java microbenchmark следует писать на JMH?** · middle
**Ориентир:** JMH учитывает warmup, forks, dead-code elimination, constant folding и способы потребления результата, которые легко искажают ручной benchmark. Даже JMH измеряет микросценарий, поэтому его выводы нужно связать с production profile.

<a id="q156-jit-tiered-compilation"></a>
**156. Как tiered compilation и deoptimization влияют на измерения?** · senior
**Ориентир:** JVM сначала исполняет/компилирует код на более быстрых уровнях, собирает профиль и затем оптимизирует горячие методы; неверные speculative assumptions вызывают deoptimization. Поэтому короткий тест без прогрева часто измеряет startup и компиляцию, а не steady state.

<a id="q157-cpu-profiling"></a>
**157. Чем sampling profiler отличается от instrumentation profiler?** · middle
**Ориентир:** Sampling периодически снимает stacks и обычно имеет меньший overhead, но может пропустить короткие события; instrumentation учитывает вызовы точнее, но сильнее меняет выполнение. Выбор зависит от вопроса, допустимого overhead и среды.

<a id="q158-jfr"></a>
**158. Что можно исследовать с помощью Java Flight Recorder?** · middle
**Ориентир:** JFR пишет низконакладные события CPU sampling, allocations, GC, locks, threads, I/O и пользовательские события для последующего анализа. Профиль записи, длительность и включённые события выбирают под гипотезу, чтобы контролировать overhead и объём.

<a id="q159-coordinated-omission"></a>
**159. Что такое coordinated omission в нагрузочном тесте?** · senior
**Ориентир:** Генератор, ожидающий завершения запроса перед следующим, снижает фактическую подачу нагрузки во время паузы и занижает хвостовые задержки. Нужны модель поступления запросов, сохраняющая заданный rate, и отчёт по полному latency distribution.

<a id="q160-production-performance-process"></a>
**160. Как системно искать performance bottleneck Java-сервиса?** · senior
**Ориентир:** Сначала фиксируют симптом и SLO, коррелируют latency/throughput/errors с CPU, memory, GC, locks, I/O и downstream, затем профилируют репрезентативный интервал. Меняют одну доказанную причину, повторяют тот же тест и сравнивают профиль и пользовательскую метрику.

## Официальные источники { #official-sources }

- [The Java Virtual Machine Specification, Java SE 25](https://docs.oracle.com/javase/specs/jvms/se25/html/)
- [The Java Language Specification, Chapter 17: Threads and Locks](https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html)
- [Java SE 25 API: `java.lang.invoke.VarHandle`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/invoke/VarHandle.html)
- [Java SE 25 API: `java.util.concurrent`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/package-summary.html)
- [Java SE 25 troubleshooting guide: Java Flight Recorder](https://docs.oracle.com/en/java/javase/25/troubleshoot/troubleshoot-performance-issues-using-jfr.html)
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [JEP 491: Synchronize Virtual Threads without Pinning](https://openjdk.org/jeps/491)
- [JEP 505: Structured Concurrency (Fifth Preview)](https://openjdk.org/jeps/505)
- [JEP 506: Scoped Values](https://openjdk.org/jeps/506)
- [JDK 25 Garbage Collection Tuning Guide](https://docs.oracle.com/en/java/javase/25/gctuning/)
- [JMH — OpenJDK Microbenchmark Harness](https://openjdk.org/projects/code-tools/jmh/)

