#! /bin/bash

# This script helps you to import these static (manual generated) lists to your pihole
# Download this script to your pihole and place it into a cronjob with enough time after the gravity update cronjob
# see: /etc/cron.d/pihole for details

# Some variables you want to change
#URL_DOMAIN="yourdomain.com"  # Domain where to find the static lists (you could define it globally too): #  export URL_DOMAIN="pilists.example.com" && pihole-update-static-lists.sh
COMMENT_ID="___AUTOUPDATE___" # Comment which identifies the URLs in the gravity domain to be updated (removed before the new list will be imported)

# Download URLs for the static list which used to update/import
URL_LIST_REGEX_BLACKLIST="https://${URL_DOMAIN}/dist/_regex-blacklist.txt"
URL_LIST_REGEX_WHITELIST="https://${URL_DOMAIN}/dist/_regex-whitelist.txt"
URL_LIST_WHITELIST="https://${URL_DOMAIN}/dist/_whitelist.txt"

# On which type could each domain item be identified
DB_TYPE_WHITELIST=0
DB_TYPE_WHITELIST_REGEX=2
DB_TYPE_BLACKLIST_REGEX=3

# DB Path
DB_GRAVITY="/etc/pihole/gravity.db"

# SQLITE 3 Binary
SQLBIN="/usr/bin/sqlite3"

# Inser patterns
INSERT_PATTERN="INSERT INTO domainlist (domain, type, date_added, date_modified, enabled, comment) VALUES ('%s', %s, date('now'), date('now'), 1, '${COMMENT_ID}');"
CLEAR_PATTERN="DELETE FROM domainlist WHERE type = '%s' AND comment = '${COMMENT_ID}';"

# Define a generic import function
import_domains() {
  URL=$1
  TYPE=$2

  for DOMAIN in `curl -sSL --fail ${URL}`; do
    DOMAIN=`echo ${DOMAIN} | xargs` # Trim string

    if [[ $DOMAIN =~ ^[^\#].*$ ]]; then # ignore comments and empty
      if [ $DOMAIN != "" ]; then
        QUERY=`printf "${INSERT_PATTERN}" "${DOMAIN}" "${TYPE}"`

        # Run query
        echo "IMPORTING: $TYPE -> $DOMAIN"
        $SQLBIN $DB_GRAVITY "${QUERY}" ".exit"
      fi
    fi
  done
}

# Define a generic clear function
clear_domains() {
  TYPE=$1
  QUERY=`printf "${CLEAR_PATTERN}" "${TYPE}"`

  # Run query
  echo "CLEARING: $TYPE"
  $SQLBIN $DB_GRAVITY "${QUERY}" ".exit"
}

# Clear lists
clear_domains $DB_TYPE_BLACKLIST_REGEX
clear_domains $DB_TYPE_WHITELIST_REGEX
clear_domains $DB_TYPE_WHITELIST

# Import new lists
import_domains $URL_LIST_REGEX_BLACKLIST $DB_TYPE_BLACKLIST_REGEX
import_domains $URL_LIST_REGEX_WHITELIST $DB_TYPE_WHITELIST_REGEX
import_domains $URL_LIST_WHITELIST $DB_TYPE_WHITELIST

# Restart FTL
pihole restartdns reload-lists
