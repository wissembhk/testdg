
from utils.prod_connection import sessionLocalProd


async def get_productname_by_id(id: int):
    with sessionLocalProd() as session:
        try:
            statement = "select name from superproducts where id = " + \
                str(id)+" limit 1"
            product_name = session.execute(statement).first()
            if (product_name):
                return (product_name[0])
            return ("NA")
        except Exception as e:
            return e
