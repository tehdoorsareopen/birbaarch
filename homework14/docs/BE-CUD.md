# Бизнес события и CUD

## Бизнес события

1. Создание новой задачи

Поскольку у нас предусмотрен CUD для юзеров и тасок в Аккаунтинг - для Аккаунтлога нам нужно передать только айдишники, дату и тип события (завершена/назначена) для определения из какого поля плюсовать баланс

```
(TM Service -> Accounting Service)
(task_id, user_id, type (assigned), date)
```

2. Реассайн задач

Отдаем список

```
(TM Service -> Accounting Service)
(task_id, user_id, type (assigned), date)
```

3. Завершение задачи

```
(TM Service -> Accounting Service)
(task_id, user_id, type (completed), date)
```

4. Рассчет сотрудников по расписанию

Поскольку в Аналитике нам не требуется подробная аналитика кто, что, когда, сколько, а только 3 калькулируемые цифры - кол-во папугов, заработок топ-менеджмента и самая дорогая задача, то и отдаем мы ограниченное кол-во данных:

```
(Accounting Service -> Analytics Service)
(most_expensive_task_price, birb_negative_balance_count, top_managers_balance)
```

Думал где выполнять рассчеты, лучше, пожалуй, все-таки на Аккаунтинге, хотя, может с точки зрения логики это не совсем корректно. Так меньше данных будет гоняться по сети, а выборка, например, самой дорогой задачи вообще элементарно делается

5. Нотификации об оплате

```
(Accounting Service -> Analytics Service)
(user__name, account__balance, message)
```

## CUD

1. Для аккаунтов

```
(Auth Service -> TM Service)
id, name, role

(Auth Service -> Accounting Service)
id, name, role
```

2. Для задач

```
(TM Service -> Accounting Service)
id, name, assigne_price, complete_price
```