from dogpile.cache import make_region

# Create a Dogpile cache region
cache_region = make_region().configure(
    'dogpile.cache.memory',
    expiration_time=3600  # Cache entries expire after 1 hour
)



d=[{
    "id":"t1",
    "correlation_id":"1529",
    "timestamp_in":"",
    "timestamp_out":"",
    "is_compensation": False,
    "type":"c1",
    "parent":[],
    "url":"https://randomuser.me/api",
    "status":"pending",
    "out":" ",
    "param":[]},
    {
    "id":"t2",
    "correlation_id":"1521",
    "timestamp_in":"",
    "timestamp_out":"",
    "is_compensation": False,
    "type":"c1",
    "parent":[],
    "status":"pending",
    "url":"https://randomuser.me/api",
     "out":" ",
    "param":[]},
    {
    "id":"t3",
    "correlation_id":"1522",
    "timestamp_in":"",
    "timestamp_out":"",
    "is_compensation": False,
    "type":"c1",
    "parent":["t1","t2"],
    "status":"pending",
    "url":"https://randomuser.me/api",
    "out":" ",
    "param":['''lst1.append(getvalue("t1").get("out").get("results")[0].get("gender"))''','''lst1.append(getvalue("t1").get("out").get("results")[0].get("name"))'''
    ]},
    {
    "id":"compensate_t1",
    "correlation_id":"1524",
    "timestamp_in":"",
    "timestamp_out":"",
    "is_compensation": True,
    "type":"c1",
    "parent":["compensate_t3"],
    "url":" ",
    "status":"pending",
    "out":" ",
    "param":[]},
    {
    "id":"compensate_t2",
    "correlation_id":"1525",
    "timestamp_in":"",
    "timestamp_out":"",
    "is_compensation": True,
    "type":"c1",
    "parent":["compensate_t3"],
    "url":" ",
    "status":"pending",
    "out":" ",
    "param":[]},
    {
    "id":"compensate_t3",
    "correlation_id":"1520",
    "timestamp_in":"",
    "timestamp_out":"",
    "is_compensation": True,
    "type":"c1",
    "parent":[],
    "url":" ",
    "status":"pending",
    "out":" ",
    "param":[]},
]



def create_val():
    return "a"

for l in d:
    key=(l.get("id"))
    cache_region.get_or_create(key,create_val)
    cache_region.set(key, l)

