call_df_list = []
text_list = []


def clear_all():
    call_df_list.clear()
    text_list.clear()


def append_call_df_list(call_df):
    call_df_list.clear()
    call_df_list.append(call_df)

def append_text_list(text):
    text_list.clear()
    text_list.append(text)


def get_call_df():
    if len(call_df_list) == 0:
        return []
    return call_df_list[-1]


def get_text():
    if len(text_list) == 0:
        return []
    return text_list[-1]
