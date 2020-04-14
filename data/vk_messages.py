import vk_api


def check_id_exist(id):
    try:
        vk_session = vk_api.VkApi(
            token='7fb518f09d690c2e4fe1e017d11453ce556f1c38506262f322213d2a9b05cf1be78bf9c3b18f3e3ac0d28')
        vk = vk_session.get_api()
        user = vk.users.get(user_id='589911894', fields="city")[0]
        return True
    except:
        return False
