# Принципы повторного использования модуля

В данном занятии нам необходимо перечислить принципы, которые необходимо соблюдать при добавлении нового модуля в проект, вот следующие принципы, которые мы также оценим в реализации на Go:

1. Новый модуль может задавать обобщенные типы

Нет, достичь этого нельзя на уровне пакета.

2. Новый модуль может объединять несколько функций

Да, в Go это можно сделать:

```go
package order

type Order struct {
    Items    []Item
    Discount float64
}

func (o *Order) Calculate() float64 {
    subtotal := o.subtotal()         // вызывает внутренний метод
    return o.applyDiscount(subtotal) // вызывает другой внутренний метод
}

func (o *Order) subtotal() float64 {
    total := 0.0
    for _, item := range o.Items {
        total += item.Price
    }
    return total
}

func (o *Order) applyDiscount(amount float64) float64 {
    return amount * (1 - o.Discount)
}
```


3. Новый модуль может входить в семейство модулей

Да, может, только могут возникнуть циклические зависимости, что компилятор не пропустит

```go
// модуль чтения
package reader

type FileReader struct{}
func (r *FileReader) Read(path string) []byte { ... }

// модуль обработки
package processor

type DataProcessor struct{}
func (p *DataProcessor) Process(data []byte) Result { ... }

// модуль записи
package writer

type FileWriter struct{}
func (w *FileWriter) Write(path string, result Result) { ... }
```

```go
// семейство модулей
package notebook

import (
	"reader"
	"writer"
	"processor"
)

type NoteBook struct {
	// ...
}

func New(r reader.Reader, w writer.Writer, pr processor.Processor) *NoteBook {
	return &NoteBook {
		// ...
	}
}
```

4. Новый модуль может предлагать конкретную реализацию родительского модуля, которая должна выбираться динамически, например, реализация обобщённого типа для конкретного типа-параметра

Нет, так как реализацию через имплементацию интерфейса выбирает сам разработчик, а не пакет. Также возникает конфликт между 1 и 4 принципами, так как в первом необходимо сделать пакет, который описывает обобщенные типы, а пункт 4 требует конкретную реализацию, то есть мы нарушаем принцип OCP, где пакет из первого пункта, который является закрытым для модификации, требует модификации.

5. Новый модуль может интегрировать общее поведение нескольких модулей, которые различаются лишь деталями

Да, может, через импортирование интерфейса.

Пакеты `consolelogger` и `filelogger` различаются только деталями реализации. Пакет `app` интегрирует их через общий контракт:

```go
// пакет logger — общий контракт
package logger

type Logger interface {
    Log(message string)
}
```

```go
// пакет consolelogger
package consolelogger

type Logger struct{}

func (l *Logger) Log(message string) {
    fmt.Println(message)
}
```

```go
// пакет filelogger
package filelogger

type Logger struct{ Path string }

func (l *Logger) Log(message string) {
    // пишет в файл
}
```

```go
// пакет app интегрирует — ему всё равно какой логгер
package app

import "myapp/logger"

type App struct {
    logger logger.Logger
}

func (a *App) Run() {
    a.logger.Log("запуск")
}
```

Также в ООП есть переопределение и перегрузка, но они доступны не всем ЯП, а также не совсем хорошо читаются.

## Почему все пять принципов недостижимы одновременно
---

На практике, всех принципов придерживаться не получается, но необходимо стремиться реализовывать максимум.

**Стандартные библиотеки** подходят только для простых проектов с чёткими разграничениями. В лучшем случае выполняются принципы 2, 3 и 5.

**Пакеты с публичным интерфейсом** — абстрактные модули без реализации. Но принцип 4 нарушается: конкретную реализацию выбирает сам программист, а не механизм языка.

**Перегрузка имён** частично решает задачу, но плохо читаема, не поддерживает дженерики, и главное — если функции различаются семантически, это различие должно быть видно на уровне синтаксиса. Перегрузка этого не обеспечивает.

**Дженерики** — самое острое противоречие. Параметризованный пакет универсален и открыт для использования с любым типом. Но расширить его под конкретный тип без изменения уже использующего его кода не получается:

```go
// хочу специальную логику для Stack[Order] — например, лимит очереди
// варианты:
// 1. менять пакет collection — нарушаю OCP
// 2. писать отдельный пакет orderqueue — теряю смысл универсальности
// 3. оборачивать — лишний слой без реального расширения
```

Дженерик-пакет открыт и универсален, но его конкретные реализации закрыты — поддержка параметризации встроена в язык, и программист не управляет этим выбором динамически. Это прямое нарушение принципа открытости-закрытости: непонятно, как расширять такие шаблоны, не затрагивая уже использующий их код.

### Рефлексия
---

Проанализировав эталонное решение понял, что я хорошо описал возможности языка Go по реализации 5 принципов.

Вот пример внедрения новых модулей в проект при соблюдении максимального количества принципов:

```go
// пакет payment — принцип 2 (тесно связанные функции)
package payment

type Payment struct {
    Amount   float64
    Currency string
    UserID   string
}

func (p *Payment) Process() error {
    if err := p.validate(); err != nil {  // внутренняя функция
        return err
    }
    if err := p.convert(); err != nil {   // внутренняя функция
        return err
    }
    return p.execute()                    // внутренняя функция
}

func (p *Payment) validate() error { ... }
func (p *Payment) convert() error { ... }
func (p *Payment) execute() error { ... }
```

```go
// пакет gateway — принцип 3 (семейство модулей)
package gateway

import "myapp/payment"

type Gateway interface {
    Send(p payment.Payment) error
}
```

```go
// пакет mir — конкретная реализация
package mir

type Gateway struct{ APIKey string }

func (g *Gateway) Send(p payment.Payment) error { ... }
```

```go
// пакет visa — ещё одна реализация
package visa

type Gateway struct{ APIKey string }

func (g *Gateway) Send(p payment.Payment) error { ... }
```

```go
// пакет service — принцип 5 (интеграция общего поведения)
package service

import (
    "myapp/gateway"
    "myapp/payment"
)

type PaymentService struct {
    gateway gateway.Gateway  // не знает какая реализация
}

func (s *PaymentService) Execute(p payment.Payment) error {
    return s.gateway.Send(p)
}
```