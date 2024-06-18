DROP TRIGGER IF EXISTS Members_log on Members;
DROP TRIGGER IF EXISTS Employees_log on Employees;
DROP TRIGGER IF EXISTS Authors_log on Authors;
DROP TRIGGER IF EXISTS Books_log on Books;
DROP TRIGGER IF EXISTS Borrowed_Books_log on Borrowed_Books;
DROP FUNCTION IF EXISTS audit_trigger_function;



-- Function: audit_trigger_function
-- Purpose: To record changes made to any table into an audit_table.
-- Returns: A TRIGGER type which captures the table name, operation type, old and new data, user who made the change, and timestamp of the change.
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
  -- Insert audit information into audit_table whenever a change is made to a table.
  INSERT INTO audit_table (table_name, operation, old_data, new_data, changed_by, changed_at)
  VALUES (TG_TABLE_NAME, TG_OP, OLD, NEW, current_user, current_timestamp);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;



-- Trigger: Members_log
-- Purpose: To create an audit log for the Members table.
-- Timing: After any INSERT, UPDATE or DELETE operation on Members table.
CREATE TRIGGER Members_log
AFTER INSERT OR UPDATE OR DELETE ON Members
FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Trigger: Employees_log
-- Purpose: To create an audit log for the Employees table.
-- Timing: After any INSERT, UPDATE or DELETE operation on Employees table.
CREATE TRIGGER Employees_log
AFTER INSERT OR UPDATE OR DELETE ON Employees
FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Trigger: Authors_log
-- Purpose: To create an audit log for the Authors table.
-- Timing: After any INSERT, UPDATE or DELETE operation on Authors table.
CREATE TRIGGER Authors_log
AFTER INSERT OR UPDATE OR DELETE ON Authors
FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Trigger: Books_log
-- Purpose: To create an audit log for the Books table.
-- Timing: After any INSERT, UPDATE or DELETE operation on Books table.
CREATE TRIGGER Books_log
AFTER INSERT OR UPDATE OR DELETE ON Books
FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Trigger: Borrowed_Books_log
-- Purpose: To create an audit log for the Borrowed_Books table.
-- Timing: After any INSERT, UPDATE or DELETE operation on Borrowed_Books table.
CREATE TRIGGER Borrowed_Books_log
AFTER INSERT OR UPDATE OR DELETE ON Borrowed_Books
FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();