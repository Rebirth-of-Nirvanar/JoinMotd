# -*- coding: UTF-8 -*-
import datetime
import json
import urllib.request

settingsAppsecret = "" # https://www.tianqiapi.com/index/doc?version=v6
settingsCurrentServer = "survival"
settingsFirstSetupday = datetime.datetime.strptime('2020-11-23', '%Y-%m-%d') #2020-11-23 21:51:53
settingsMainServer = "§6服务器名称"
settingsMutiServer = True
settingsWeather = True
playerIPs = {}

servers = {
    "creative": 
    {
        "displayName": "§b创造",
        "name": "creative",
        "title": "-----===== 欢迎来到{0}§f({1}§f) =====-----",
        "tip": "§e小提示: /op 你的ID 来获取 op"
    },
    "mirror": 
    {
        "displayName": "§e镜像",
        "name": "mirror",
        "title": "-----===== 欢迎来到{0}§f({1}§f) =====-----",
        "tip": "§e小提示: /op 你的ID 来获取 op"
    },
    "survival": 
    {
        "displayName": "§a生存",
        "name": "survival",
        "title": "-----===== 欢迎来到{0}§f({1}§f) =====-----",
        "tip": ""
    }
   
}

def on_player_joined(server, player, info):
    playerIP = getPlayerIP(player, info)
    playerIPs[player] = playerIP
    showMotd(server, player)
def on_user_info(server, info):
    if info.content.startswith("!!joinMotd"):
        showMotd(server, info.player)
    if info.content.startswith("!!day"):
        server.tell(info.player, "今天是 {} §f开服的第 §e{} §f天".format(settingsMainServer, getDaySub(settingsFirstSetupday, datetime.datetime.now())))


def showMotd(server, player):
    server.tell(player, servers[settingsCurrentServer]["title"].format(settingsMainServer, servers[settingsCurrentServer]["displayName"]))
    server.tell(player, "今天是 {} §f开服的第 §e{} §f天".format(settingsMainServer, getDaySub(settingsFirstSetupday, datetime.datetime.now())))
    server.tell(player, servers[settingsCurrentServer]["tip"])
    if settingsMutiServer:
        server.tell(player, "-----===== 服务器列表 =====-----")
        serverList = []
        for k, v in servers.items():
            if k != settingsCurrentServer:
                serverList.append({
                    "text": "[{}§f]".format(v["displayName"]),
                    "clickEvent": {
                        "action": "run_command",
                        "value": "/server {}".format(v["name"])
                    },
                    "hoverEvent": {
                        "action": "show_text",
                        "contents": {
                            "text": "§6点击传送至 {} §6子服".format(v["displayName"])
                        }
                    }
                })
                serverList.append({"text": " "})
            
        server.tell(player, serverList)
    if settingsWeather:
        try:
            playerWeatherInfo = getPlayerWeather(playerIPs[player])
            server.tell(player, "-----===== 天气信息 =====-----")
            server.tell(player, "§6城市: §e{} §6天气: §e{} §6空气质量: §e{}§6(§e{}§6)".format(playerWeatherInfo["city"], playerWeatherInfo["wea"], playerWeatherInfo["air_level"], playerWeatherInfo["air"]))
            server.tell(player, "§6温馨提示: §e".format(playerWeatherInfo["air_tips"]))
            server.tell(player, "§6气温: §e{}§6(§e{}§6/§e{}§6) §6湿度: §e{} §6能见度: §e{}".format(playerWeatherInfo["tem"], playerWeatherInfo["tem2"], playerWeatherInfo["tem1"], playerWeatherInfo["humidity"], playerWeatherInfo["visibility"]))
            server.tell(player, "§6气压: §e{} §6风速: §e{} §6风力等级: §e{} §6风向: §e{}".format(playerWeatherInfo["pressure"], playerWeatherInfo["win_meter"], playerWeatherInfo["win_speed"],playerWeatherInfo["win"]))
        except:
            pass

def getDaySub(startTime, stopTime):
    return str((stopTime - startTime).days)
  
def getPlayerIP(player, info):
    return info.content.split(" ")[0].split(":")[0].split("/")[1]
    

def getPlayerWeather(playerIP):
    response = urllib.request.urlopen("https://www.tianqiapi.com/api?version=v6&appid=53566646&appsecret={}&ip={}".format(settingsAppsecret, playerIP))
    return json.loads(response.read())
    