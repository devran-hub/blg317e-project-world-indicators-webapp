import json
from db_utils import execute

def submit_change(table_name, action_type, data, record_id=None):
    """
    Submits a change to the PendingChanges table.
    action_type: 'INSERT', 'UPDATE', 'DELETE'
    data: dict containing the data
    record_id: primary key of the record (for UPDATE/DELETE)
    """
    return execute(
        """
        INSERT INTO PendingChanges (table_name, action_type, record_id, data_json)
        VALUES (%s, %s, %s, %s)
        """,
        (table_name, action_type, str(record_id) if record_id else None, json.dumps(data))
    )

def get_pending_changes():
    """Retrieves all pending changes."""
    return execute(
        "SELECT * FROM PendingChanges WHERE status = 'PENDING' ORDER BY created_at DESC",
        fetch=True
    )

def get_pending_change_by_id(change_id):
    """Retrieves a single pending change."""
    result = execute(
        "SELECT * FROM PendingChanges WHERE id = %s",
        (change_id,),
        fetch=True
    )
    return result[0] if result else None

def reject_change(change_id):
    """Deletes a pending change."""
    return execute("DELETE FROM PendingChanges WHERE id = %s", (change_id,))

def approve_change(change_id):
    """
    Applies the pending change to the actual table and deletes the pending record.
    """
    change = get_pending_change_by_id(change_id)
    if not change:
        return False, "Change not found"

    table_name = change['table_name']
    action_type = change['action_type']
    data = json.loads(change['data_json']) if change['data_json'] else {}
    record_id = change['record_id']

    try:
        if action_type == 'INSERT':
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            values = list(data.values())
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            execute(query, tuple(values))

        elif action_type == 'UPDATE':
            # Prepare SET clause
            columns = list(data.keys())
            set_clause = ', '.join([f"{col}=%s" for col in columns])
            values = list(data.values())

            # Determine Primary Key
            pk_column = 'id'
            if table_name == 'Countries':
                pk_column = 'country_code'
            elif table_name == 'Indicators' or table_name == 'HealthIndicators' or table_name == 'EconomyIndicators' or table_name == 'EducationIndicators':
                pk_column = 'indicator_code'
            elif table_name == 'IndicatorCategories':
                pk_column = 'id'
            
            if table_name == 'IndicatorData':
                # Composite key: country_code|indicator_code|year
                keys = record_id.split('|')
                if len(keys) == 3:
                    query = f"UPDATE {table_name} SET {set_clause} WHERE country_code=%s AND indicator_code=%s AND year=%s"
                    values.extend(keys)
                    execute(query, tuple(values))
            else:
                # Standard single PK update
                query = f"UPDATE {table_name} SET {set_clause} WHERE {pk_column}=%s"
                values.append(record_id)
                execute(query, tuple(values))

        elif action_type == 'DELETE':
            pk_column = 'id'
            if table_name == 'Countries':
                pk_column = 'country_code'
            elif table_name == 'Indicators' or table_name == 'HealthIndicators' or table_name == 'EconomyIndicators' or table_name == 'EducationIndicators':
                pk_column = 'indicator_code'
            elif table_name == 'IndicatorData':
                # Composite key deletion
                keys = record_id.split('|')
                if len(keys) == 3:
                    query = f"DELETE FROM {table_name} WHERE country_code=%s AND indicator_code=%s AND year=%s"
                    execute(query, tuple(keys))
                reject_change(change_id)
                return True, "Approved successfully"
            
            query = f"DELETE FROM {table_name} WHERE {pk_column}=%s"
            execute(query, (record_id,))

        # If successful, delete from pending
        reject_change(change_id)
        return True, "Approved successfully"

    except Exception as e:
        return False, str(e)
