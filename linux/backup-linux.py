import json
import os
import sys
import time

if len(sys.argv) < 2:
    print('Usage:\n', sys.argv[0],
          '\ndev_all\n'
          + 'dev_keycloak\n'
          + 'dev_masterdata\n'
          )
    exit()
dbparam = sys.argv[1]

print('------------>' + dbparam)

with open(os.getcwd() + os.sep + 'backup-linux.json') as conf_file:
    # with open(os.path.dirname(__file__) + os.sep + 'env-conf.json') as conf_file:
    backup_conf = json.load(conf_file)


def set_env_param(dbparam):
    dbhost = backup_conf[dbparam]['host']
    dbport = backup_conf[dbparam]['port']
    dbname = backup_conf[dbparam]['database']
    dbuser = backup_conf[dbparam]['username']
    dbpassword = backup_conf[dbparam]['password']
    return GenBat(dbhost, dbport, dbname, dbuser, dbpassword)


def GenBat(dbhost, dbport, dbname, dbuser, dbpassword):
    curdate = time.strftime("%Y%m%d", time.localtime())
    strbuf = ('#/bin/bash' + '\n'
              + '' + '\n'
              + 'echo ">>>>>>host[' + dbhost + '],port[' + dbport + '],dbname[' + dbname + '] dump begin' + '<<<<<<"' + '\n'
              + '' + '\n'
              + 'export PGPASSWORD="' + dbpassword + '"\n'
              + 'export db_name="' + dbname + '"\n'
              + 'export encoding="UTF-8' + '"\n'
              + 'export host="' + dbhost + '"\n'
              + 'export port="' + dbport + '"\n'
              + 'export username="' + dbuser + '"\n'
              + 'export bak_path="/home/appuser/devhost/' + curdate + '/' + '"\n'
              + 'export other_flags="--verbose  --no-privileges"' + '\n'
              + 'export bak_file="' + dbname + '_' + curdate + '"\n'
              + 'if [ ! -d $bak_path ]; then' + '\n'
              + '  mkdir -p $bak_path ' + '\n'
              + 'else' + '\n'
              + ' echo "Not need to create directory "' + '\n'
              + 'fi' + '\n'
              + 'pg_dump  --host=$host  --port=$port --username=$username --format=c --encoding=$encoding $other_flags   -n "public" $db_name > $bak_path/$bak_file.backup' + '\n'
              + 'echo ">>>>>>host[' + dbhost + '],port[' + dbport + '],dbname[' + dbname + '] dump end' + '<<<<<<"' + '\n'
              + '' + '\n'
              )
    return strbuf


if dbparam == 'dev_all':
    dbparamall = ['dev_keycloak',
                  'dev_masterdata',
                 ]
    for db_param_single in dbparamall:
        backup_script_path = db_param_single + '_backup.sh'
        with open(backup_script_path, 'w') as f:
            content = set_env_param(db_param_single)
            f.write(content)
    with open('dev_all_backup.sh', 'w') as f:
        content_all = ('#/bin/bash' + '\n'
                       + 'for i in  `ls dev* | grep -v dev_all`;' + '\n'
                       + 'do' + '\n'
                       + ' source ./$i' + '\n'
                       + 'done' + '\n'
                       + '' + '\n')
        f.write(content_all)
else:
    backup_script_path = dbparam + '.sh'
    with open(backup_script_path, 'w') as f:
        content = set_env_param(dbparam)
        f.write(content)
