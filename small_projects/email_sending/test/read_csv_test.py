from sche_email_sending import get_user_list, pack_send_email_and_user


# print(get_user_list("../u.csv"))
# print(get_user_list("../user.csv"))

s = pack_send_email_and_user("../user.csv", "users.csv")
print(list(s))
