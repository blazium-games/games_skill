# Player MCP prompts

| Prompt | Arguments | Purpose |
|--------|-----------|---------|
| `setup_account` | none | Create an account, confirm the email code, and save the first key. A later connection calls `elevate_session`. Do not set Authorization |
| `sign_in` | none | Sign in with a typed password. The connection is logged in only after sign-in succeeds |
