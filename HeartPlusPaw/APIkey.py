# @app.route('/')
# def index(): 
#     logging.basicConfig(filename="D://Logs//test.log",
#                         format="%(asctime)s: %(levelname)s: %(message)s")
    
#     logger=logging.getLogger()
#     logger.setLevel(logging.DEBUG)
    
#     logger.debug("Logging test...")
#     logger.info("The program is working as expected")
#     logger.warning("The program may not function properly")
#     logger.error("The program encountered an error")
#     logger.critical("The program crashed")
    
#     url='https://www.paycomonline.net/v4/ats/web.php/jobs?clientkey=FC9962A89833ED19DB7F75E9F964ACB9'
#     driver = webdriver.Chrome(ChromeDriverManager().install())
#     driver.get(url)
#     time.sleep(2)
#     select=driver.find_element('xpath',"//select[@class='countDropdown'][1]").send_keys('50')
#     time.sleep(2)
#     product=driver.find_elements('xpath',"//div[@class='jobInfo JobListing']")
    
#     links = []
#     for pp in product:
#      pp1=pp.find_elements(By.TAG_NAME,"('div')[-1]")
#      pp2=pp.find_element(By.TAG_NAME,"a")
#      link = pp2.get_attribute('href')
#      links.append(link)
    
    
#     from tqdm import tqdm
#     alldetails=[]


#     for i in tqdm(links):
#        try:
#         driver.get(i)
    
#         job_title=driver.find_element('xpath','//*[@id="jobTitle-row"]/div/span').text
#         job_details_lefttable=driver.find_element('xpath',"//div[@class=' col-md-6 local-tax-col local-ee']").text
#         job_details_righttable=driver.find_element('xpath',"//div[@class=' col-md-6 local-tax-col local-client']").text
#         job_description=driver.find_element('xpath','//*[@id="jobDesc-row"]/div/span').text
#         tempJ={'job_title':job_title,
#                'job_details_lefttable':job_details_lefttable,
#                'job_details_righttable':job_details_righttable,
#                'job_description':job_description,
#                'linkofproduct':i}
#         alldetails.append(tempJ)
#        except:
#          print("e")
         
#     data=pd.DataFrame(alldetails)
    
#     def find_number(text):
#        num = re.findall(r'\$.+',text) 
#        return " ".join(num)
#     data['Bonus']=data['job_description'].apply(lambda x: find_number(x))
    
#     df=data['job_details_lefttable'].str.split('\n',expand=True) 
#     df.columns=['Level','Level1','Job_location','Job_location1','Position','Position1','education','education1']
#     left_level=df[(df.Level=='Level') ]
#     df1 =left_level.rename(columns={'education': 'Education', 'education1': 'Education1'})
    
#     left_loc=df[(df.Level=='Job Location')]
#     df2 =left_loc.rename(columns={'Level': 'Job_location', 'Level1': 'Job_location1','Job_location':'Position','Job_location1':'Position1','Position':'Education','Position1':'Education1'})
#     Left_table=df1.append(df2)
 
    
#     df3=data['job_details_righttable'].str.split('\n',expand=True)
#     df3.columns=['Travel_Percentage','Travel_Percentage1','Job Shift','Job Shift1','job Category','job Category1']
#     right_travel=df3[(df3.Travel_Percentage=='Travel Percentage')]
#     df4 =right_travel.rename(columns={'job Category': 'Job Category', 'job Category1': 'Job Category1'})
    
#     right_shift=df3[(df3.Travel_Percentage=='Job Shift')]
#     df5 =right_shift.rename(columns={'Travel_Percentage':'Job Shift', 'Travel_Percentage1':'Job Shift1','Job Shift':'Job Category','Job Shift1':'Job Category1'})
#     Right_table=df4.append(df5)
    
#     df6=data.drop(['job_details_lefttable', 'job_details_righttable','linkofproduct'], axis=1)
    
#     df7=pd.concat([Left_table,Right_table,df6],axis=1)
    
#     df8=df7.drop(['Level', 'Job_location','Position','Education','Travel_Percentage','Job Shift','Job Category','education','education1','job Category','job Category1'], axis=1)
    
#     list_of_jsons = df8.to_json(orient='index')
#     driver.close()
    

#     jb=jsbeautifier.beautify(list_of_jsons)
    
    
#     t = datetime.today()
#     basedir = 'D://Scraping'

#     path=Path(f'{basedir}/{"HeartPlusPaw"}/{t.year}/{t.strftime("%b")}/{t.day:02d}')
#     path.mkdir(parents=True, exist_ok=True)
#     File=path / (t.strftime("%H")+"-"+t.strftime("%M") +".json")
#     with open(File,'w') as f:
#         d=f.write(jb)
      
#     return str(jb)
# index()
    
   
  
# if __name__ == "__main__":
#     # schedule.every(5).minutes.do(app)
#     # scheduler.add_job(id = 'Scheduled Task', func=scheduleTask, trigger="interval", seconds=3)
#     # scheduler.start()
#     app.run(debug=True,host="127.0.0.1",port=5000)
    
    
    
#     schedule.every(5).minutes.do(app)