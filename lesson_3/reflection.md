# Класс как модуль и класс как тип

В данном занятии необходимо описать, как в выбранном ЯП устроены классы как модули.

Вообще классы могут представляться в двух видах:
1. Модуль - синтаксическая единица проекта
2. Тип - семантическая единица проекта

Наследование в каждом из двух вариантов играет совершенно разные роли!

Сейчас рассмотрим первый тип.

---

### Класс как модуль
---

В этом случае наследование больше выступает в роли переиспользования, реализуя паттерн DRY. С пмощью модулей, можно внедрять зависимости в другие "классы", переиспользовать их функционал, разрабатывая программы различной сложности.

> **Создавая новый модуль, мы опираемся на уже существующий модуль, из которого заимствуем существенную часть базовой функциональности, и дополняем его новой**


### Golang
---

В выбранном мною ЯП работа разработанной программы напрямую зависит от того, как именно ты импортируешь [^1]"классы" и внедряешь зависимости между собой.

Основной единицей управления [^1]"классами" зависимостей является пакет - ключевое слово `package`.

Например:

```go
// Основной пакет main
package main

import (
	"context"
	"os/signal"
	"syscall"

	"git.dip.pics/dip/platform/go/logger.git"

	"git.dip.pics/dip/a7_account/be-stories.git/internal/app"
	"git.dip.pics/dip/a7_account/be-stories.git/internal/config"
	"git.dip.pics/dip/a7_account/be-stories.git/internal/utils"
)

// Переменные, в которые парсятся значения из -ldflags
var (
	version = "unknown"
	commit  = "unknown"
	date    = "unknown"
)

func main() {
	if err := utils.InitEnv(); err != nil {
		panic("utils.InitEnv:" + err.Error())
	}

	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	cfg, err := config.Parse()
	if err != nil {
		panic("parse config:" + err.Error())
	}

	logger.Init(loggerOptions()...)
	defer logger.Close()

	logger.Info("starting be-stories").
		String("version", version).
		String("commit", commit).
		String("date", date).
		String("environment", utils.Env()).
		Send()

	application, err := app.New(ctx, cfg)
	if err != nil {
		logger.Fatal("app initialization").Err(err).Send()
	}

	go application.Run(ctx)

	<-ctx.Done()
	logger.Info("received shutdown signal").Send()

	application.Shutdown()
}

func loggerOptions() []logger.Option {
	opts := []logger.Option{
		logger.WithCaller(true),
		logger.WithFields(map[string]any{
			"app":     "be-stories",
			"version": version,
		}),
		logger.WithContextFields(logger.RequestIDKey),
	}

	if utils.IsLocal() {
		opts = append(opts, logger.Pretty(), logger.WithLevel(logger.DebugLevel))
	}

	return opts
}

```

В основом пакете используются другие пакеты, из основных `logger` - корпоративаня библиотека  и `app` - внутренний пакет

```go
// пакет app
package app

import (
	"context"
	"fmt"
	"sync"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"

	"git.dip.pics/dip/a7_account/be-stories.git/internal/config"
	"git.dip.pics/dip/a7_account/be-stories.git/internal/delivery/http/stories"
	"git.dip.pics/dip/go/infrastructure.git/connections/minio"
	"git.dip.pics/dip/go/infrastructure.git/connections/postgres"

	"git.dip.pics/dip/platform/go/logger.git"

	handler "git.dip.pics/dip/a7_account/be-stories.git/internal/delivery/http"
	api "git.dip.pics/dip/a7_account/be-stories.git/internal/gen/ogen"
	feed_repo "git.dip.pics/dip/a7_account/be-stories.git/internal/repository/postgres/feed"
	splash_repo "git.dip.pics/dip/a7_account/be-stories.git/internal/repository/postgres/splash"
	feed_service "git.dip.pics/dip/a7_account/be-stories.git/internal/service/feed"
	splash_service "git.dip.pics/dip/a7_account/be-stories.git/internal/service/splash"
)

type App struct {
	cfg    *config.App
	server *server
	pgPool *pgxpool.Pool
}

func New(ctx context.Context, cfg *config.App) (*App, error) {
	pool, err := postgres.New(ctx, cfg.Postgres)
	if err != nil {
		return nil, fmt.Errorf("postgres.New: %w", err)
	}

	_, err = minio.NewClient(ctx, cfg.Minio)
	if err != nil {
		return nil, fmt.Errorf("minio.NewClient: %w", err)
	}

	feedRepo := feed_repo.NewFeedRepo(pool)
	feedService := feed_service.NewFeed(feedRepo)

	splashRepo := splash_repo.New(pool)
	splashService := splash_service.New(splashRepo)

	h := handler.New(
		stories.New(splashService, feedService),
	)

	sec := &handler.SecurityHandler{}

	ogenServer, err := api.NewServer(h, sec, api.WithMiddleware(handler.RequestIDMiddleware()))
	if err != nil {
		return nil, fmt.Errorf("ogen.NewServer: %w", err)
	}

	return &App{
		cfg:    cfg,
		server: newServer(cfg.HTTPServer, ogenServer),
		pgPool: pool,
	}, nil
}

func (a *App) Run(ctx context.Context) {
	a.server.Run(ctx)
}

func (a *App) Shutdown() {
	logger.Info("shutting down server").Send()

	a.server.SetNotReady()
	time.Sleep(a.cfg.DrainDelay)

	shutdownCtx, cancel := context.WithTimeout(context.Background(), a.cfg.ShutdownTimeout)
	defer cancel()

	var wg sync.WaitGroup

	wg.Go(func() {
		if err := a.server.Shutdown(shutdownCtx); err != nil {
			logger.Error("http server shutdown").Err(err).Send()
		}
	})

	wg.Wait()

	a.pgPool.Close()

	logger.Info("server stopped gracefully").Send()
}

```

В нем же используются другие [^1]"классы", которые формируют функциональность нашего приложения.

Но чтобы следить за наличием используемых пакетов, их версиями и импортами, есть два других служеюных файла:

1. `go.mod` - файл, в котором хранятся все используемые [^1]"классы"

```go
module some_module.git

go 1.25.6

require (
	internal_lib/infrastructure.git v1.2.6
	internal_lib/logger.git v0.0.3
	github.com/go-faster/errors v0.7.1
	github.com/go-faster/jx v1.2.0
	github.com/go-playground/validator/v10 v10.30.1
	// ...
)
```

2. `go.sum` - файл, который хранит хеши - состояния программы с импортируемыми классами, для быстрой проверки.

```go
dario.cat/mergo v1.0.2 h1:85+piFYR1tMbRrLcDwR18y4UKJ3aH1Tbzi24VRW1TK8=
dario.cat/mergo v1.0.2/go.mod h1:E/hbnu0NxMFBjpMIE34DRGLWqDy0g5FuKDhCb31ngxA=
internal_lib/infrastructure.git v1.2.6 h1:ReBjctZWgYlZ4vk0ZNQs6Qj7CUmrYShhkqH9kvNV9AI=
internal_lib/infrastructure.git v1.2.6/go.mod h1:VlSbBfGMAWrr/ziXvMy10lqTRcbdh1DbGMPkLNTzpBE=
```

Для использования [^1]"класса" достаточно импортировать его, написав путь в директиве `import` и нам становятся доступны все публичные методы и атрибуты [^1]"класса".

```go
import (
	"some_package/app"
)

func main() {
	app.New()
	// ...
}
```

[^1]: В данном уроке под словом "класс" подразумевается - пространство имен, сборки, пакеты, библиотеки -- все что содержит готовый код и что можно импортировать в свою программу.

### Рефлексия

---

Проанализировав примеры решения задания, понял, что справился хорошо, и максимально подробно представил организацию [^1]"классов" в Golang.