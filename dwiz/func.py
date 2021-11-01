from numpy import mean

def get_turnover(df):
    sum = 0
    for d in df:
        sum += d
    return round(sum, 2)

def get_count_receipts(receipts, date):
    l = 0
    for r in receipts:
        if str(date) in str(r['date']):
            l += 1
    return l

def get_middle_check(receipts, date):
    checks_ls = []
    for r in receipts:
        if str(date) in str(r['date']):
            total = 0
            for item in r['cartitems']:
                total += item['total_price']
            checks_ls.append(total)
    return round(mean(checks_ls), 2)

def get_count_products(receipts, date):
    q = 0
    for r in receipts:
        if str(date) in str(r['date']):
            for item in r['cartitems']:
                q += item['qty']
    return round(q, 2)

def diff_percent(num1, num2):
    res = (num2 - num1) / num1 * 100
    return round(res, 2)

def difference(num1, num2):
    res = num1 - num2
    return round(-res, 2)

def get_products(receipts, date):
    ls = []
    for r in receipts:
        if str(date) in str(r['date']):
            for item in r['cartitems']:
                id = item['product_id']
                total = item['total_price']
                qty = item['qty']
                ls.append(
                    {
                        "product_id" : id,
                        "total" : total,
                        "qty" : qty,
                    }
                )

    res = []
    tmp = {}
    for i in ls:
        d1, d2, d3 = i.items()
        if d1[1] not in tmp:
            tmp[d1[1]] = len(res)
            res.append(i)
        else:
            t = res[tmp[d1[1]]]
            t['total'] = t.get('total') + d2[1]
            t['qty'] = t.get('qty') + d3[1]
    
    return res

def get_info_products(prod1, prod2, top, down):

    for p1 in prod1:
        for p2 in prod2:
            if p1['product_id'] == p2['product_id']:
                total = p1['total'] - p2['total']
                qty = p1['qty'] - p2['qty']
                if total > 0:
                    top.append(
                        {
                            'product_id' : p1['product_id'],
                            'total' : round(total, 2),
                            'qty' : round(qty, 2),
                        }
                    )
                if total < 0:
                    down.append(
                        {
                            'product_id' : p1['product_id'],
                            'total' : round(total, 2),
                            'qty' : round(qty, 2),
                        }
                    )