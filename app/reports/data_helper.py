from datetime import datetime
from .. import db

from ..models import Staff, Member, Group, Church, Pcf, Cell, PartnerGiving, PartnershipArm

from sqlalchemy import or_
from sqlalchemy import text



def get_partnerships():

    p_arms = PartnershipArm.query.with_entities(PartnershipArm.id, PartnershipArm.partnership_arm).all()

    return p_arms

def get_members_data():
    query = """

    SELECT
    t1.id AS id,
    CONCAT(t1.title, ' ', t1.f_name, ' ', t1.l_name) AS NAME,

    t5.pcf AS pcf,
    t2.cell AS cell,
    t1.phone AS phone,
    t1.email AS email

    FROM members t1


    JOIN cells t2
    ON t1.`cell_id` = t2.`id`
    JOIN pcfs t5
    ON t1.pcf_id = t5.`id`

    """
    sql = text(query)
    result = db.engine.execute(sql)
    members = [list(row) for row in result]
    # print(members)
    # print(get_p_table_header())

    return members

def get_member_data(m_id):
    query = """

    SELECT
    t1.id AS id,
    CONCAT(t1.title, ' ', t1.f_name, ' ', t1.l_name) AS NAME,

    t6.`group` AS mgroup,
    t7.`church` AS church,
    t5.pcf AS pcf,
    t2.cell AS cell,
    t1.phone AS phone,
    t1.email AS email,
    t1.`kingschat_no` AS kchat

    FROM members t1

    JOIN cells t2
    ON t1.`cell_id` = t2.`id`
    JOIN pcfs t5
    ON t1.pcf_id = t5.`id`
    JOIN groups t6
    ON t1.`group_id` = t6.`id`
    JOIN churches t7
    ON t1.`church_id` = t7.`id`

    WHERE t1.`id`={m_id}

    """.format(m_id=m_id)

    sql = text(query)
    result = db.engine.execute(sql)
    members = [list(row) for row in result]
    member_data = members[0]
    # print(members)
    # print(get_p_table_header())

    return member_data

def get_monthly_partnership(m_id):

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    query = """

    SELECT MONTH(entry_date) AS emonth, SUM(amount) AS total
    FROM partner_givings WHERE YEAR(entry_date) = 2019 AND is_pledge=0 AND member_id={m_id}
    GROUP BY YEAR(entry_date), MONTH(entry_date)


    """.format(m_id=m_id)

    sql = text(query)
    result = db.engine.execute(sql)
    monthly_givings = [list(row) for row in result]

    max_index = len(monthly_givings) - 1
    max_month = monthly_givings[max_index][0]
    # print("max: "+str(max_month)+" month: "+months[int(max_month)-1])

    avail_months = months[:max_month]
    monthly_data = [ [m, '0'] for m in avail_months ]
    # print(monthly_data)
    # count = 0
    for mg in monthly_givings:
        m_index = mg[0] - 1
        monthly_data[m_index][1] = mg[1]
    # print("init: ", monthly_givings)
    # print(monthly_data)
    return monthly_data


def get_arm_count():
    query= "select COUNT(DISTINCT(partnership_arm)) FROM partnership_arms"
    sql = text(query)
    result = db.engine.execute(sql)

    arm_count = 0
    for i in result:
        arm_count = i[0]
    # print("COunt: ",arm_count)
    return arm_count

def get_arm_count_by_member(m_id):
    query= "SELECT DISTINCT(arm_id) FROM partner_givings WHERE member_id={m_id}".format(m_id=m_id)
    sql = text(query)
    result = db.engine.execute(sql)

    arms = [ arm[0] for arm in result]
    # print("COunt: ",arm_count)
    return arms

def get_arms():
    query= "SELECT partnership_arm FROM partnership_arms"
    sql = text(query)
    result = db.engine.execute(sql)
    arms = [arm[0].strip() for arm in result]
    # print(arms)
    # print("COunt: ",arm_count)
    return arms

def get_partnership_amount(m_id, arm):

    query ="""

    select
    SUM(t1.amount) AS pledge16,
    t2.pledge AS give16
    FROM partner_givings t1
    JOIN
    (SELECT SUM(amount) AS pledge FROM partner_givings WHERE arm_id={arm} AND is_pledge=0 AND member_id={m_id} ) t2
    WHERE t1.`arm_id`={arm} AND t1.`is_pledge`=1  AND t1.member_id={m_id}

    """.format(arm=arm, m_id=m_id)

    # print("query: ", query)
    pledge = 0
    giving = 0
    sql = text(query)
    result = db.engine.execute(sql)
    # print("Memebr: ",m_id)
    for res in result:
        # print(res)
        pledge = str(res[0]) if res[0] != None else '0'
        giving = str(res[1]) if res[1] != None else '0'
        # print("Giving: "+str(giving)+" Pledge: "+str(pledge))

    return pledge, giving

def get_partnership_amount_by_date(m_id, arm, start, end):

    query ="""

    select
    SUM(t1.amount) AS pledge16,
    t2.pledge AS give16
    FROM partner_givings t1
    JOIN
    (SELECT SUM(amount) AS pledge FROM partner_givings WHERE arm_id={arm} AND is_pledge=0 AND member_id={m_id} and entry_date BETWEEN "{start}" AND "{end}" ) t2
    WHERE t1.`arm_id`={arm} AND t1.`is_pledge`=1  AND t1.member_id={m_id} and t1.entry_date BETWEEN "{start}" AND "{end}"

    """.format(arm=arm, m_id=m_id, start=start, end=end)

    # print("query: ", query)
    pledge = 0
    giving = 0
    sql = text(query)
    result = db.engine.execute(sql)
    # print("Memebr: ",m_id)
    for res in result:
        # print(res)
        pledge = str(res[0]) if res[0] != None else '0'
        giving = str(res[1]) if res[1] != None else '0'
        # print("Giving: "+str(giving)+" Pledge: "+str(pledge))

    return pledge, giving


def get_member_partnership(m_id):

    # get arms member has given for
    p_arms = db.session.query(PartnerGiving.arm_id).filter_by(member_id=m_id).distinct().all()
    arms = [arm[0] for arm in p_arms]

    #total amounts for giving n pledge
    total_pledge = 0
    total_giving = 0

    # get total no of arms
    arm_count = get_arm_count()
    # p_amounts = ['0'] * arm_count * 2
    giving_amounts = ['0'] * arm_count
    pledge_amounts = ['0'] * arm_count

    for arm in arms:
        pledge, giving = get_partnership_amount(m_id, arm)
        index = (arm-1)
        total_pledge += float(pledge)
        total_giving += float(giving)
        pledge_amounts[index] = pledge
        giving_amounts[index] = giving

    # print("Member:  ", m_id)
    # print("Total g: "+str(total_giving)+" Totla pled: "+str(total_pledge))
    pledge_amounts.append(str(total_pledge))
    giving_amounts.append(str(total_giving))
    # print(p_amounts)
    arms = get_arms()
    arms.append('TOTAL')

    return zip(arms,pledge_amounts, giving_amounts)

def get_member_partnership_by_date(m_id, start, end):

    query = """

    select DISTINCT(arm_id) FROM partner_givings WHERE
    member_id={m_id} AND
    entry_date BETWEEN "{start}" AND "{end}"

    """.format(m_id=m_id, start=start, end=end)

    sql = text(query)
    p_arms = db.engine.execute(sql)

    # get arms member has given for

    # p_arms = db.session.query(PartnerGiving.arm_id).filter_by(member_id=m_id).distinct().all()

    arms = [arm[0] for arm in p_arms]
    # print("Arms: ", arms)

    #total amounts for giving n pledge
    total_pledge = 0
    total_giving = 0

    # get total no of arms
    arm_count = get_arm_count()
    p_amounts = ['0'] * arm_count * 2

    for arm in arms:
        pledge, giving = get_partnership_amount_by_date(m_id, arm, start, end)
        index = (arm-1) * 2
        total_pledge += float(pledge)
        total_giving += float(giving)
        p_amounts[index] = pledge
        p_amounts[index+1] = giving

    # print("Member:  ", m_id)
    # print("Total g: "+str(total_giving)+" Totla pled: "+str(total_pledge))
    p_amounts.append(str(total_pledge))
    p_amounts.append(str(total_giving))
    # print(p_amounts)

    return p_amounts


def get_partnership_data():

    member_info = get_members_data()

    partner_table_data = []
    count = 1

    for info in member_info:

        partner_data = get_member_partnership(info[0])
        info[0] = count
        full_info = info+partner_data
        partner_table_data.append(full_info)
        count += 1
        # print(full_info)

    # print(partner_table_data)
    return partner_table_data

def get_partnership_data_by_date(start, end):

    member_info = get_members_data_by_date(start, end)

    partner_table_data = []
    count = 1

    for info in member_info:

        partner_data = get_member_partnership_by_date(info[0], start, end)
        info[0] = count
        full_info = info+partner_data
        partner_table_data.append(full_info)
        count += 1
        # print(full_info)

    # print("Final: ",partner_table_data)
    return partner_table_data
