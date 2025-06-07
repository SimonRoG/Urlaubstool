# Практична робота №4

**Виконали:** ІП-з31 Семен Прохода, Арсен Потеряйко

**Тема:** Event-driven архітектура.

**Мета:** Застосувати event-driven для проектування складних систем.

## Завдання:

### 1. Вкажіть use cases у вашій системі, які потребують event-driven архітектури.

- Після зміни статусу заявки на відпустку - відправлення повідомлень (NotificationService).

- Логування подій авторизації (AuditService) після успішного чи неуспішного логіну (AuthService).

- Надсилання подій для аналітики (AnalyticsService) після створення, оновлення, видалення заявок чи користувачів.

- Синхронізація між сервісами через асинхронні події при зміні даних користувачів, заявок.

- Генерація звітів або оновлення статистики на основі подій у системі.

### 2. Вкажіть, які саме патерни event-driven архітектури використовуються.

| Патерн                                          | Опис                                                                                                          |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Event-driven                                    | Взаємодія через події (events), які асинхронно передаються між сервісами через брокер повідомлень (RabbitMQ). |
| Publish-Subscribe                               | Сервіси публікують події, інші підписуються на них і обробляють.                                              |
| Event Sourcing                                  | Збереження послідовності подій для відновлення стану (опціонально для аналітики).                             |
| CQRS (Command Query Responsibility Segregation) | Розділення операцій запису і читання через події для підвищення продуктивності (можливо майбутня еволюція).   |

### 3. Вкажіть, які інструменти та технології використовуються та чому.

| Інструмент / Технологія | Причина використання                                            |
| ----------------------- | --------------------------------------------------------------- |
| RabbitMQ                | Надійний брокер повідомлень, підтримує черги та Pub/Sub патерн. |
| FastAPI                 | Легкий асинхронний фреймворк для реалізації сервісів.           |
| Alembic                 | Для управління міграціями бази даних під час CI/CD.             |
| MySQL      | Відокремлені бази даних для кожного сервісу (DB per service).   |
| Docker | Контейнеризація та просте розгортання сервісів і брокера.       |

### 4. Оновіть діаграми.

``` mermaid
graph TD

    subgraph Frontend
        WebUI["HTML/CSS/JS"]
    end

    subgraph Services
        AuthService["AuthService"]
        UserService["UserService"]
        VacationService["VacationService"]
        NotificationService["NotificationService"]
        AuditService["AuditService"]
        AnalyticsService["AnalyticsService"]
    end

    subgraph Brokers
        MQ["RabbitMQ"]
    end

    WebUI --> AuthService
    WebUI --> UserService
    WebUI --> VacationService

    AuthService --> MQ
    VacationService --> MQ
    MQ --> NotificationService
    MQ --> AuditService
    MQ --> AnalyticsService

    VacationService --> UserService
```

### 5. Event-driven system PoC чи Stream processing PoC.
