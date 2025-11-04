from users.models import User


def save_chat_id_to_user(token, chat_id):
    try:
        user = User.objects.get(telegram_auth_token=token)
        user.telegram_chat_id = chat_id  # добавьте поле telegram_chat_id в модель User
        user.save()
    except User.DoesNotExist:
        print(f'Пользователь с токеном {token} не найден')