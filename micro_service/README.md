На основе предложенного шаблона реализуйте сервис, реализующий регистрацию пользователей. Сервис должен поддерживать REST API и коллекцию /user/, хранящую данные о логинах и паролях пользователей, зарегистрированных в системе. Сервис должен принимать и отдавать информацию в формате JSON. Сервис должен хранить следующую информацию про каждого пользователя: логин, хеш пароля (лучше с солью), дату регистрации.

Я использую библиотеку Request она помогает делать различные запросы. когад мы удаляем пользователя, который подключился к серверу нам возвращется пустая строка, если мы создаём разных людей с одинаковыми паролями, то результат будет разынм. Если вы попытаеть узнать информацию об удалённом пользователе то сервер вернёт ошибку.

![Screenshot_130](https://user-images.githubusercontent.com/72688086/147085733-6e3fa1a8-0724-43c3-9526-e5c060760539.png)

Вот так выглядит json 

![Screenshot_131](https://user-images.githubusercontent.com/72688086/147086350-fc7c1f28-8b1e-41a4-9e84-4e84be0fea68.png)

Модифицируйте код вашего сервиса таким образом, чтобы он поддерживал защищенное соединение.
![Screenshot_132](https://user-images.githubusercontent.com/72688086/147086563-8b18595f-f2fe-4ee5-b1b6-113eaab7126f.png)