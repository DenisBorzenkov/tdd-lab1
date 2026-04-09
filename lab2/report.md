# Отчёт по лабораторной работе 2

## Практика 1 — GET-запросы через Postman

Тестирование API Звёздных войн (https://swapi.dev/) с помощью Postman.

### 1.1. species — name=droid, average_lifespan=?

**Ответ:** `average_lifespan = "indefinite"`

![species droid](p1_collection_species_droid.png)

### 1.2. starships — name=Millennium Falcon, crew=?

**Ответ:** `crew = "4"`

![starships Millennium Falcon](p1_collection_starships_millennium_falcon.png)

### 1.3. people — name=Darth Vader, eye_color=?

**Ответ:** `eye_color = "yellow"`

![people Darth Vader](p1_collection_people_darth_vader.png)

### 1.4. planets — name=Naboo, terrain=?

**Ответ:** `terrain = "grassy hills, swamps, forests, mountains"`

![planets Naboo](p1_collection_planets_naboo.png)

---

## Практика 2 — Получение по id и команда cURL

### 2.1. Фильм с id=5 — название и дата выхода

![film id=5](p2_film_id5.png)

### 2.2. curl-запрос на получение starship с id=3

Запрос в Postman:

![starship id=3 Postman](p2_starship_id3_postman.png)

Выполнение curl-запроса в терминале (команда + вывод):

![curl starship id=3 terminal](p2_curl_starship_id3_terminal.png)

---

## Практика 3 — Поиск через ?search=

### 3.1. Поиск космического корабля Star Destroyer через ?search=

На скриншоте видны: метод (GET), адрес, параметры запроса (search=Star Destroyer), статус-код (200 OK) и body ответа.

![search Star Destroyer](p3_search_star_destroyer.png)

---

## Практика 4 — Postman Console

### 4.1. Вывод кода ответа в консоль через console.log()

Скрипт с console.log для вывода кода ответа:

![console.log script](p4_console_log_script.png)

Результат выполнения скрипта:

![console.log output](p4_console_log_output.png)

---

## Практика 5 — Insomnia

Тестирование swapi (people) с помощью Insomnia.

### 5.1. Получение данных по людям по id

Сначала запрос GET на https://swapi.dev/api/people/?search=C-3PO для определения id:

![Insomnia search C-3PO](p5_insomnia_search_c3po.png)

Затем запрос GET на https://swapi.dev/api/people/2/ (C-3PO имеет id=2):

![Insomnia people id=2](p5_insomnia_people_id2.png)

### 5.2. Ошибка 405 Method Not Allowed

Отправка запроса неправильным методом (DELETE) для получения ошибки 405:

![Insomnia 405 error](p5_insomnia_405_error.png)

### 5.3. Ошибка 404 Not Found

Отправка запроса на несуществующий ресурс для получения ошибки 404:

![Insomnia 404 error](p5_insomnia_404_error.png)

---

## Практика 6 — Swagger

### 6.1. Swagger Editor

![Swagger Editor](p6_swagger_editor.png)

### 6.2. Swagger Petstore — добавление питомца

![Petstore add pet](p6_petstore_add_pet.png)

### 6.3. Swagger Petstore — получение питомца по id

![Petstore get pet by id](p6_petstore_get_pet_by_id.png)
