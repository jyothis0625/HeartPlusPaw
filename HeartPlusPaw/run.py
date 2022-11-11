import json
from pathlib import Path
import re as re
import time
from datetime import date, datetime
import jsbeautifier
import pandas as pd
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


with open("Config.yml", "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

def sensor():
    t = datetime.today()
    url=(cfg['caps']['URL'])
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(2)
    select=driver.find_element('xpath',"//select[@class='countDropdown'][1]").send_keys('50')
    time.sleep(2)
    product=driver.find_elements('xpath',"//div[@class='jobInfo JobListing']")
    
    links = []
    for pp in product:
     pp1=pp.find_elements(By.TAG_NAME,"('div')[-1]")
     pp2=pp.find_element(By.TAG_NAME,"a")
     link = pp2.get_attribute('href')
     links.append(link)
     
    from tqdm import tqdm
    alldetails=[]

    for i in tqdm(links):
        

        driver.get(i)
        
        try:
          Job_Level=driver.find_element('xpath','//span[@aria-label="Level"]').text 
        except:
          Job_Level="None"
            
        try:
          Job_Location=driver.find_element('xpath','//*[@id="Job Location-row"]/div/div/span').text  
        except:
          Job_Location="None"
            
        try:
          Position_Type=driver.find_element('xpath','//*[@id="Position Type-row"]/div/div/span').text
        except:
          Position_Type='None'
            
        try:
          Education_Level=driver.find_element('xpath','//*[@id="Education Level-row"]/div/div/span').text
        except:
          Education_Level='None'
            
        try:
          Travel_Percentage=driver.find_element('xpath','//*[@id="Travel Percentage-row"]/div/div/span').text
        except:
          Travel_Percentage='None'
            
        try:
          Job_Shift=driver.find_element('xpath','//*[@id="Job Shift-row"]/div/div/span').text
        except:
          Job_Shift='None'
            
        try:
          Job_Category=driver.find_element('xpath','//*[@id="Job Category-row"]/div/div/span').text
        except:
          Job_Category='None'
                
        try:
          Job_Title=driver.find_element('xpath','//*[@id="jobTitle-row"]/div/span').text
        except:
          Job_Title='None'
            
        try:
          Job_description=driver.find_element('xpath','//*[@id="jobDesc-row"]/div/span').text
        except:
          Job_description='None'
        
        

        tempJ={'Job_Level':Job_Level,
                'Job_position':Position_Type,
                'Education_Level':Education_Level,
                'Travel_Percentage':Travel_Percentage,
                'Job_Shift':Job_Shift,
                'Job_Category':Job_Category,
                'Job_Title':Job_Title,
                'Job_description':Job_description,
                'linkofproduct':i}

        alldetails.append(tempJ)
    
    data=pd.DataFrame(alldetails)
    # print(data)
    
    def find_number(text):
        num = re.findall(r'\$.+',text) 
        return " ".join(num)
    data['Bonus']=data['Job_description'].apply(lambda x: find_number(x))
    # print(data)
    
    list_of_jsons = data.to_json(orient='index')
    
    driver.close()
    
    jb=jsbeautifier.beautify(list_of_jsons)

    basedir = (cfg['caps']['Basedirectory'])

    path=Path(f'{basedir}/{"HeartPlusPaw"}/{t.year}/{t.strftime("%b")}/{t.day:02d}')
    path.mkdir(parents=True, exist_ok=True)
    File=path / (t.strftime("%H")+"-"+t.strftime("%M") +".json")
    with open(File,'w') as f:
        d=f.write(jb)
      
    return str(jb)
    
sensor()




    
    
    
    
    