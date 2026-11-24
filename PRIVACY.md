# Privacy policy

L3R MCP server (https://mcp.l3r.io/mcp). Effective 8 November 2026.

## What we collect

The service has no accounts and asks for no personal information. It never asks for your location. Each call
receives the address or identifier that you or your assistant typed, and your network address.

## What we keep

For each call we keep a log line with:

- the tool;
- the result's status and kind;
- the county;
- counts and the time taken;
- a keyed hash of the query;
- a keyed hash of your network block (the /24 for IPv4, the /64 for IPv6), or the name of the AI platform the call
came through.

The service's own log does not record the address or identifier you typed, or your full network address, and
the server writes no per-request access log. Rate-limit counters are held in memory and cleared each day.

Two providers that carry the traffic keep their own logs under their own policies. Cloudflare, which sits in front
of the service, sees each request, including your network address. Railway, which hosts it, keeps the service's log
lines described above. We ask that log lines be kept no longer than 90 days; how long each provider retains its own
request logs is set by that provider's plan.

## Who we share with

When L3R's own address index does not hold a typed address, the service sends that address to the U.S. Census
Bureau's public geocoder (geocoding.geo.census.gov) to find its Census tract and location. It also does this for
some San Francisco and New York City addresses. Nothing else is sent to anyone. We do not sell data, and the service
shows no advertising.

Your AI platform (for example Anthropic or OpenAI) sees your conversation, including what it sends to this service
and what it gets back, under its own privacy policy.

## Security

The service runs as its own application, apart from the rest of L3R's systems. It holds no keys to any of
them. It uses a read-only database account and a storage key limited to the files it serves.

## Contact

Questions or requests: [mcp@l3r.io](mailto:mcp@l3r.io).
