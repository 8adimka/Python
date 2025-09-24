import re

text_1 = """1.181.2.178 [17/May/2015:20:05:36] "GET / HTTP/1.1" 200
1.125.2.148 [17/May/2015:20:05:19] "GET /?flav=rss20 HTTP/1.1" 200
1.170.2.204 [17/May/2015:20:05:03] "POST /?flav=atom HTTP/1.1" 200
1.163.30.77 [17/May/2015:20:05:36] "GET /images/gle.png HTTP/1.1" 200
1.163.30.77 [17/May/2015:20:05:37] "GET /blog/dot.html HTTP/1.1" 200"""

text_2 = "Команда regex принимает в качестве аргумента регулярное выражение, по которой нужно будет фильтровать строки входных данных. -> посчитай колличество слов"


reg_exp_1 = r"\d{1,3}\.\d{3}\.\d{1,3}\.\d{1,3}"

result = re.findall(reg_exp_1, text_1)
ip = re.match(reg_exp_1, text_1)

print(result)
if ip:
    print(ip.group())

reg_exp_2 = r"\b\w+\b"

res = re.findall(reg_exp_2, text_2)

print(len(res))
