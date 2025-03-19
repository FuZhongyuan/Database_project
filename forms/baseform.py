from wtforms import Form


class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for errors in self.errors.values():
                message_list.extend(errors)
        return message_list

    # 这段代码定义了一个表单基类BaseForm，
    # 它添加了一个messages属性，该属性收集表单中所有字段的错误消息，并以列表的形式返回它们。这可以用于在用户界面上显示错误消息。
