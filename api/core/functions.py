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
        set_unit_stopped_on_update(tender)
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
            bid_round = BidRound.objects.get(tender=tender, number=bid_round),
            unit = Unit.objects.get(tender=tender, fromdate = round_table['fromdate'][i])
        )


def create_our_bids(tender, bids):
    print("create_our_bids...")
    for i, unit in enumerate(Unit.objects.filter(tender=tender)):
        for amount in AMOUNTS:
            our_bid, _ = OurBid.objects.update_or_create(
                o_price = bids[i][str(amount)],
                o_amount = amount,
                o_bid_round = BidRound.objects.get(tender=tender, number=tender.current_bid_round),
                o_unit = unit
            )
            set_unit_stopped(our_bid)


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


def set_unit_stopped(our_bid):
    if our_bid.o_bid_round.number == 1:
        isWeekday = our_bid.o_unit.fromdate.weekday() < 5
        max_price = our_bid.o_bid_round.max_price_wkdy if isWeekday else our_bid.o_bid_round.max_price_wknd
        if our_bid.o_price > max_price:
            our_bid.o_unit.stopped = True
            our_bid.o_unit.save()
    else:
        isWeekday = our_bid.o_unit.fromdate.weekday() < 5
        min_drop = our_bid.o_bid_round.min_drop_wkdy if isWeekday else our_bid.o_bid_round.min_drop_wknd
        prev_bid_round = BidRound.objects.get(tender=our_bid.o_unit.tender, number=our_bid.o_bid_round.number-1)
        our_prev_bid = OurBid.objects.get(o_bid_round=prev_bid_round, o_unit=our_bid.o_unit, o_amount=our_bid.o_amount)
        if our_prev_bid.o_price - our_bid.o_price < min_drop:
            our_bid.o_unit.stopped = True
            our_bid.o_unit.save() 


def set_unit_stopped_on_update(tender):
    prev_bid_round = BidRound.objects.get(tender=tender, number=tender.current_bid_round-1)
    for unit in Unit.objects.filter(tender=tender):
        if not OurBid.objects.filter(o_unit=unit, o_bid_round=prev_bid_round):
            unit.stopped = True
            unit.save()


def our_last_bid(unit, amount):
    try:
        last_bid = OurBid.objects.filter(o_unit=unit, o_amount=amount)[0]
        return last_bid.o_price
    except:
        return 0


def initial_bids(tender_id):
    tender = Tender.objects.get(pk=tender_id)
    bid_round = BidRound.objects.get(tender=tender, number=tender.current_bid_round)
    bid_table = []
    for unit in Unit.objects.filter(tender=tender_id):
        bid_row = {}
        isWeekday = unit.fromdate.weekday() < 5
        for amount in AMOUNTS:
            if bid_round.number == 1:
                bid_row[amount] = bid_round.max_price_wkdy if isWeekday else bid_round.max_price_wknd
            else:
                try:
                    our_prev_bid = OurBid.objects.get(o_unit=unit, o_amount=amount, o_bid_round__number=bid_round.number-1)
                    drop = bid_round.min_drop_wkdy if isWeekday else bid_round.min_drop_wknd
                    bid_row[amount] = our_prev_bid.o_price if unit.stopped else our_prev_bid.o_price - drop
                except OurBid.DoesNotExist:
                    bid_row[amount] = our_last_bid(unit, amount)
        bid_table.append(bid_row)
    return bid_table


def make_bid(bids, tender_id):
    try:
        tender = Tender.objects.get(pk=tender_id)
        create_our_bids(tender, bids)
        proposal_table = pandas.read_excel(tender.bid_file, engine='openpyxl', sheet_name='PROPOSAL', header=None)
        info_table = pandas.read_excel(tender.bid_file, engine='openpyxl', sheet_name='INFO', header=None)
        info_table.iloc[8, 1] = tender.current_bid_round
        for i, unit in enumerate(Unit.objects.filter(tender=tender)):
            proposal_table.at[i+1, 3] = bids[i]['5']
            proposal_table.at[i+1, 4] = bids[i]['10']
            proposal_table.at[i+1, 5] = bids[i]['15']
        filepath = '{0}/bids_{1}_{2}_{3}_{4}.xlsx'.format(settings.MEDIA_ROOT, tender.datestr, tender.market, tender.direction, tender.tender_round) 
        with pandas.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            info_table.to_excel(writer, sheet_name='INFO', header=False, index=False)
            proposal_table.to_excel(writer, sheet_name='PROPOSAL', header=False, index=False)
            format_bid_file(writer, info_table, proposal_table)
        return filepath
    except:
        printException()
        raise


def format_bid_file(writer, info_table, proposal_table):
    workbook = writer.book
    info_sheet = writer.sheets['INFO']
    proposal_sheet = writer.sheets['PROPOSAL']
    plain_text = workbook.add_format({'bold': False})
    for i, width in enumerate(get_col_widths(info_table)):
        info_sheet.set_column(i, i, width, plain_text)
    for i, width in enumerate(get_col_widths(proposal_table)):
        proposal_sheet.set_column(i, i, width, plain_text)
    writer.save()


def get_col_widths(dataframe):
    return [max([len(str(cell).strip()) for cell in dataframe[col]]) + 1 for col in dataframe]


def printException():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print("Exception in {0} at line {1}: {2}".format(fname, exc_tb.tb_lineno,  exc_obj))