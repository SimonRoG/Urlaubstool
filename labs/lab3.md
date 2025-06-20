# Практична робота №3

**Виконали:** ІП-з31 Семен Прохода, Арсен Потеряйко

**Тема:** Мікросервісна архітектура.

**Мета:** Застосувати мікросервісну архітектуру для проектування складних систем.

## Завдання:

### 1. Між-сервісна взаємодія:

#### a. Визначити які сервіси між собою спілкуються синхронно.

- Frontend &harr; AuthService – логін, реєстрація користувача
- Frontend &harr; VacationService – створення/перегляд заявок на відпустку
- Frontend &harr; UserService – отримання/оновлення даних про користувача
- Manager &harr; VacationService – затвердження або відхилення запиту
- Admin &harr; UserService – додавання/видалення користувачів, зміна ролей

#### b. Визначити які сервіси між собою спілкуються асинхронно, за допомогою RabbitMQ

- VacationService &rarr; NotificationService – надсилання повідомлень після зміни статусу заявки
- AuthService &rarr; AuditService – логування авторизаційних подій

### 2. Робота з даними.

#### a. Визначити, який патерн використовується для роботи з базою даних (db per service or shared db)

**Shared DB**

| Сервіс              | Таблиця       |
| ------------------- | ------------- |
| AuthService         | auth          |
| UserService         | users         |
| VacationService     | vacations     |
| NotificationService | notifications |
| AuditService        | audit         |

#### b. Визначити, як накачуються міграційні скрипти для бази даних.

- Інструмент: **Alembic** (для FastAPI)
- Автоматичне застосування в CI/CD під час деплойменту контейнера

#### c. Визначити, як саме відбувається синхронізація даних між сервісами.

- **Event-driven architecture** через RabbitMQ
- Використовується підхід **eventual consistency**

### 3. Оновити діаграми, зобразити всі зв’язки між сервісами.

**Архітектура мікросервісів:**

```mermaid
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

    VacationService --> UserService
```

### 4. Вказати, які саме патерни для мікросервісної архітектури використовуються.

| Категорія     | Патерн                     | Опис                                                   |
| ------------- | -------------------------- | ------------------------------------------------------ |
| Архітектура   | **Microservices**          | Поділ на незалежні сервіси за функціями                |
| Взаємодія     | **API Gateway (Frontend)** | Один вхід до системи                                   |
| База даних    | **Shared DB**              | Одна спільна база даних для всіх сервісів              |
| Події         | **Event-driven**           | RabbitMQ для комунікації між сервісами                 |
| Стабільність  | **Circuit Breaker**        | Захист від каскадних збоїв (через async timeout)       |
| Безпека       | **JWT Authentication**     | Авторизація через токени                               |
| Синхронізація | **Eventual Consistency**   | Дані між сервісами узгоджуються асинхронно через події |
