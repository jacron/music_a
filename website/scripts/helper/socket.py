import json

from channels import Group


def socket_log(msg, mode, id=None):
    Group("chat").send({
        "text": json.dumps({
            'msg' : msg,
            'mode': mode,
            'id': id
        })
    })


