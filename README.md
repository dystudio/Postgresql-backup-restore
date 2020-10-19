# Postgresql-backup-restore

## The core idea is to use Python to parse the JSON file containing the database information, and then dynamically generate Windows and Linux script files that back up the database

### backup

1. Write the data information to backup-*.json file

2. Execute Python backup-*.py dev_all dev_masterdata

3. Generate backup .bat or .sh script



### restore

1. Write the data information to the restore-*.json file

2. Run Python restore-*.py dev_all dev_masterdata

3. Generate restore .bat or .sh script

