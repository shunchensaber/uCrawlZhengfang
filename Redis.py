import redis
import Login
r =redis.Redis(host="127.0.0.1",port=6379)
print(r.llen("list1"))
a = r.llen("list1")
print(a)
while (a>0):
    id = r.rpop("list1")
    id = bytes.decode(id)
    print(id)
    print(type(id))
    pass1 = r.rpop("list2")
    pass1 = bytes.decode(pass1)

    pass2 = r.rpop("list3")
    pass2 = bytes.decode(pass2)
    r.rpush("list1",id)
    r.rpush("list2",pass1)
    r.rpush("list3",pass2)
    s = Login.Who(id, pass1)
    pa = Login.University(s, pass2)
    pa.login()
    print(pa.getclass())
    print(pa.highest_grade())
print('1111')

