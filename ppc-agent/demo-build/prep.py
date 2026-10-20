"""Merge real product data: Oct 18 catalog read (42 items, Santa Rosa stock) + Oct 19 Sana warehouse read
(all four stores) + 17 new items. Run: python3 prep.py > products_all.json"""
import json
old = json.load(open("real_products.json"))
rs = json.load(open("real_stock_2026-10-19.json"))
WH = rs["warehouses"]
out = []
for p in old:
    st = {WH[k]: v for k, v in rs["inv"][p["item"]].items()}
    out.append(dict(item=p["item"], name=p["name"], price=p["price"], stock=st, sr_oct18=p["sr_stock"], new=False))
for p in rs["new_products"]:
    st = {WH[k]: v for k, v in rs["inv"][p["item"]].items()}
    out.append(dict(item=p["item"], name=p["name"], price=p["price"], stock=st, sr_oct18=None, new=True))
al = json.load(open("real_alert_inputs.json"))
for p in al["products"]:
    st = {WH[k]: v for k, v in p["stock"].items()}
    out.append(dict(item=p["item"], name=p["name"], price=p["price"], stock=st, sr_oct18=None, new=True))
print(json.dumps(dict(asof=rs["asof"], products=out)))
