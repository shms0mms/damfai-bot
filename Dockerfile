FROM python:3.12

WORKDIR /app

# Устанавливаем зависимости
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

# Копируем весь проект в контейнер
COPY . .


# RUN apt-get update && apt-get install -y supervisor
# Копируем скрипт-обертку
COPY go.sh .


# Запускаем скрипт-обертку
CMD ["./go.sh"]


# CMD ["supervisord", "-c", "/app/supervisord.conf"]

