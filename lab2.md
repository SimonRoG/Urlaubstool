# Практична робота №2

**Виконали:** ІП-з31 Семен Прохода, Арсен Потеряйко

**Тема:** Формування та документація технічних рішень додатку. (System/Software design)

**Мета:** Навчитись формувати та документувати базові технічні рішення з архітектури додатку, зокрема, основні компоненти (сервіси), зв’язки між компонентами, дизайн API.

## Завдання:

### 1. Нефункціональні вимоги

| Атрибут         | Source    | Stimulus                  | Artifact         | Environment      | Response               | Measure                |
| --------------- | --------- | ------------------------- | ---------------- | ---------------- | ---------------------- | ---------------------- |
| **Performance**     | User      | Запит на створення заявки | API              | Робочий час      | Обробка запиту         | ≤ 2 с                  |
| **Security**        | Attacker  | Спроба несанкц. доступу   | Дані користувача | Будь-коли        | Блокування і логування | Жодного витоку даних   |
| **Modifiability**   | Developer | Зміна в API               | Код              | Під час розробки | Зміни ізоляовані       | ≤ 3 файли              |
| **Reliability**     | User      | Повторний запит           | Сховище заявок   | Нормальний режим | Один запис створюється | Жодних дублів          |
| **Availability**    | User      | Запит до системи          | API/Web          | Робочий час      | Доступна відповідь     | ≥ 99.9% uptime         |
| **Usability**       | New user  | Перше використання        | UI               | Браузер          | Успішне подання заявки | ≤ 2 хв, без помилок    |
| **Testability**     | Tester    | Запуск автотестів         | Кодова база      | CI/CD            | Тести проходять        | ≥ 80% покриття, ≤ 2 хв |
| **Maintainability** | Developer | Баг-репорт                | Код              | Робочий час      | Виправлення ізоляоване | ≤ 1 година             |

### 2. Архітектура системи та архітектурні рішення

```mermaid
graph TD
    UserEmployee["Employee"]
    UserManager["Manager"]
    UserAdmin["Admin"]
    WebApp["Urlaubstool"]

    UserEmployee -->|Submit/view requests| WebApp
    UserManager -->|Manage requests| WebApp
    UserAdmin -->|Manage users & roles| WebApp
```

```mermaid
graph TD
    subgraph "Urlaubstool"
        Frontend["HTML/CSS/JS"]
        Backend["FastAPI"]
        Database[("MySQL")]
        Docs["Swagger"]
    end

    User["User"] --> Frontend
    Frontend --> Backend
    Backend <--> Database
    Backend --> Docs
```

### 3. API design guidelines

1. **Протокол:** HTTP
2. **Формат:** JSON
3. **Організація ресурсів:**
    - GET `/users/`
    - POST `/users/`
    - GET, PUT, DELETE `/users/{id}`
    - GET `/requests/`
    - POST `/requests/`
    - GET, PUT, DELETE `/requests/{id}`
4. **Правила іменування:** snake_case
5. **Версіонування:** `/v1/`
6. **Методи HTTP:**
    - GET
    - POST
    - PUT
    - DELETE
7. 
8. **HTTP статуси:**
    - 200 OK
    - 404 Not Found
    - 422 Validation Error
    - 403 Forbidden
    

### 4. Дизайн API у вигляді Open API

![OpenApi!](/static/Pics/API.png)