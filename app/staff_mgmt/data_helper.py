from datetime import datetime
from .. import db

from ..models import Staff, Member, Group, Church, Pcf, Cell, PartnerGiving, PartnershipArm

from sqlalchemy import or_
from sqlalchemy import text

def get_staff_details():
    query = """

    SELECT
    t1.`id`,
    CONCAT(t1.f_name, " ", t1.l_name) AS sname,
    t2.role AS role,
    t1.phone, t1.email

    FROM staffs t1

    JOIN staff_roles t2
    ON t1.role_id = t2.`id`

    """
    sql = text(query)
    result = db.engine.execute(sql)
    staff = [list(row) for row in result]
    # print(members)
    # print(get_p_table_header())

    return staff
