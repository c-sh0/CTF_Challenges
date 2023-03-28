# Input Validation
## 50pts: [SQL Login]
Figure out the password to login. Get the password for user: admin

1. This is a classic SQL injection challenge.
2. Enter a single quote `'` and note the error.
3. Classic SQLi payload: `' or '1'='1`

## 75pts: [Cross Site Scripting]
We've implemented a special anti-XSS technology - can you hack it? What is value of 'admin_sess_id' cookie?

1. You are presented with a simple form.
2. Enter an invalid `Image URL`
3. Right click and `Inspect` the `<img>` tag.
4. This is a classic XSS challenge where quotes are not properly escaped/encoded.
5. Payload: `x" onerror="alert(document.cookie)`
6. Right click and `Inspect` the `<img>` tag.

## 100pts: [SQL Credit Cards]
Find the credit card number. Get the credit card number for user: `UserNameHere`

1. This is a classic SQL injection challenge.
2. Enter a single quote `'` and note the error. (`COLLATE NOCASE` an indication this is a Sqlite3 database)
3. The hint provides a clue to the possible table name. `credit_cards`?
4. Injecting a `UNION SELECT` and `-- ` to ignore the rest of the statement, should return the correct record?
5. Payload: `UserNameHere' UNION SELECT card FROM credit_cards where username='UserNameHere' --`
