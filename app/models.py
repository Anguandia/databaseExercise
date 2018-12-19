class Human:
    def __init__(self, name, address, age, single=True):
        self.name = name
        self.address = address
        self.age = age
        self.single = single

    def __repr__(self):
        return 'name: {}, address: {}, age: {}, single: {}'.format(
            self.name, self.address, self.age, self.single)


class Simcard:
    def __init__(
        self, name, phone_number, serial, service_provider,\
        human_id,
            is_active=False):
        self.name = name
        self.phone_number = phone_number
        self.serial = serial
        self.service_provider = service_provider
        self.human_id = human_id
        self.is_active = is_active


    def __repr__(self):
        return 'phone_number: {}, service_provider: {}, serial: {}'.format(
            self.phone_number,
            self.service_provider, self.serial)
