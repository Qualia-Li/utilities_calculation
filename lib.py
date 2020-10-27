from datetime import datetime


all_tenants = []


class Tenant:
    def __init__(self, name: str, start: datetime, end: datetime = None):
        self.name = name
        self.start = start
        if end is not None:
            self.end = end
        else:
            self.end = datetime(2099, 1, 1)
        self.balance = 0.0
        self.record = []
        all_tenants.append(self)

    def post(self, amount: float, name: str = None):
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

        self.record.clear()

    def __str__(self):
        return self.name


class Bill:
    def __init__(self, start: datetime, end: datetime, name: str = None):
        self.start = start
        self.end = end
        self.name = name
        self.billing_period = "Billing Period: %s ~ %s" % (str(start.date()), str(end.date()))

    def charge_per_usage(self, amount: float, tenants: [Tenant] = None):
        if tenants is None:
            tenants = all_tenants
        total_person_days = 0
        tenant_days = {}
        actual_period = {}
        # print('*'*8)
        for tenant in tenants:
            days = (min(tenant.end, self.end) - max(tenant.start, self.start)).days + 1
            actual_period[tenant] = "Actual Period: %s ~ %s" % \
                                    (str(max(tenant.start, self.start).date()), str(min(tenant.end, self.end).date()))
            if days < 0:
                days = 0
            # print(tenant.name, days)
            # print(tenant.end, min(tenant.end, self.end), max(tenant.start, self.start))
            total_person_days += days
            tenant_days[tenant] = days
        # print(self.name)
        # for tenant in tenants:
        #     print(tenant.name, tenant_days[tenant])
        for tenant in tenants:
            if tenant_days[tenant] == 0:
                continue
            tenant.post(amount/total_person_days*tenant_days[tenant],
                        "%s\n\t%s\n\t%s\n\t%.2f/%d*%d" %
                        (self.name, self.billing_period, actual_period[tenant], amount, total_person_days, tenant_days[tenant]))

    def charge_per_day(self, amount_per_day: float, tenants: [Tenant] = None):
        if tenants is None:
            tenants = all_tenants
        for tenant in tenants:
            days = (min(tenant.end, self.end) - max(tenant.start, self.start)).days + 1
            actual_period = "Actual Period: %s ~ %s" % \
                            (str(max(tenant.start, self.start).date()), str(min(tenant.end, self.end).date()))
            if days < 0:
                continue
            tenant.post(amount_per_day * days,
                        "%s\n\t%s\n\t%s\n\t%.2f*%d" %
                        (self.name, self.billing_period, actual_period, amount_per_day, days))

#
# xu_chen = Tenant("Xu Chen", start=datetime(2019, 1, 1))
# zewei_chen = Tenant("Zewei Chen", start=datetime(2019, 1, 1))
# quanlai_li = Tenant("Quanlai Li", start=datetime(2019, 9, 1), end=datetime(2019, 12, 8))
# ping_hu = Tenant("Ping Hu", start=datetime(2019, 5, 10), end=datetime(2019, 8, 25))
# yuchen_guo = Tenant("Yuchen Guo", start=datetime(2019, 11, 1))
#
# Bill(start=datetime(2019, 10, 1), end=datetime(2019, 12, 10), name="Internet")\
#     .charge_per_day(0.5)
#
# Bill(start=datetime(2019, 10, 1), end=datetime(2019, 12, 10), name="Cleaning")\
#     .charge_per_day(0.33)
#
# Bill(start=datetime(2019, 9, 4), end=datetime(2019, 10, 1), name="PGE")\
#     .charge_per_usage(48.33)
# Bill(start=datetime(2019, 10, 2), end=datetime(2019, 10, 30), name="PGE")\
#     .charge_per_usage(73.01)
#
# Bill(start=datetime(2019, 8, 15), end=datetime(2019, 10, 15), name="Water")\
#     .charge_per_usage(184.51)
#
# # Bill(start=datetime(2019, 10, 1), end=datetime(2019, 12, 10), name="Garbage")\
# #     .charge_per_day(0.3)
#
# quanlai_li.check()
# xu_chen.check()
# zewei_chen.check()
# ping_hu.check()
# yuchen_guo.check()
