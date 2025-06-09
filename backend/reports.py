# reports.py
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app import db

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

# Utility function to execute view queries


def execute_view_query(view_name):
    try:
        query = text(f"SELECT * FROM {view_name}")
        result = db.session.execute(query)
        return [dict(row._mapping) for row in result]
    except Exception as e:
        raise e

# ========== INVENTORY REPORTS ==========


@reports_bp.route('/inventory/expired')
def get_expired_inventory():
    """Get expired inventory items"""
    try:
        data = execute_view_query('v_inventory_expired')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/inventory/low-stock')
def get_low_stock():
    """Get low stock items (below reorder point)"""
    try:
        data = execute_view_query('v_low_stock')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/inventory/out-of-stock')
def get_out_of_stock():
    """Get products that are completely out of stock"""
    try:
        data = execute_view_query('v_products_out_of_stock')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/inventory/by-category')
def get_inventory_by_category():
    """Get inventory breakdown by category"""
    try:
        data = execute_view_query('v_inventory_by_category')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/inventory/days-of-supply')
def get_days_of_supply():
    """Get days of supply for products"""
    try:
        data = execute_view_query('v_product_days_of_supply')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/inventory/idle-60d')
def get_idle_inventory():
    """Get idle inventory (no movement in 60 days)"""
    try:
        data = execute_view_query('v_idle_inventory_60d')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/inventory/expiry-alert')
def get_expiry_alert():
    """Get lots expiring within 30 days"""
    try:
        data = execute_view_query('v_lot_expiry_alert')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== SALES REPORTS ==========


@reports_bp.route('/sales/30d')
def get_sales_30d():
    """Get sales summary for last 30 days"""
    try:
        data = execute_view_query('v_sales_30d')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/sales/fast-moving-top10')
def get_fast_moving_products():
    """Get top 10 fast moving products in last 30 days"""
    try:
        data = execute_view_query('v_fast_moving_top10')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/sales/avg-order-value-by-customer-type')
def get_avg_order_value_by_customer_type():
    """Get average order value by customer type"""
    try:
        data = execute_view_query('v_avg_order_value_by_cust_type')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== ORDER REPORTS ==========


@reports_bp.route('/orders/pending')
def get_pending_orders():
    """Get pending orders"""
    try:
        data = execute_view_query('v_orders_pending')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/orders/unshipped-today')
def get_unshipped_today():
    """Get orders scheduled to ship today but not yet shipped"""
    try:
        data = execute_view_query('v_orders_unshipped_today')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/orders/status-7d')
def get_orders_status_7d():
    """Get order status statistics for last 7 days"""
    try:
        data = execute_view_query('v_orders_status_7d')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/orders/delayed-shipping')
def get_delayed_shipping():
    """Get orders with delayed shipping (pending for more than 3 days)"""
    try:
        data = execute_view_query('v_orders_delayed_shipping')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/orders/to-ship-this-week')
def get_orders_to_ship_this_week():
    """Get orders scheduled to ship this week"""
    try:
        data = execute_view_query('v_orders_to_ship_this_week')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/orders/processing-time')
def get_avg_processing_time():
    """Get average order processing time by day"""
    try:
        data = execute_view_query('v_avg_order_processing_time')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== SHIPMENT REPORTS ==========


@reports_bp.route('/shipments/today')
def get_today_shipments():
    """Get today's shipments"""
    try:
        data = execute_view_query('v_shipments_today')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/shipments/vendor-delays')
def get_vendor_delays():
    """Get shipping vendor delay counts"""
    try:
        data = execute_view_query('v_vendor_delay_cnt')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== LOCATION REPORTS ==========


@reports_bp.route('/locations/over-capacity')
def get_locations_over_capacity():
    """Get locations that are at or over capacity"""
    try:
        data = execute_view_query('v_locations_over_capacity')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== SCRAP REPORTS ==========


@reports_bp.route('/scrap/cost-month')
def get_scrap_cost_month():
    """Get scrap cost summary for current month"""
    try:
        data = execute_view_query('v_scrap_cost_month')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/scrap/product-scrap-rate')
def get_product_scrap_rate():
    """Get scrap rate by product"""
    try:
        data = execute_view_query('v_product_scrap_rate')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== CUSTOMER REPORTS ==========


@reports_bp.route('/customers/last-order')
def get_customer_last_order():
    """Get customer last order dates"""
    try:
        data = execute_view_query('v_customer_last_order')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== SUPPLIER REPORTS ==========


@reports_bp.route('/suppliers/product-variants')
def get_supplier_product_variants():
    """Get supplier product variant counts"""
    try:
        data = execute_view_query('v_supplier_product_variants')
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== COMBINED REPORTS ==========


@reports_bp.route('/summary/inventory')
def get_inventory_summary():
    """Get comprehensive inventory summary"""
    try:
        expired = execute_view_query('v_inventory_expired')
        low_stock = execute_view_query('v_low_stock')
        out_of_stock = execute_view_query('v_products_out_of_stock')
        over_capacity = execute_view_query('v_locations_over_capacity')

        return jsonify({
            'success': True,
            'data': {
                'expired_items': expired,
                'low_stock_items': low_stock,
                'out_of_stock_products': out_of_stock,
                'over_capacity_locations': over_capacity,
                'summary': {
                    'expired_count': len(expired),
                    'low_stock_count': len(low_stock),
                    'out_of_stock_count': len(out_of_stock),
                    'over_capacity_count': len(over_capacity)
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/summary/orders')
def get_orders_summary():
    """Get comprehensive orders summary"""
    try:
        pending = execute_view_query('v_orders_pending')
        unshipped_today = execute_view_query('v_orders_unshipped_today')
        delayed = execute_view_query('v_orders_delayed_shipping')
        this_week = execute_view_query('v_orders_to_ship_this_week')

        return jsonify({
            'success': True,
            'data': {
                'pending_orders': pending,
                'unshipped_today': unshipped_today,
                'delayed_orders': delayed,
                'this_week_shipments': this_week,
                'summary': {
                    'pending_count': len(pending),
                    'unshipped_today_count': len(unshipped_today),
                    'delayed_count': len(delayed),
                    'this_week_count': len(this_week)
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/summary/sales')
def get_sales_summary():
    """Get comprehensive sales summary"""
    try:
        sales_30d = execute_view_query('v_sales_30d')
        fast_moving = execute_view_query('v_fast_moving_top10')
        avg_order_value = execute_view_query('v_avg_order_value_by_cust_type')

        return jsonify({
            'success': True,
            'data': {
                'sales_30d': sales_30d,
                'fast_moving_products': fast_moving,
                'avg_order_value_by_type': avg_order_value,
                'summary': {
                    'sales_days_count': len(sales_30d),
                    'top_products_count': len(fast_moving),
                    'customer_types_count': len(avg_order_value)
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/summary/financial')
def get_financial_summary():
    """Get comprehensive financial summary"""
    try:
        scrap_cost = execute_view_query('v_scrap_cost_month')
        scrap_rate = execute_view_query('v_product_scrap_rate')
        avg_order_value = execute_view_query('v_avg_order_value_by_cust_type')

        return jsonify({
            'success': True,
            'data': {
                'monthly_scrap_cost': scrap_cost,
                'product_scrap_rates': scrap_rate,
                'avg_order_values': avg_order_value,
                'summary': {
                    'scrap_cost_records': len(scrap_cost),
                    'products_with_scrap': len(scrap_rate),
                    'customer_segments': len(avg_order_value)
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
