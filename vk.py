# Импортируем созданный нами класс Server
from system.server import Server
# Получаем из config.py наш api-token
from system.config import vk_api_token, vk_group_id


server1 = Server(vk_api_token, vk_group_id, "server1")

server1.start()
