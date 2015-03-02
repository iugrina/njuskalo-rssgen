# RSS generator for www.njuskalo.hr web page

[Njuškalo](www.njuskalo.hr) is the largest and most popular online
classifieds in Croatia that daily connects hundreds of thousands of buyers and sellers
(at least they say so :D).

Unfortunately, it doesn't support RSS/Atom feeds.

This application corrects that flaw! It is a simple Python program
for generating RSS feeds for Njuškalo pages. For example,
if you're following 
[Playstation3](http://www.njuskalo.hr/ps3-igre) games market
 on Njuškalo you can easily adjust `njuskalo-rssgen` to
generate RSS feeds for that page. 

All that is needed is to edit `vars.ini`, adjust variables and
start `njuskalo-ps3.py`. To avoid starting the app by hand
you can run it through cron.
