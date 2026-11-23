# Inactivity sign-out and SSO

No tool changes these settings: explain them and give the user the steps in the app.

## Sign out after inactivity

Settings → Security → **Sign out after inactivity** applies to everyone in the account, including the owner.
It offers Never, 5/10/15/30 minutes, and 1/2/4 hours; Never is the default. Only the owner can change it, because
the change signs every member out; anyone else sees "Only owner can change the inactivity sign out time". The
current value is readable as `inactivity_timeout` from `docsumo_get_account_config`. After a change, reload the page
and check the saved value.

Docsumo warns one minute before signing out. Clicking, typing and scrolling count as activity, and activity in another
tab of the same account keeps the session alive. **Stay signed in** on the warning renews the session. A device that
slept past the deadline signs out when it wakes.

For an unexpected sign-out, establish the configured duration, the message shown at login, recent activity, other
open tabs and whether the device slept. Not every sign-out or 401 error comes from this setting.

## SSO

Settings → Security separates testing and enabling the SAML connection from its scope (all users, domain
exemptions) and per-user exemptions. The scope controls unlock only after a successful connection test, and only
users allowed to configure SSO see them. If a scope change seems to revert, reload, check the saved scope and the
connection test state, then try again. Never collect SAML secrets or tokens in chat. Questions about how SSO is
enforced go to Docsumo support.
