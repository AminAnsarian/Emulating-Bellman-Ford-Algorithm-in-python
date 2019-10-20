"""
This class is for BellmanFord Algorithm Calculations
 Pooya Khandel
"""

from socket import *
import math


class BFA:
    def __init__(self, r_count, first_cost, my_name, which_port, adr_to_name):
        self.use_who = dict()
        self.update = True
        self.do_print = False
        self.new_pm = None
        self.pm_adr = None
        self.first_cost = first_cost
        self.old_pm = {}
        self.ports = which_port
        self.my_port = which_port[my_name]
        self.name = my_name
        self.r_count = r_count
        self.adr_to_name = adr_to_name
        self.table = []
        self.lie_table = []



        self.init_tables()
        # for m in range(r_count):
        #     self.table.append([])
        #     self.lie_table.append([])
        #     for n in range(r_count):
        #         self.table[m].append('N')
        #         self.lie_table[m].append(first_cost[n])

        print("check1")
        print(self.table)
        print(self.lie_table)
        # for m in range(r_count):
        #     self.table[int(my_name) - 1][m] = first_cost[m]
        #     if first_cost[m] == 'N':
        #         self.use_who[m + 1] = '@N'
        #     else:
        #         self.use_who[m + 1] = str(m + 1)
        print("check2")
        print(self.table)
        print(self.lie_table)
        self.bf_show()
        self.permittion = []
        self.router_sock = socket(AF_INET, SOCK_DGRAM)
        self.router_sock.bind(('', self.my_port))
        self.serverName = '127.0.0.1'


        # print(self.use_who)
        # self.solving_pp_cost()

    def init_tables(self):
        self.table = []
        self.lie_table = []
        self.use_who = dict()
        for m in range(self.r_count):
            self.table.append([])
            self.lie_table.append([])
            for n in range(self.r_count):
                self.table[m].append('N')
                self.lie_table[m].append(self.first_cost[n])

        for m in range(self.r_count):
            self.table[int(self.name) - 1][m] = self.first_cost[m]
            if self.first_cost[m] == 'N':
                self.use_who[m + 1] = '@N'
            else:
                self.use_who[m + 1] = str(m + 1)

        self.solving_pp_cost()

    def who_to_send(self):
        for m in range(self.r_count):
            if self.table[int(self.name) - 1][m] == 'N':
                self.permittion.append(False)
            else:
                self.permittion.append(True)

    def send(self):
        if self.update:
            message = str()
            for sending_router in range(self.r_count):
                # print(sending_router)
                if self.permittion[sending_router]:
                    if not(sending_router + 1 == int(self.name)):
                        for m in range(self.r_count):
                            message = message + self.lie_table[sending_router][m]
                        self.router_sock.sendto(bytes(message, 'UTF-8'),
                                                (self.serverName, self.ports[str(sending_router + 1)]))
                        # print("message: {} to {} with {}".format(message, self.ports[str(sending_router + 1)], str(sending_router + 1)))
                        message = str()
                    else:
                        pass

    def receive(self):
        self.router_sock.settimeout(0.5)
        try:
            message, client_address = self.router_sock.recvfrom(2048)
            self.new_pm = list(message.decode())
            self.pm_adr = client_address[1]
            print("ad: {}  pm: {}".format(self.pm_adr, self.new_pm))
            if self.pm_adr in list(self.old_pm.keys()):
                if not(self.old_pm[self.pm_adr] == self.new_pm):
                    self.old_pm[self.pm_adr] = self.new_pm
                    self.table[self.adr_to_name[self.pm_adr] - 1] = self.new_pm
                    print("router {} send new update: {}".format(self.pm_adr, self.new_pm))
                    self.do_print = True
                else:
                    self.do_print = False
            else:
                self.old_pm[self.pm_adr] = self.new_pm
                self.table[self.adr_to_name[self.pm_adr] - 1] = self.new_pm
                print("router {} send new update: {}".format(self.pm_adr, self.new_pm))
                # print("table{}".format(self.table))
                self.do_print = True
        except:
            self.router_sock.settimeout(None)

    def do_alg(self):
        distance = []
        for d_r_iter in range(self.r_count):
            # print("name{}, iter{}".format(self.name, d_r_iter))
            if not(int(self.name) - 1 == d_r_iter):
                if self.table[int(self.name) - 1][d_r_iter] == 'N':
                    temp = math.inf
                else:
                    temp = float(self.table[int(self.name) - 1][d_r_iter])
                for c_r_iter in range(self.r_count):
                    if c_r_iter == d_r_iter:
                        if self.table[int(self.name) - 1][c_r_iter] == 'N':
                            cost1 = math.inf
                        else:
                            cost1 = float(self.table[int(self.name) - 1][c_r_iter])
                    else:
                        if self.table[c_r_iter][int(self.name) - 1] == 'N':
                            cost1 = math.inf
                        else:
                            cost1 = float(self.table[c_r_iter][int(self.name) - 1])

                    if self.table[c_r_iter][d_r_iter] == 'N':
                        cost2 = math.inf
                    else:
                        cost2 = float(self.table[c_r_iter][d_r_iter])
                    distance.append(cost1 + cost2)

                min_dis = min(distance)
                if min_dis < temp and not(min_dis == math.inf):
                    self.table[int(self.name) - 1][d_r_iter] = str(int(min_dis))
                    for m in range(self.r_count):
                        for _ in range(self.r_count):
                            self.lie_table[m][d_r_iter] = str(int(min_dis))
                    # print(distance)
                    self.update = True
                    min_through = distance.index(min_dis)
                    self.use_who[d_r_iter + 1] = str(min_through + 1)
                    # print(min_through)
                    lie_to = min_through
                    # print(self.lie_table)
                    self.lie_table[lie_to][d_r_iter] = 'N'
                    # print(lie_to, d_r_iter, self.lie_table)
                distance.clear()

        if self.do_print:
            self.bf_show()
            # print(self.table)
            # print(self.lie_table)


    def bf_show(self):
        print("\nThe Cost Tabel of router {} is :".format(self.name))
        print("        ", end="")
        for h in range(self.r_count):
            print("{}    ".format(h + 1), end="")
        print("\n---------------------------------")
        for row in range(self.r_count):
            print("{}|      ".format(row + 1), end="")
            for col in range(self.r_count):
                if row == int(self.name) - 1:
                    print("{}\{}  ".format(self.table[row][col], self.use_who[col + 1]), end="")
                else:
                    print("{}    ".format(self.table[row][col]), end="")
            print()
        print("--------------------------------------------------------")

    def solving_pp_cost(self):
        for m in range(self.r_count):
            if self.use_who[m + 1] == str(m + 1) and not(self.name == m + 1):
                self.lie_table[m][m] = 'N'

    def check_cost(self, new_cost):
        if self.first_cost == new_cost:
            print("No Cost Change!")
        else:
            print("link costs of router {} is changed!".format(self.name))
            self.first_cost = new_cost
            print(self.lie_table)
            self.init_tables()
            print(self.lie_table)
            self.who_to_send()
            pass
