# Client-side Protections
## 10pts: [Super Admin]
You must be an admin to proceed. (Javascript Parameter Tampering)

1. Click Submit
2. A hint to the solution is in the error message: <br>
`Javascript validation failed. You are not super admin. is_super_admin = false`
3. Open DevTools console and change the `is_super_admin` variable to `true`
4. Click Submit

## 50pts: [Timer]
Wait until the timer completes to press the submit button. (Tampering with Local Storage)

1. Disable Javascript in your browser
2. Open DevTools and navigate to `Application -> Local Storage`
3. Edit the value of `hackerchallenge.timer` to something small (in seconds)
4. Re-Enable Javascript
5. Wait until the timer reaches zero and click Submit

## 100pts: [Paid Content]
You must be a paid user to proceed. (Web Parameter/Payload Tampering)

1. Open DevTools and click Submit (Alternatively, Burpsuite or OWASP Zap could be used but, I just used DevTools)
2. In the Network tab, locate the POST request made to `challenge/submit-answer/`
3. Using the command line to resubmit the request: `Right-Click -> Copy -> Copy as cURL`
4. Use an editor, change the payload to: `"PaidContent","paid":true`
5. Resubmit the request via the command line (curl in this case), be sure to include the CSRF token and any other necessary headers
