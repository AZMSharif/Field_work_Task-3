"""
Mock database and data structures for LogiTrack AI.
"""

ORDERS = {
    "ORD-7001": {
        "customer_name": "Riya Sharma",
        "customer_email": "riya.sharma@email.com",
        "items": [
            {"name": "Wireless Earbuds Pro", "sku": "WEP-200", "qty": 1, "price": 79.99}
        ],
        "total": 79.99,
        "order_date": "2026-07-01",
        "shipping_address": "42 Lake View Rd, Dhaka 1205",
        "status": "shipped",
    },
    "ORD-7002": {
        "customer_name": "Riya Sharma",
        "customer_email": "riya.sharma@email.com",
        "items": [
            {"name": "Mechanical Keyboard RGB", "sku": "MKR-500", "qty": 1, "price": 149.99},
            {"name": "USB-C Hub 7-in-1", "sku": "UCH-710", "qty": 1, "price": 45.00},
        ],
        "total": 194.99,
        "order_date": "2026-07-05",
        "shipping_address": "42 Lake View Rd, Dhaka 1205",
        "status": "delivered",
    },
    "ORD-7003": {
        "customer_name": "Tanvir Hasan",
        "customer_email": "tanvir.h@email.com",
        "items": [
            {"name": "Ergonomic Office Chair", "sku": "EOC-100", "qty": 1, "price": 249.50}
        ],
        "total": 249.50,
        "order_date": "2026-06-28",
        "shipping_address": "15/A Banani, Dhaka 1213",
        "status": "delivered",
    },
    "ORD-7004": {
        "customer_name": "Sarah Miller",
        "customer_email": "smiller.design@email.com",
        "items": [
            {"name": "Smart Watch Elite", "sku": "SWE-300", "qty": 1, "price": 299.00}
        ],
        "total": 299.00,
        "order_date": "2026-07-10",
        "shipping_address": "78 Gulshan Ave, Dhaka 1212",
        "status": "processing",
    },
    "ORD-7005": {
        "customer_name": "Arif Rahman",
        "customer_email": "arif.r@email.com",
        "items": [
            {"name": "Bluetooth Speaker Mini", "sku": "BSM-400", "qty": 2, "price": 29.99}
        ],
        "total": 59.98,
        "order_date": "2026-07-11",
        "shipping_address": "90 Mirpur Rd, Dhaka 1216",
        "status": "shipped",
    },
}

SHIPMENTS = {
    "ORD-7001": {
        "tracking_id": "FDX-998877",
        "carrier": "FedEx",
        "status": "in_transit",
        "current_location": "Sorting Hub — Chittagong",
        "estimated_delivery": "2026-07-16",
        "shipped_date": "2026-07-02",
        "events": [
            {"date": "2026-07-02", "event": "Picked up from warehouse WH-Dhaka-01"},
            {"date": "2026-07-03", "event": "Arrived at Chittagong sorting hub"},
            {"date": "2026-07-05", "event": "In transit to destination city"},
        ]
    },
    "ORD-7002": {
        "tracking_id": "DHL-554433",
        "carrier": "DHL",
        "status": "delivered",
        "current_location": "Delivered",
        "delivered_date": "2026-07-10",
        "shipped_date": "2026-07-06",
        "signature": "R. Sharma",
        "events": [
            {"date": "2026-07-06", "event": "Picked up from warehouse WH-Dhaka-01"},
            {"date": "2026-07-08", "event": "Out for delivery"},
            {"date": "2026-07-10", "event": "Delivered — signed by R. Sharma"},
        ]
    },
    "ORD-7003": {
        "tracking_id": "UPS-112233",
        "carrier": "UPS",
        "status": "delivered",
        "current_location": "Delivered",
        "delivered_date": "2026-07-02",
        "shipped_date": "2026-06-29",
        "signature": "Front Desk / Reception",
        "events": [
            {"date": "2026-06-29", "event": "Picked up from warehouse WH-Dhaka-01"},
            {"date": "2026-07-02", "event": "Delivered to reception desk"},
        ]
    },
    "ORD-7004": {
        "tracking_id": "FDX-123456",
        "carrier": "FedEx",
        "status": "exception",
        "current_location": "Customs Clearance — Dhaka Airport",
        "estimated_delivery": "Delayed",
        "shipped_date": "2026-07-11",
        "events": [
            {"date": "2026-07-11", "event": "Picked up from warehouse WH-Dhaka-01"},
            {"date": "2026-07-12", "event": "Exception: Held at customs, pending documentation"},
        ]
    },
    "ORD-7005": {
        "tracking_id": "DHL-987654",
        "carrier": "DHL",
        "status": "in_transit",
        "current_location": "Local Dispatch Facility",
        "estimated_delivery": "2026-07-14",
        "shipped_date": "2026-07-12",
        "events": [
            {"date": "2026-07-12", "event": "Picked up from warehouse WH-Dhaka-01"},
            {"date": "2026-07-13", "event": "Arrived at local dispatch facility"},
        ]
    },
}

WAREHOUSE = {
    "WEP-200": {"name": "Wireless Earbuds Pro", "stock": 45, "location": "Aisle 4, Bin B"},
    "MKR-500": {"name": "Mechanical Keyboard RGB", "stock": 7, "location": "Aisle 12, Bin A"},
    "UCH-710": {"name": "USB-C Hub 7-in-1", "stock": 120, "location": "Aisle 2, Bin C"},
    "EOC-100": {"name": "Ergonomic Office Chair", "stock": 0, "location": "Aisle 22, Bulk (OUT OF STOCK)"},
    "SWE-300": {"name": "Smart Watch Elite", "stock": 15, "location": "Aisle 5, Bin A"},
    "BSM-400": {"name": "Bluetooth Speaker Mini", "stock": 30, "location": "Aisle 6, Bin C"},
    "NCH-800": {"name": "Noise Cancelling Headphones", "stock": 25, "location": "Aisle 4, Bin A"},
}

CLAIMS = {}

FRAUD_HISTORY = {
    "arif.r@email.com": {
        "claims_this_quarter": 4,
        "flagged_reason": "Excessive damage claims without photographic proof",
        "status": "restricted"
    },
    "tanvir.h@email.com": {
        "claims_this_quarter": 1,
        "status": "good_standing"
    }
}

reshipment_log = []
