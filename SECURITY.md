# Security

Report a vulnerability in the L3R MCP server (https://mcp.l3r.io/mcp) or in this repository by email to
[security@l3r.io](mailto:security@l3r.io). Please do not open a public issue.

Include what you found, how to reproduce it, and what it could expose. We will acknowledge your report and keep you
informed while we fix it.

Of particular interest:

- an answer that carries a field outside the documented response (for example an owner, contact or value);
- a way past the rate limits or the one-input-per-call rule;
- a way to reach data or systems other than the server's published tools.

Please test only against your own calls, keep within the published limits (60 calls an hour per IP address), and do not attempt to
access other people's data or degrade the service.
