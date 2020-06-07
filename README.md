# test_social_net
Simple API and Bot for interaction automation.

## API
Endpoints:
- [x] User: Sign Up
- [x] User: Self information -> show when user was login last time and when he mades a last
request to the service
- [x] User: Login
- [x] User: Logout
- [x] Token: Refresh
- [x] Token: Revoke access
- [x] Token: Revoke refresh
- [x] Post: Create
- [x] Post: Like
- [x] Post: Unlike
- [x] Analytics -> how many likes was made aggregated by day.

## Bot
Object of this bot demonstrate functionalities of the system according to defined rules.

Use existing params or create new in config file:
- default
- post_only_min
- post_only_max
- like_only_min
- like_only_max

It works with ArgumentParser that allow to use -c --conf command to define configuration section.