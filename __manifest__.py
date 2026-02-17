{
    'name': 'Real-Time Margin Dashboard',
    'version': '1.0',
    'summary': 'Architectural task for Sales Margin with Cost Breakdown',
    'description': """
        - Smart Margin Card in Sales Order
        - Real-time COGS and Overhead calculation
        - Detailed cost breakdown popup
        - Portal visibility for managers
    """,
    'category': 'Sales',
    'author': 'Your Name',
    'depends': [
        'sale_management', 
        'stock_account', 
        'stock_landed_costs', 
        'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # This is where we will add OWL JS files later if needed
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}