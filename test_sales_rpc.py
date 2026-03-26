#!/usr/bin/env python3
"""
Test directo del RPC de sales
"""
import sys
import os
sys.path.insert(0, 'layers/shared')
sys.path.insert(0, 'src')

from dotenv import load_dotenv
load_dotenv()

from db.db_client import DBClient

db_client = DBClient.get_client()

print("Testing RPC get_sales_cpr...")

rpc_params = {
    "p_id_sale": None,
    "p_search": None,
    "p_limit": 10,
    "p_offset": 0,
    "p_record_type": "sale",
    "p_payment_method": None
}

print(f"Params: {rpc_params}")

try:
    response = db_client.rpc("get_sales_cpr", rpc_params).execute()
    print(f"Response type: {type(response)}")
    print(f"Response: {response}")
    if response:
        print(f"Response.data type: {type(response.data)}")
        print(f"Response.data: {response.data}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
