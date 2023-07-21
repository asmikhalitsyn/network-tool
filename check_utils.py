import pynetbox

NO_DCIM_DEVICES = ('Ответ от Netbox не является pynetbox.models.dcim.Devices\n'
                   'Полученный тип: {}')
NO_ATTRIBUTE = ('У объекта отсутствует необходимый атрибут'
                'primary_ip или platform')


def check_response(response):
    if not isinstance(response, pynetbox.models.dcim.Devices):
        raise TypeError(NO_DCIM_DEVICES.format(type(response)))
    if not hasattr(response, 'primary_ip') or not hasattr(response, 'platform'):
        raise AttributeError(NO_ATTRIBUTE.format(NO_ATTRIBUTE))
    return response
