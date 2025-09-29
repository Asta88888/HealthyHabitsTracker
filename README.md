# Приложение для отслеживания привычек. 
## Описание: 
Позволяет создавать, просматривать, обновлять и удалять привычки, а также делиться публичными привычками.
## Установка:
1) Клонируем репозиторий
2) Создаём и активируем виртуальное окружение
3) Устанавливаем зависимости
4) Применяем миграции
5) Создаём суперпользователя
6) Запускаем сервер

## Разрешения
1) Публичные привычки доступны всем пользователям.
2) CRUD (обновление и удаление) доступны только владельцу привычки.



* Создаем файл docker-compose.yaml
1) описываем подключение и создание контейнера базы данных, редиса, nginx, селери, селери бит, бэкэнда
2) командой docker compose up --build создаем контейнер
3) командами docker compose ps, docker compose logs проверяем

* Создаем Dockerfile
после созданных контейнеров проверяем http://localhost:8000 должен отобразиться сайт

* Создаем гитхаб сикретс
1) Складываем ключи для проэкта. Либо залить всю папку .env, либо каждый ключ отдельно 
2) Создаем директорию гитхаб воркфлоу и прописываем в файле с расширением ямл настройки для линтеров, тестов, билда и деплоя, так чтобы при пуше или пул реквесте автоматически начинались проверки и деплой на сервер

* Создаем виртуальную машину в яндекс клауд или на другом ресурсе. 
1) Соединяемся с вм в терминале введя команду: ssh -l asta 158.160.145.80
2) Далее скачиваем и проверяем на обновления докер командами:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
3) Настраиваем файрвол и открываем порты 80,443,22:
docker ufw status
docker ufw enable
docker ufw allow 80/tcp
docker ufw allow 443/tcp
docker ufw allow 22/tcp

* В итоге после пуша и пул реквеста гитхаб осуществит все процессы и можно открывать сайт по IP вм: 158.160.145.80:80 
