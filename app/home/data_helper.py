from datetime import datetime
from .. import db

from ..models import Staff, Member, Group, Church, Pcf, Cell, PartnerGiving, PartnershipArm

from sqlalchemy import or_
from sqlalchemy import text

colors = [
    "#f56954", "#00a65a", "#f39c12", "#00c0ef",
    "#3c8dbc", "#FEDCBA", "#FDB45C", "#4169E1",
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


def get_top_partners():

    query = """

    select CONCAT( t2.title, " " , t2.f_name , " " ,  t2.l_name ) AS m_name, SUM(t1.amount) AS total
    FROM partner_givings t1
    JOIN members t2 ON t1.`member_id` = t2.`id`
    WHERE is_pledge=0 GROUP BY t1.member_id
    ORDER BY total DESC LIMIT 10

    """

    sql = text(query)
    result = db.engine.execute(sql)
    members = [list(row) for row in result]

    member_count = len(members)
    if member_count < 10:
        diff = 10 - member_count
        b = [[ '', '']]* diff
        members += b


    return members

def get_total_monthly_partnership():

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    query = """

    select MONTH(entry_date) AS emonth, SUM(amount) AS total
    FROM partner_givings WHERE YEAR(entry_date) = 2019 AND is_pledge=0
    GROUP BY YEAR(entry_date), MONTH(entry_date)


    """

    sql = text(query)
    result = db.engine.execute(sql)
    monthly_givings = [list(row) for row in result]

    count = 0
    for mg in monthly_givings:
        mg[0] = months[count]
        count += 1
    return monthly_givings

def get_partnership_by_arms():

    query = """

    select t2.partnership_arm AS arm, SUM(t1.amount) AS total
    FROM partner_givings AS t1
    JOIN partnership_arms AS t2
    ON t1.`arm_id` = t2.`id`
    WHERE YEAR(t1.entry_date) = 2019 AND t1.is_pledge=0
    GROUP BY t2.`partnership_arm`

    """

    sql = text(query)
    result = db.engine.execute(sql)
    monthly_givings = [list(row) for row in result]
    ch_colors = colors[:len(monthly_givings)]

    return monthly_givings, ch_colors

def get_partnership_by_pcfs():

    query = """

    select t3.pcf AS pcf, SUM(t1.amount) AS amount FROM
    partner_givings AS t1
    JOIN
    (
    SELECT t9.pcf AS pcf, t2.cell_id AS cell,t2.`id` AS m_id
    FROM members AS t2
    JOIN pcfs AS t9
    ON t9.`id`=t2.`pcf_id`
    ) AS t3
    ON t1.`member_id` = t3.m_id
    WHERE t1.`is_pledge`=0
    GROUP BY t3.pcf

    """

    sql = text(query)
    result = db.engine.execute(sql)
    monthly_givings = [list(row) for row in result]
    ch_colors = colors[:len(monthly_givings)]

    return monthly_givings, ch_colors


