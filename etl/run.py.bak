from etl.settings import OWS_GRAPHQL_URL, OWS_TOKEN
from etl.ows_client import OWSGQLClient
from etl.db import connect, upsert_raw
from etl.settings import dsn


def main():
    print("MAIN START")
    gql = OWSGQLClient(OWS_GRAPHQL_URL, OWS_TOKEN)
    print("GQL CREATED", gql)
    conn = connect(dsn())

    q_subjects = """
    query {
      Subjects(limit: 5) {
        pid
        bin
        nameRu
      }
    }
    """

    try:
        data_subjects = gql.query(q_subjects)
        upsert_raw(
           conn=conn,
           source="Subjects",
           bin_="N/A",
           external_id="limit_5",
           payload=data_subjects,
           updated_at=None,
        )
        print("saved Subjects raw")
    except Exception as e:
        print("skip Subjects:", str(e)[:120])

    q_plans = """
    query {
      Plans(limit: 5) {
        id
      }
    }
    """

    try:
        data_plans = gql.query(q_plans)
        upsert_raw(
            conn=conn,
            source="Plans",
            bin_="N/A",
            external_id="limit_5",
            payload=data_plans,
            updated_at=None,
        )
        print("saved Plans raw")
    except Exception as e:
        print("skip Plans:", str(e)[:120])

    q_lots = """
    query {
      Lots(limit: 5) {
        id
      }
    }
    """

    try:
        data_lots = gql.query(q_lots)
        upsert_raw(
            conn=conn,
            source="Lots",
            bin_="N/A",
            external_id="limit_5",
            payload=data_lots,
            updated_at=None,
        )
        print("saved Lots raw")
    except Exception as e:
        print("skip Lots:", str(e)[:120])

    q_contracts = """
    query {
      Contract(limit: 5) {
        id
      }
    }
    """

    try: 
        data_contracts = gql.query(q_contracts)
        upsert_raw(
            conn=conn,
            source="Contract",
            bin_="N/A",
            external_id="limit_5",
            payload=data_contracts,
            updated_at=None,
        )
        print("saved Contract raw")
    except Exception as e:
        print("skip Contract:", str(e)[:120])

    q_trdbuy = """
    query {
      TrdBuy(limit: 5) {
        id
      }
    }
    """

    try:
        data_trdbuy = gql.query(q_trdbuy)
        upsert_raw(
            conn=conn,
            source="TrdBuy",
            bin_="N/A",
            external_id="limit_5",
            payload=data_trdbuy,
            updated_at=None,
        )
        print("saved TrdBuy raw")
    except Exception as e:
        print("skip TrdBuy:", str(e)[:120])

    q_obtrdbuy = """
    query {
      ObTrdBuy(limit: 5) {
        id
      }
    }
    """

    try:
        data_obtrdbuy = gql.query(q_obtrdbuy)
        upsert_raw(
            conn=conn,
            source="ObTrdBuy",
            bin_="N/A",
            external_id="limit_5",
            payload=data_obtrdbuy,
            updated_at=None,
        )
        print("saved ObTrdBuy raw")
    except Exception as e:
        print("skip ObTrdBuy:", str(e)[:120])

    q_customers = """
    query {
      Subjects(limit: 5) {
        pid
        bin
        nameRu
        customer
        supplier
        typeSupplier
      }
    }
    """

    try:
        data_customers = gql.query(q_customers)
        upsert_raw(
            conn=conn,
            source="Customers",
            bin_="N/A",
            external_id="limit_5",
            payload=data_customers,
            updated_at=None,
        )
        print("saved Customers raw")
    except Exception as e:
        print("skip Customers:", str(e)[:120])

    q_suppliers = """
    query {
      Subjects(limit: 5) {
        pid
        bin
        nameRu
        supplier
        customer
        typeSupplier
      }
    }
    """

    try:
        data_suppliers = gql.query(q_suppliers)
        upsert_raw(
            conn=conn,
            source="Suppliers",
            bin_="N/A",
            external_id="limit_5_suppliers",
            payload=data_suppliers,
            updated_at=None,
        )
        print("saved Suppliers raw")
    except Exception as e:
        print("skip Suppliers:", str(e)[:120])


if __name__ == "__main__":
    main()
