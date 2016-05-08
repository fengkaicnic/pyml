import utils
import traceback

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    
        
    
except:
    traceback.print_exc()
    