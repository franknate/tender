import pandas
from .models import Bid, Unit, Tender

def save_to_db(data):
    table = pandas.read_excel(data['file'], engine='openpyxl')
    if not check_file(table): return False

    table.columns = ['fromdate', 'todate', 'product_type', 'price', 'amount', 'product', 'producer', 'partner']
    table['fromdate'] = pandas.to_datetime(table['fromdate'])
    table['todate'] = pandas.to_datetime(table['todate'])

    tender, _ = Tender.objects.update_or_create(
        date = table['fromdate'][0],
        market = data['market'],
        direction = data['direction'],
        tender_round = data['tender_round']
    )

    for i in table.index:
        unit, _ = Unit.objects.update_or_create(
            fromdate = table['fromdate'][i],
            todate = table['todate'][i],
            tender = tender
        )        
        Bid.objects.update_or_create(
            bid_round = data['bid_round'],
            price = table['price'][i],
            amount = table['amount'][i],
            ours = not pandas.isna(table['producer'][i]),
            unit = unit
        )

    return True

def check_file(table):
    expected_columns = [
                    'Időszak kezdete', 'Időszak vége', 'Termék típusa',
                    'Elnyert kapacitás ára [Ft/MW/h]', 'Elnyert kapacitás mennyisége [MW/h]',
                    'Kapacitás típusa', 'Szabályozási egység', 'Partner'
                    ]
    if len(table.columns) != len(expected_columns): 
        print("Length error")
        return False
    for i in range(len(table.columns)):
        if table.columns[i] != expected_columns[i]:
            print(table.columns[i])
            return False
    return True