import pickle
import pyupbit

""" members id, pw save """

# members = {'zenka' : 'ktu007za!', 'butysoo' : '8050soo!', 'liebe' : 'lb6114!'}
members = {'zenka' : 'dragonktu007!', 'butysoo' : 'mom8050!', 'liebe' : 'liebe5634!'}


with open('/root/UBiCauto/Acct/members.pickle', 'wb') as fw:
    pickle.dump(members, fw)

print(members)