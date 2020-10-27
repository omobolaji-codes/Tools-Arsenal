import gspread
import re
from collections import defaultdict
from prettyprinter import pprint
import time
from gspread.exceptions import APIError



# Open google sheet
gc = gspread.service_account(filename="../service_account.json")
sh = gc.open("Copy of Tools Arsenal")
siteDesc = sh.sheet1
lastPass = sh.get_worksheet(1)

# create domain from links
links = lastPass.col_values(1)
new_domain = ["Domain"]
for link in links[1:]:
    domain = re.match(r'^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:\.)?([^:\/?\n]+)', link)
    new_domain.append(domain.group(1))
print(len(new_domain))
# lastPass.update('C1:C1908', new_domain)


#create client from names
names = lastPass.col_values(2)
clients = ["Client"]
for name in names[1:]:
    if "-" in name:
        client = name.split("-")[0]
        clients.append(client)
    else:
        clients.append(name)
print(len(clients))
# lastPass.update("D1:D1908", clients)

domain_client_dict = defaultdict(list)
for i, domain in enumerate(new_domain):
    client = clients[i]
    if domain not in domain_client_dict:
            domain_client_dict[domain] = [client]
    else:
        if client not in domain_client_dict[domain]:
            domain_client_dict[domain].append(client)
        else:
            pass 

for key, value in domain_client_dict.items():
    print(key, value)
    try:
        siteDesc.append_row(values=value)
    except APIError:
        time.sleep(150)