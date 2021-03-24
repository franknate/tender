import pandas
import datetime
import sys, os
from django.conf import settings
from .models import OurBid, Bid, BidRound, Unit, Tender


AMOUNTS = [5, 10, 15]

def create_new_tender(data):
    try:
        drops = preprocess_drops_file(data['drops_file'])
        dates, datestr = preprocess_bid_file(data['bid_file'])
        tender, _ = Tender.objects.update_or_create(
            datestr = datestr,
            market = data['market'],
            direction = data['direction'],
            tender_round = data['tender_round'],
            current_bid_round = 1,
            bid_file = data['bid_file']     # Bid file validation is not implemented!
        )
        create_bid_rounds(tender, drops)
        create_units(tender, dates)
    except:
        printException()
        raise


def update_tender(data):
    try:
        round_table = preprocess_round_file(data['round_file'])
        tender = Tender.objects.get(pk=data['tender_id'])
        create_bids(tender, round_table, data['bid_round'])
        tender.current_bid_round += 1
        tender.save()
    except:
        printException()
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
        printException()
        raise


def preprocess_drops_file(drops_file):
    print("preprocess_drops_file...")
    try:
        drops = pandas.read_excel(drops_file, engine='openpyxl')
        check_drops_file(drops)
        drops.columns = ['round', 'max1', 'drop1', 'max2', 'drop2']
        return drops
    except:
        printException()
        raise


def preprocess_bid_file(bid_file):
    print("preprocess_bid_file...")
    try:
        bid_table = pandas.read_excel(bid_file, engine='openpyxl', sheet_name='PROPOSAL')
        info_sheet = pandas.read_excel(bid_file, engine='openpyxl', sheet_name='INFO')
        check_bid_file(bid_table, info_sheet)
        dates = []
        for i in bid_table.index:
            stupid_date = bid_table['Dátum'][i].split("-")
            fromdate = pandas.to_datetime(stupid_date[0])
            todate = fromdate.replace(day=int(stupid_date[1]))
            dates.append({'from': fromdate, 'to': todate})
        datestr = info_sheet.iloc[0, 1]
        return dates, datestr
    except:
        printException()
        raise


def create_bid_rounds(tender, drops):
    print("create_bid_rounds...")
    for i in range(10):
        BidRound.objects.update_or_create(
            number = i + 1,
            max_price_wkdy = drops['max1'][i],
            max_price_wknd = drops['max2'][i],
            min_drop_wkdy = drops['drop1'][i],
            min_drop_wknd = drops['drop2'][i],
            tender = tender
        )


def create_units(tender, dates):
    print("create_units...")
    for date in dates:
        unit, _ = Unit.objects.update_or_create(
            fromdate = date['from'],
            todate = date['to'],
            tender = tender
        )


def create_bids(tender, round_table, bid_round):
    print("create_bids...")
    for i in round_table.index:
        bid, _ = Bid.objects.update_or_create(
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


def check_bid_file(bid_table, info_sheet):
    bid_expected_columns = [
        'Dátum', 'Termék', 'Ajánlat paraméterei',
        '5 MW', '10 MW', '15 MW', '20 MW', '25 MW',
        '30 MW', '35 MW', '40 MW', '45 MW', '50 MW',
        '55 MW', '60 MW', '65 MW', '70 MW', '75 MW',
        '80 MW', '85 MW', '90 MW', '95 MW', '100 MW',
        '105 MW', '110 MW', '115 MW', '120 MW', '125 MW'
    ]
    if len(bid_table.columns) != len(bid_expected_columns):
        raise Exception("Invalid number of columns in bid file: " + str(len(bid_table.columns)) + ", expected: " + str(len(bid_expected_columns)))
    for i in range(len(bid_table.columns)):
        if bid_table.columns[i] != bid_expected_columns[i]:
            raise Exception("Invalid column in round file '" + bid_table.columns[i] + "', expected: '" + bid_expected_columns[i] + "'")
    # Check info sheet here


def create_our_bids(tender, bids):
    print("create_our_bids...")
    for i, unit in enumerate(Unit.objects.filter(tender=tender)):
        for amount in AMOUNTS:
            if bids[i][str(amount)]:
                our_bid, _ = OurBid.objects.update_or_create(
                    o_price = bids[i][str(amount)],
                    o_amount = amount,
                    o_bid_round = BidRound.objects.get(tender=tender, number=tender.current_bid_round),
                    o_unit = unit
                )


def initial_bids(tender_id):
    tender = Tender.objects.get(pk=tender_id)
    bid_round = BidRound.objects.get(tender=tender, number=tender.current_bid_round)
    bid_table = []
    for unit in Unit.objects.filter(tender=tender_id):
        isWeekday = unit.fromdate.weekday() < 5
        drop = bid_round.min_drop_wkdy if isWeekday else bid_round.min_drop_wknd
        bid_row = {}
        for amount in AMOUNTS:
            try:
                our_last_bid = OurBid.objects.get(o_unit=unit, o_amount=amount, o_bid_round__number=bid_round.number-1)
                price = our_last_bid.o_price - drop
                out = False
            except OurBid.DoesNotExist:
                price = bid_round.max_price_wkdy if isWeekday else bid_round.max_price_wknd
                out = tender.current_bid_round != 1
            price = 0 if out else price
            bid_row[amount] = price
        bid_table.append(bid_row)
    return bid_table


def make_bid(bids, tender_id):
    try:
        tender = Tender.objects.get(pk=tender_id)
        create_our_bids(tender, bids)
        bid_table = pandas.read_excel(tender.bid_file, engine='openpyxl', sheet_name='PROPOSAL')
        info_sheet = pandas.read_excel(tender.bid_file, engine='openpyxl', sheet_name='INFO')
        info_sheet.iloc[7, 1] = tender.current_bid_round
        for i, unit in enumerate(Unit.objects.filter(tender=tender)):
            bid_table.at[i, '5 MW'] = bids[i]['5']
            bid_table.at[i, '10 MW'] = bids[i]['10']
            bid_table.at[i, '15 MW'] = bids[i]['15']
        filepath = '{0}/bids_{1}_{2}_{3}_{4}.xlsx'.format(settings.MEDIA_ROOT, tender.datestr, tender.market, tender.direction, tender.tender_round) 
        with pandas.ExcelWriter(filepath) as writer:
            info_sheet.to_excel(writer, index=False, sheet_name='INFO')
            bid_table.to_excel(writer, index=False, sheet_name='PROPOSAL')
        return filepath
    except:
        printException()
        raise


def printException():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print("Exception in {0} at line {1}: {2}".format(fname, exc_tb.tb_lineno,  exc_obj))