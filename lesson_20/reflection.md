# Классификация категорий наследования - 2

Продолжаем изучать категории наследования [прошлая часть](https://github.com/aaboyarchukov/OOAP_2/blob/main/lesson_19/reflection.md)

### Категории наследования
---

4. **Наследование вариаций** (переопределение методов: либо сигнатуру, либо логику)
5. **Конкретезированное** (родитель является абстрктным или частично абстрактным классом, дети конкретизируют методы)
6. **Структурное** (мы обогащаем наследуемый тип каким-то свойством, например, List -> OrderList(List, Comparable), обычно это свойство добавляется с помощью интерфейса)

### Примеры
---
**Наследование вариаций:**

Базовый класс "животное", у которого есть метод - издает звук, есть наследники: "кошка" и "собака", метод остается тем же - логика переопределяется.

Есть базовый класс "соединение с БД", есть наследник, который переопределяет сигнатуру метода опреленным конфигом, например, для postgres.

**Наследование конкретизация:**

Есть абстрактный класс Iterable, и есть наследники List, Tree, которые реализуют по собственному обход своей структуры.

**Наследование структурное:**

Есть базовый класс "Word", который содержит буфер с данными, мы бы хотели выводить его на рахных языках, для этого у нас реализован интерфейс "LanguageConverter", с которым мы делаем наследника "WordConverter"

### Рефлексия
---
Эталонное решение:

**Java**

Наследование вариаций: иерархия "обычная газовая плита GasStove - газовая плита с электоподжигом ElectricGasStove", так как процесс её зажигания не требует спичек.

```java
class GasStove {
    private boolean isGasTurnedOn;
    private boolean isGasFired;

    public void turnOn(Match match) {
        match.setFired();
        turnOnGas();
        isGasFired = true;
    }

    protected void turnOnGas() {
        isGasTurnedOn = true;
    }
}

class ElectricGasStove extends GasStove {
    //@Override
    public void turnOn() {
        turnOnGas();
        turnOnElectricIgnition();
    }

    private void turnOnElectricIgnition() {

    }
}
```

Наследование с функциональной вариацией: иерархия классов HttpRequest и HttpsRequest. HTTPS-запрос помимо перадачи данных требует предварительно создать ключ сессии, которым шифруются данныею

```java
class HttpRequest {
    void doRequest(String body, Map<String, String> headers, String url) {
        dataInterchange(body, headers, url);
    }

    protected void dataInterchange(String body, Map<String, String> headers, String url) {
        System.out.println("");
    }
}

class HttpsRequest extends HttpRequest {
    protected String secretKey;

    @Override
    void doRequest(String body, Map<String, String> headers, String url) {
        handshake(url);
        var encryptedBody = encrypt(body, this.secretKey);
        super.doRequest(encryptedBody, headers, url);
    }

    private void handshake(String url) {
        var certificate = getServerCertificate(url);

        var canTrust = checkCertificateInCertificateAuthority(certificate);
        if (canTrust) {
            var publicKey = getPublicKeyFromCertificate(certificate);
            this.secretKey = createSecretKey();
            var encryptedSecretKey = encrypt(secretKey, publicKey);
            super.dataInterchange(encryptedSecretKey, null, url);
        }
    }

    private String createSecretKey() {
        return String.valueOf(ThreadLocalRandom.current().nextInt(0, Integer.MAX_VALUE));
    }

    private String encrypt(String text, String key) {
        return text; // ... дополнительные действия
    }

    private String getPublicKeyFromCertificate(String certificate) {
        return certificate.substring(0, 10);
    }

    private String getServerCertificate(String url) {
        // заглушка
        return "some certificate";
    }

    private boolean checkCertificateInCertificateAuthority(String certificate) {
        // более сложная логика
        return true;
    }
}
```

Структурное наследование: наследование класса от интерфейса Summable, который добавляет классу "возможность" суммирования. Это полезно при работе с разными математическими понятиями, поддерживающими операцию суммирования -- например для скаляров (MyInt) и векторов (Vector).

```java
enum OperationResult {
    SUCCESS,
    FAILURE
}

abstract class Summable extends Any {
    abstract void sum(Summable number);
    abstract int getLength();
    abstract OperationResult getSumOperationResult();
    abstract List<Summable> getValues();
}

class MyInt extends Summable {
    private OperationResult addOperationResult;

    int value;

    public MyInt(int value) {
        this.value = value;
    }

    @Override
    void sum(Summable number) {
        if (number.getLength() != this.getLength()) {
            return ;
        }

        MyInt myInt = new MyInt(0);
        myInt = Any.assignmentAttempt(number, myInt);
        if (myInt == null) {
            addOperationResult = OperationResult.FAILURE;
            return;
        }

        this.value += myInt.value;
        addOperationResult = OperationResult.SUCCESS;
    }

    @Override
    int getLength() {
        return 1;
    }

    @Override
    OperationResult getSumOperationResult() {
        return this.addOperationResult;
    }

    @Override
    List<Summable> getValues() {
        var list = new ArrayList<Summable>();
        list.add(new MyInt(this.value));
        return list;
    }
}
```

**Python**

```python
# 3. Structure inheritance
class SimpleResponse(TypedDict):
    content: bytes
    content_length: int
    status: HTTPStatus

class BaseAPI:
    def __init__(self, url: str):
        self.url = self.validate(url)

    def upload_content(self, content: bytes) -> SimpleResponse:
        response = ...
        return response

    def validate(self, url: str) -> str:
        raise NotImplementedError

class BaseView:
    ...

    def has_view_permission(self, request, user=None) -> bool:
        return True

class SecretView(BaseView):
    ...

    # 1.1. Functional variation inheritance
    def has_view_permission(self, request, user=None) -> bool:
        if user and user.is_admin:
            return True
        else:
            return False

class FileAPI(BaseAPI):
    # 1.2. Type variation inheritance
    @overload
    def upload_content(self, content: Union[str, Path]) -> SimpleResponse: ...

    def upload_content(self, content) -> SimpleResponse:
        with open(str(content), mode='rb') as file_obj:
            content = file_obj.read()
        response = super().upload_content(content)
        return response

    # 2. Reification inheritance
    def validate(self, url: str) -> str:
        valid_url = ...
        return valid_url
```

Проанализировав эталонное решение понял, что невнимательно прочел задание, исправляюсь:

**Наследование вариаций:**

Базовый класс "животное", у которого есть метод - издает звук, есть наследники: "кошка" и "собака", метод остается тем же - логика переопределяется.

```python
class Animal:
	def sound(self):
		print("sound")

class Cat(Animal):
	def sound(self):
		print("мяу")

class Dog(Animal):
	def sound(self):
		print("гав")
```

Есть базовый класс "соединение с БД", есть наследник, который переопределяет сигнатуру метода опреленным конфигом, например, для postgres.

```python
class DBConnect:
	def connect(self) -> conn:
		...

class PostgresConn(DBConnect):
	def connect(self, pg_config) -> conn:
		...
```


**Наследование конкретизация:**

Есть абстрактный класс Iterable, и есть наследники List, Tree, которые реализуют по собственному обход своей структуры.

```python
class Iterable:
	def move(self): ...
	
class List(Iterable):
	def move(self): ...
	
class Tree(Iterable):
	def move(self): ...
```

**Наследование структурное:**

Есть базовый класс "Word", который содержит буфер с данными, мы бы хотели выводить его на рахных языках, для этого у нас реализован интерфейс "LanguageConverter", с которым мы делаем наследника "WordConverter"s

```python
class LanguageConverter:
	def convert(self, from_lang, to_lang):
		...
		
class Word:
	def __init__(self, buffer):
		self.buffer = buffer

class WordConverter(Word, LanguageConverter):
	...
```