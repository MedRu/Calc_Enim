import time,os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class Inputs:
    def get(self):

        self.username = str(input("Insert Username : "))
        self.password = str(input("Insert Password : "))
        return self

class Driver:
    def __init__(self):
        opt = Options()
        opt.add_argument("--headless")
        opt.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=opt,service_log_path=os.devnull)

class Logger_Manager:
    def __init__(self,username,password,driver):
        self.url = "https://edu.mines-rabat.ma/"
        self.driver = driver
        self.username = username
        self.password = password

    def logger(self):
        c__ = 0 
        while c__< 25:
            try :
                self.driver.get(self.url)
                time.sleep(2)
                self.driver.find_element_by_id('user_username').send_keys(self.username)
                self.driver.find_element_by_id('user_password').send_keys(self.password)
                self.driver.find_element_by_class_name('submit').click()
                break 
            except Exception:
                c__ += 1
            if c__ == 25 :
                raise Exception("Timeout issues !")
        c__ = 0
        while c__< 25:
            try :
                time.sleep(2)
                self.driver.find_element_by_id('academic_button').click()
                break 
            except Exception:
                c__ += 1
            if c__ == 25 :
                raise Exception("Timeout issues !")
        return self

    def scraper(self):
        ELM,COFF = [i.text for i in self.driver.find_elements_by_class_name('tr-odd')],[]
        dt = {}
        for i in ELM :
            if i[0] == "M":
                s = i[1:3]
            else :
                for k in range(1,len(i)):
                    if i[k] == ')':
                        try :
                            p = int(i[k-1])
                        except :
                            i = i[:k]+ '-' +i[k+1:]
                for k in range(len(i)-1):
                    if i[k] == '(':
                        try :
                            p = int(i[k+1])
                        except :
                            i = i[:k]+ '-' +i[k+1:]
                l_1= i.split('(')
                l_2=l_1[1].split(')')
                l_1[1] = l_2[0]
                l_1.append(l_2[1].replace('pas saisie',''))
                l_1[2] = l_1[2].split(" ")[3]
                try :
                    dt[s]+=[l_1]
                except :
                    dt[s] = [l_1]
        ELM = []
        for modele in dt :
            for elm in dt[modele] :
                if elm[2] != '':
                    ELM.append(float(elm[2]))
                    COFF.append(float(elm[1]))
        self.driver.close()
        return ELM,COFF

def p_scalaire(elm):
    s,c_s = 0,0
    for i in range(len(elm[0])):
        s += elm[0][i]*elm[1][i]
        c_s +=  elm[1][i]
    return s/c_s

if __name__ == '__main__':
    creds = Inputs().get()
    l = Logger_Manager(creds.username,creds.password,Driver().driver).logger()
    print("%.2f" % round(p_scalaire(l.scraper()), 2))




