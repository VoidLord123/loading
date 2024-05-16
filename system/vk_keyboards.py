from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from system.config import vk_group_id, vk_admin_id

not_subscribed = VkKeyboard(inline=True)
not_subscribed.add_openlink_button("Подписаться", f"https://vk.com/club{vk_group_id}")
not_subscribed.add_button("Запустить тест", VkKeyboardColor.PRIMARY)


num_buttons = VkKeyboard(one_time=True)
for i in range(1, 6):
    num_buttons.add_button(str(i), VkKeyboardColor.SECONDARY)
num_buttons.add_line()
for i in range(6, 11):
    num_buttons.add_button(str(i), VkKeyboardColor.SECONDARY)

to_user = VkKeyboard(inline=True)
to_user.add_openlink_button("Записаться на бесплатную консультацию!", f"https://vk.com/id{vk_admin_id}")
