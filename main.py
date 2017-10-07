# coding:utf-8
from wox import Wox
import subprocess
import os
import ConfigParser
import traceback

class Main(Wox):

	LOG_FILE = "./logs/error.txt"
	PAC_FILE = "\user-rule.txt"


	def query(self, query):

		results = []
		if query == "":
			with open(self.loads(), "r") as pacs:
				for pac in pacs:
					results.append({
						"Title": u"%s" % pac.strip().strip("||").strip("^"),
						"IcoPath": "Images/pic.png",
					})
			return list(reversed(results))

		if query in "set":
			return [{
				"Title": u"设置name, directory",
				"IcoPath": "Images/pic.png"
			}]

		if query in "delete":
			return self.deal_delete()
		
		words = query.split(" ")
		if len(words) > 1:
			return deal_set(words)


		site = self.get_main_site(query)
		results.append({
			"Title": u"存储 %s 到pac中" % site,
			"IcoPath": "Images/pic.png",
			"JsonRPCAction":{
				"method": "add",
				"parameters": [site,],
				"dontHideAfterAction": False,
			}
		})
		return results

	def add(self, site):
		try:
			site = "||%s^" % site
			with open(self.loads(), "a") as pac:
				pac.write(site + "\n")
			self.restart()
		except:
			self.log_error("add")



	def delete(self, pd):
		try:
			pacs = []
			with open(self.loads(), "r") as pacls:
				for pac in pacls:
					pacs.append(pac)
			with open(self.loads(), "w") as pacls:
				for pac in pacs:
					if pac == pd:
						continue
					pacls.write(pac + "\n")
			self.restart()
		except:
			self.log_error("delete")

	def deal_delete(self):
		with open(self.loads(), "r") as pacs:
			for pac in pacs:
				results.append({
					"Title": u"删除 %s" % pac.strip().strip("||").strip("^"),
					"IcoPath": "Images/pic.png",
					"JsonRPCAction": {
						"method": "delete",
						"parameters": [pac],
						"dontHideAfterAction": False,
					}
				})
		return list(reversed(results))


	def deal_set(self,words):
		if words[0] == "set":
			self.loads()
			if words[1] == "name":
				return [{
					"Title": u"设置name属性为%s" % words[2],
					"SubTitle": u"此时name的属性为%s" % self.ss_name,
					"IcoPath": "Images/pic.png",
					"JsonRPCAction": {
						"method": "set_conf",
						"parameters": ["name", words[2]],
						"dontHideAfterAction": False,
					}
				}]
			elif words[1] == "directory":
				return [{
					"Title": u"设置directory属性为 %s" % words[2],
					"SubTitle": u"此时name的属性为 %s" % self.ss_directory,
					"IcoPath": "Images/pic.png",
					"JsonRPCAction": {
						"method": "set_conf",
						"parameters": ["directory", words[2]],
						"dontHideAfterAction": False,
					}
				}]
			else:
				return [{
					"Title": u"设置name, directory属性",
					"IcoPath": "Images/pic.png",
				}]

	def get_main_site(self, site):
		if site.startswith("https"):
			site = site[8:]
		elif site.startswith("http"):
			site = site[7:]
		site = site.split("/")[0]
		return site


	def restart(self):
		try:
			self.loads()
			c = 'taskkill /F /IM %s' % self.ss_name
			s = self.ss_directory + "\\" + self.ss_name
			os.system(c)
			subprocess.Popen(s)
		except:
			self.log_error("restart")

	def set_conf(self, key, value):
		cf = ConfigParser.ConfigParser()
		cf.read("config.conf")
		if key == "name":
			cf.set("ss_info", "ss_name", value)
		elif key == "directory":
			cf.set("ss_info", "ss_directory", value)
		cf.write(open("config.conf", 'w'))

	def loads(self):
		cf = ConfigParser.ConfigParser()
		cf.read("config.conf")
		self.ss_name = cf.get("ss_info", "ss_name")
		self.ss_directory = cf.get("ss_info", "ss_directory")
		self.user_pac = self.ss_directory + self.PAC_FILE
		return self.user_pac

	def log_error(self, fun_str):
		with open(self.LOG_FILE, "a") as f:
			f.write("%s: \n%s" % (fun_str, traceback.format_exc()))


if __name__ == "__main__":
	Main()
