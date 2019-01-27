from redis import Redis


r = Redis(host="127.0.0.1", port=6379, db=0)
r.set('test:one', 'hey')
print(r.get('test'))