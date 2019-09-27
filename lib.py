from datetime import datetime


class Tenant:
    def __init__(self, name: str, start: datetime, end: datetime=None):
        self.name = name
        self.start = start
        if end is not None:
            self.end = end
        else:
            self.end = datetime(2099, 1, 1)
        self.balance = 0.0
        self.record = []

    def post(self, amount: float, name: str=None):
        self.balance += amount
        self.record.append("%s=\t\t%.2f" % (name, amount))

    def check(self):
        self.record.append("Due:\t\t%.2f" % self.balance)
        self.balance = 0

        print('-'*20)
        print(self.name)
        for r in self.record:
            print(r)
        print('-'*20)


class Bill:
    def __init__(self, start: datetime, end: datetime, name: str=None):
        self.start = start
        self.end = end
        self.name = name

    def charge_per_usage(self, amount: float, tenants: [Tenant]):
        total_person_days = 0
        tenant_days = {}
        for tenant in tenants:
            days = (min(tenant.end, self.end) - max(tenant.start, self.start)).days + 1
            if days < 0:
                days = 0
            total_person_days += days
            tenant_days[tenant] = days
        for tenant in tenants:
            tenant.post(amount/total_person_days*tenant_days[tenant],
                        self.name + "\n\t%.2f/%d*%d" % (amount, total_person_days, tenant_days[tenant]))

    def charge_per_day(self, amount_per_day: float, tenants: [Tenant]):
        for tenant in tenants:
            days = (min(tenant.end, self.end) - max(tenant.start, self.start)).days + 1
            if days < 0:
                days = 0
            tenant.post(amount_per_day * days,
                        self.name + "\n\t%.2f*%d" % (amount_per_day, days))
