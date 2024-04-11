from functools import wraps

LIST_OF_ADMINS = [12345678, 87654321]

def restricted(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        if args[0].message.from_user.id:
            user_id = args[0].message.from_user.id
            if user_id not in LIST_OF_ADMINS:
                await args[0].message.reply_text("Usted no tiene acceso a estas funcionalidades.")
                print(f"Unauthorized access denied for {user_id}.")
                return
        return await func(*args, **kwargs)
    return wrapped