import pandas
from django.conf import settings
from .models import Bid, BidRound, Unit, Tender

def create_new_tender(data):
    try:
        first_round = preprocess_round_file(data['first_round_file'])
        drops = preprocess_drops_file(data['drops_file'])
        tender, _ = Tender.objects.update_or_create(
            date = first_round['fromdate'][0],
            market = data['market'],
            direction = data['direction'],
            tender_round = data['tender_round'],
            bid_file = data['bid_file']     # Bid file validation is not implemented!
        )
        create_bid_rounds(tender, drops)
        create_units(tender, first_round)
        create_bids(tender, first_round, bid_round=1)
    except:
        raise


def update_tender(data):
    try:
        round_table = preprocess_round_file(data['round_file'])
        create_bids(Tender.objects.get(pk=data['tender_id']), round_table, data['bid_round'])
    except:
        raise

def preprocess_round_file(round_file):
    print("preprocess_round_file...")
    try:
        round_table = pandas.read_excel(round_file, engine='openpyxl')
        check_round_file(round_table)
        round_table.columns = ['fromdate', 'todate', 'product_type', 'price', 'amount', 'product', 'producer', 'partner']
        round_table['fromdate'] = pandas.to_datetime(round_table['fromdate'])
        round_table['todate'] = pandas.to_datetime(round_table['todate'])
        return round_table
    except:
        raise

def preprocess_drops_file(drops_file):
    print("preprocess_drops_file...")
    try:
        drops = pandas.read_excel(drops_file, engine='openpyxl')
        check_drops_file(drops)
        drops.columns = ['round', 'max1', 'drop1', 'max2', 'drop2']
        return drops
    except:
        raise

def create_bid_rounds(tender, drops):
    print("create_bid_rounds...")
    for i in range(10):
        BidRound.objects.update_or_create(
            number = i + 1,
            max_price_wkdy = drops['max1'][i],
            max_price_wknd = drops['max2'][i],
            tender = tender
        )

def create_units(tender, round_table):
    print("create_units...")
    for i in round_table.index:
        unit, _ = Unit.objects.update_or_create(
            fromdate = round_table['fromdate'][i],
            todate = round_table['todate'][i],
            tender = tender
        )

def create_bids(tender, round_table, bid_round):
    print("create_bids...")
    for i in round_table.index:
        Bid.objects.update_or_create(
            price = round_table['price'][i],
            amount = round_table['amount'][i],
            ours = not pandas.isna(round_table['producer'][i]),
            bid_round = BidRound.objects.get(number=bid_round),
            unit = Unit.objects.get(tender=tender, fromdate = round_table['fromdate'][i])
        )

def check_round_file(round_table):
    expected_columns = [
                    'Időszak kezdete', 'Időszak vége', 'Termék típusa',
                    'Elnyert kapacitás ára [Ft/MW/h]', 'Elnyert kapacitás mennyisége [MW/h]',
                    'Kapacitás típusa', 'Szabályozási egység', 'Partner'
                    ]
    if len(round_table.columns) != len(expected_columns): 
        raise Exception("Invalid number of columns in round file: " + str(len(round_table.columns)) + ", expected: " + str(len(expected_columns)))
    for i in range(len(round_table.columns)):
        if round_table.columns[i] != expected_columns[i]:
            raise Exception("Invalid column in round file '" + round_table.columns[i] + "', expected: '" + expected_columns[i] + "'")

def check_drops_file(drops):
    expected_columns = ['Kör', 'Max. árszint', 'Min. csökkentés', 'Max. árszint.1', 'Min. csökkentés.1']
    if len(drops.columns) != len(expected_columns) or len(drops.index) != 10:
        raise Exception("Invalid table dimensions in drops file: " + str(len(drops.columns)) + "x" + str(len(drops.index)) + ", expected: " + str(len(expected_columns)) + "x11")
    for i in range(len(drops.columns)):
        if drops.columns[i] != expected_columns[i]:
            raise Exception("Invalid column in drops file '" + drops.columns[i] + "', expected: '" + expected_columns[i] + "'")

def override_bid_file(data):
    try:
        tender = Tender.objects.get(pk=data['tender_id'])
        bid_table = pandas.read_excel(tender.bid_file, engine='openpyxl', sheet_name='PROPOSAL')
        info_sheet = pandas.read_excel(tender.bid_file, engine='openpyxl', sheet_name='INFO')
        bids = data['bids']
        info_sheet.iloc[7, 1] = data['round']
        for i in range(len(bids)):
            bid_table.at[i, '5 MW'] = bids[str(i)]['5']
            bid_table.at[i, '10 MW'] = bids[str(i)]['10']
            bid_table.at[i, '15 MW'] = bids[str(i)]['15']
        date = str(tender.date).split(" ")[0]
        filepath = '{0}/bids_{1}_{2}_{3}_{4}.xlsx'.format(settings.MEDIA_ROOT, date, tender.market, tender.direction, tender.tender_round) 
        with pandas.ExcelWriter(filepath) as writer:
            info_sheet.to_excel(writer, index=False, sheet_name='INFO')
            bid_table.to_excel(writer, index=False, sheet_name='PROPOSAL')
        return filepath
    except:
        raise