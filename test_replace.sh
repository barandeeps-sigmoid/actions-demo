file_name="V0__table_f.sql"
fn="fddsf.sql"
substitute_text=".$(date +%s%3)_" 

echo ${file_name/_/$substitute_text}
echo ${fn/_/$substitute_text}
