# Common password blocklist

`100k-most-used-passwords-NCSC.txt` is sourced from the
[SecLists Common Credentials collection](https://github.com/danielmiessler/SecLists/tree/master/Passwords/Common-Credentials).

The application imports every non-empty entry into PostgreSQL on first start
and uses the table only to reject commonly compromised passwords.
