from db import db_session
from schemas import DiabetesStats, StrokeStats, HeartDiseaseStats

# helper function for getting advice
def getInfo(d_table, stat_table, d_id):
    stuff = db_session.query(stat_table).filter_by(id=1).first()
    sources = db_session.query(stat_table).filter_by(id=2).first()
    info = db_session.query(stat_table).filter_by(id=3).first()
    user = db_session.query(d_table).filter_by(diagnostic_id=d_id).first()

    statsColNames = []
    userColNames = []

    for column in stat_table.__table__.columns:
        column_name = column.name
        if column_name == 'id' or column_name == 'updated_at':
            continue
        statsColNames.append(column_name)

    for column in d_table.__table__.columns:
        column_name = column.name
        if column_name == 'diagnostic_id':
            continue
        userColNames.append(column_name)

    advice = []
    cite = []

    for i in range(len(userColNames)):
        statValue = getattr(stuff, statsColNames[i])
        userValue = getattr(user, userColNames[i])

        if statValue != userValue:
            src = getattr(sources, statsColNames[i])
            if src != '':
                advice.append(getattr(info, statsColNames[i]))
                cite.append(src)
    
    return [advice, cite]

# helper function to insert metadata for advice
def insertStats():
    # insert averages for diabetes
    diabetes_stats = DiabetesStats(
        average_pregnancies='3',
        average_glucose='110',
        average_blood_pressure='68',
        average_skin_thickness='20',
        average_insulin='69',
        average_bmi='30',
        average_diabetes_pedigree_function='0.43',
        average_age='31'
    )
    db_session.add(diabetes_stats)

    # insert averages for stroke
    stroke_stats = StrokeStats(
        average_gender = 'Male',
        average_age='42',
        average_hypertension='0',
        average_heart_disease='0',
        average_ever_married='Yes',
        average_work_type='Private',
        average_residence_type='Urban',
        average_avg_glucose_level='105',
        average_bmi='28.8',
        average_smoking_status='never smoked'
    )
    db_session.add(stroke_stats)

    # insert averages for heart disease
    heart_stats = HeartDiseaseStats(
        average_age='50',
        average_sex='F',
        average_chest_pain_type='ATA',
        average_resting_bp='130',   
        average_cholesterol='227',
        average_fasting_bs='0',
        average_ecg='Normal',
        average_max_hr='148',
        average_exercise_angina='N',
        average_oldpeak='0.41',
        average_st_slope='Up'
    )
    db_session.add(heart_stats)

    # commit all and close session
    db_session.commit()
    db_session.close()

    # insert sources for diabetes advice
    diabetes_stats = DiabetesStats(
        average_pregnancies='https://www.niddk.nih.gov/health-information/diabetes/diabetes-pregnancy',
        average_glucose='https://www.northeastmedicalgroup.org/articles/what-is-healthy-blood-sugar',
        average_blood_pressure='https://www.hopkinsmedicine.org/health/conditions-and-diseases/diabetes/diabetes-and-high-blood-pressure',
        average_skin_thickness='https://www.ncbi.nlm.nih.gov/books/NBK481900/',
        average_insulin='https://www.veri.co/learn/optimal-fasting-insulin-level?srsltid=AfmBOoo_40qWIVtWcVOTucNXnz3hbKN3vDplcTL060pGT4Mv-XuwAv2k',
        average_bmi='https://www.heart.org/en/healthy-living/healthy-eating/losing-weight/bmi-in-adults#:~:text=A%20BMI%20between%2018.5%20and,or%20higher%20is%20considered%20obese.',
        average_diabetes_pedigree_function='',
        average_age='https://www.medicalnewstoday.com/articles/317375#:~:text=The%20average%20age%20of%20onset%20for%20type%202%20diabetes&text=The%20onset%20of%20diabetes%20is,can%20occur%20at%20any%20age.'
    )
    db_session.add(diabetes_stats)

    # insert sources for stroke advice
    stroke_stats = StrokeStats(
        average_gender = 'https://www.ahajournals.org/doi/10.1161/CIRCRESAHA.121.319915',
        average_age='https://pmc.ncbi.nlm.nih.gov/articles/PMC6535078/#:~:text=Aging%20is%20the%20most%20robust,persons%20aged%20%E2%89%A565%20years.',
        average_hypertension='https://www.heart.org/en/health-topics/high-blood-pressure/health-threats-from-high-blood-pressure/how-high-blood-pressure-can-lead-to-stroke',
        average_heart_disease='https://pmc.ncbi.nlm.nih.gov/articles/PMC9945299/',
        average_ever_married='https://www.mountsinai.org/files/MSHealth/Assets/HS/Locations/Precision-Recovery/BLOG%2011.pdf#:~:text=A%20recent%20study%20showed%20that%20the%20risk,stroke%20more%20than%20simply%20being%20married%20(2).',
        average_work_type='https://pmc.ncbi.nlm.nih.gov/articles/PMC10574301/',
        average_residence_type='https://pubmed.ncbi.nlm.nih.gov/34087323/',
        average_avg_glucose_level='https://www.ahajournals.org/doi/10.1161/01.str.0000115297.92132.84',
        average_bmi='https://pubmed.ncbi.nlm.nih.gov/35971008/#:~:text=Higher%20BMI%20(overweight%20or%20obese,reduce%20the%20risk%20of%20stroke.',
        average_smoking_status='https://www.world-stroke.org/assets/downloads/STROKE_RISK_AND_PREVENTION_LEAFLET_SMOKING-EN.pdf'
    )
    db_session.add(stroke_stats)

    # insert sources for heart disease advice
    heart_stats = HeartDiseaseStats(
        average_age='https://pmc.ncbi.nlm.nih.gov/articles/PMC6616540/',
        average_sex='https://pmc.ncbi.nlm.nih.gov/articles/PMC6616540/',
        average_chest_pain_type='https://www.mayoclinic.org/diseases-conditions/chest-pain/symptoms-causes/syc-20370838',
        average_resting_bp='https://utswmed.org/medblog/high-blood-pressure-heart-disease/#:~:text=For%20the%20average%20person%20who,at%20risk%20for%20heart%20disease.',   
        average_cholesterol='https://www.mayoclinic.org/diseases-conditions/high-blood-cholesterol/symptoms-causes/syc-20350800#:~:text=Prevention,drinks%20a%20day%20for%20men.',
        average_fasting_bs='https://www.cdc.gov/diabetes/diabetes-complications/diabetes-and-your-heart.html',
        average_ecg='https://www.mayoclinic.org/tests-procedures/ekg/about/pac-20384983',
        average_max_hr='https://www.health.harvard.edu/heart-health/what-your-heart-rate-is-telling-you',
        average_exercise_angina='https://www.health.harvard.edu/heart-health/angina-symptoms-diagnosis-and-treatments#:~:text=Angina%20(pronounced%20ANN%2Djuh%2Dnuh%20or%20ann%2DJIE%2Dnuh)%20is%20pain,which%20is%20caused%20by%20cholesterol%2Dclogged%20coronary%20arteries.',
        average_oldpeak='',
        average_st_slope='https://www.sciencedirect.com/science/article/abs/pii/0002870386902656#:~:text=Abstract,compared%20favorably%20with%20TI%20imaging.'
    )
    db_session.add(heart_stats)

    # commit all and close session
    db_session.commit()
    db_session.close()

    # diabetes advice
    diabetes_stats = DiabetesStats(
        average_pregnancies='Some people develop diabetes during pregnancy that goes away after they have the baby. This type of diabetes is called gestational diabetes. However, having gestational diabetes increases your risk of getting type 2 diabetes later in life. Physical activity may help lower your blood glucose, blood pressure, and cholesterol. Try for at least 150 minutes of moderate-intensity physical activity, such as brisk walking, each week.',
        average_glucose='A range of 100-125 mg/dL falls under the category of prediabetes, while a blood sugar of 126 mg/dL or higher is considered type 2 diabetes. Quitting smoking, exercising, losing weight, getting better sleep, reducing stress and eating a healthy diet that incorporates fiber-rich fruits, vegetables and whole grains can treat prediabetes.',
        average_blood_pressure='High blood pressure is twice as likely to strike a person with diabetes than a person without diabetes. Left untreated, high blood pressure can lead to heart disease and stroke. To prevent high blood pressure: reduce your salt intake, engage in stress-relieving activities, exercise regularly, get to and stay at a healthy weight, avoid alcohol and smoking.',
        average_skin_thickness='Diabetes mellitus is a common and debilitating disease that affects a variety of organs including the skin. Between thirty and seventy percent of patients with diabetes mellitus will present with a cutaneous complication of diabetes mellitus at some point during their lifetime. Such skin changes can offer insight into patients’ glycemic control and may be the first sign of metabolic derangement in undiagnosed patients with diabetes.',
        average_insulin='Insulin is a hormone that plays a critical role in regulating blood glucose levels by facilitating its absorption. Sustained high glucose levels often indicate that your body is struggling to effectively utilize insulin, which can suggest insulin resistance. Certain foods cause a spike in glucose levels and you should limit them in your diet. Light physical activity, like walking, helps in maintaining more stable glucose levels.',
        average_bmi='BMI is a numerical value of your weight in relation to your height. A BMI between 18.5 and 25 kg/m² indicates a normal weight. A BMI between 25 kg/m² and 29.9 kg/m² is considered overweight. A BMI of 30 kg/m² or higher is considered obese. Lifestyle changes that help you maintain a 3% to 5% weight loss are likely to result in clinically meaningful improvements in blood glucose and lower your risk of developing Type 2 diabetes.',
        average_diabetes_pedigree_function='',
        average_age='The onset of diabetes is most common in people ages 45 to 64. Ways to reduce the risk of developing type 2 diabetes include: doing light-to-moderate exercise for at least 150 minutes per week, cutting down on the consumption of simple sugars, excess sugars, and fats, and eating smaller meals throughout the day rather than three large meals.'
    )
    db_session.add(diabetes_stats)

    # stroke advice
    stroke_stats = StrokeStats(
        average_gender = 'Women face a disproportionate burden of stroke mortality and disability. They have substantial differences in the strength of association of stroke risk factors, as well as female-specific risk factors. In the United States, the lifetime risk of stroke is higher in women (20%–21%) than in men (14%–17%), for a 55-year-old individual.',
        average_age='Of 795,000 strokes occurring annually in the United States, 87 percent are classified as ischemic (brain) strokes. Aging is the most robust non-modifiable risk factor for incident stroke, which doubles every 10 years after age 55 years. Approximately three-quarters of all strokes occur in persons aged ≥65 years.',
        average_hypertension='High blood pressure damages arteries throughout the body. It creates conditions that can make arteries burst or clog easily. Weakened or blocked arteries in the brain create a much higher risk for stroke. You can reduce your risk for stroke by managing your high blood pressure.',
        average_heart_disease='People with cardiac disease have 2–4 times greater risk of stroke than the general population. Older females and younger patients with multiple cardiac conditions are at an elevated risk. Choosing healthy food and drinks and keeping a healthy weight can help prevent heart disease.',
        average_ever_married='The risk of dying after stroke is significantly higher for those who were never married, remarried, divorced, or widowed than for those who had been continuously married. Another study went further to show that high quality marriages increased the length of survival after stroke more than simply being married.',
        average_work_type='There is sufficient evidence for the relationship between increased risk of stroke and job stress, working in extreme temperatures, long working hours, and/or shift work. When working long hours, job stress and sedentary lifestyle increase, which are risk factors for cerebral infarction. Effective communication, building a strong support network, and establishing work-life boundaries are also crucial for managing workplace stress.',
        average_residence_type='An overall a higher stroke incidence in rural areas appears to be a contributor to the higher rural stroke mortality, with this higher incidence potentially associated with a higher prevalence of stroke risk factors in rural areas. To the extent that disparities in case fatality do exist, there are many studies showing rural-urban disparities in stroke care could be contributing.',
        average_avg_glucose_level='Elevated blood glucose is common in the early phase of stroke. The prevalence of hyperglycemia, defined as blood glucose level >6.0 mmol/L (108 mg/dL), has been observed in two thirds of all ischemic stroke subtypes. Adhering to good general stroke management, including control of blood glucose, normalization of body temperature, fluid balance and hemodynamics increase favorable outcomes.',
        average_bmi='The risk of stroke was positively correlated with BMI, and the association was stronger in male and ischemic stroke. Lowering BMI can be used as a way to prevent stroke, and for people who are overweight or obese, lowering body weight can reduce the risk of stroke. ',
        average_smoking_status='Smoking tobacco increases your risk of having a stroke. Someone who smokes 20 cigarettes a day is six times more likely to have a stroke compared to a non-smoker. If you are a smoker, quitting will reduce your risk of stroke and a range of other diseases. If you live with a non-smoker, quitting will reduce their stroke risk too.'
    )
    db_session.add(stroke_stats)

    # heart disease advice
    heart_stats = HeartDiseaseStats(
        average_age='The aging and elderly population are particularly susceptible to cardiovascular disease. Age is an independent risk factor for cardiovascular disease (CVD) in adults, but these risks are compounded by additional factors, including frailty, obesity, and diabetes.',
        average_sex='Sex is another potential risk factor in aging adults, given that older females are reported to be at a greater risk for CVD than age-matched men. However, in both men and women, the risks associated with CVD increase with age, and these correspond to an overall decline in sex hormones, primarily of estrogen and testosterone. ',
        average_chest_pain_type='Chest pain is pain or discomfort in the area between the neck and belly. Chest pain may be sharp or dull. It might come and go, or you might always feel the pain. Chest pain is often related to heart disease. Chest pain symptoms due to a heart attack or another heart condition. If you have new or unexplained chest pain, call 911 or emergency medical help right away.',
        average_resting_bp='For the average person who is not at high risk for hypertension, we aim for a total blood pressure of 120/80 or lower. If your blood pressure is higher than 120/80, you could be at risk for heart disease. Being obese, drinking too much alcohol, eating an unhealthy diet (too much salt, not enough potassium), getting too little exercise increase the risk of hypertension. If you are overweight, losing weight reduces blood pressure.',   
        average_cholesterol='With high cholesterol, fats and other substances can build up in arteries. This buildup is called plaque. Sometimes a piece of plaque can break loose and form a blood clot, which may cause a heart attack or stroke. Risk factors for high cholesterol include eating habits, obesity, lack of exercise, smoking, and alcohol. Eat a diet that focuses on lean protein, fruits, vegetables and whole grains. Also limit the amount of saturated and trans fats you eat.',
        average_fasting_bs='Over time, high blood sugar can damage blood vessels and the nerves that control your heart. Follow a healthy diet by eating more fresh fruits and vegetables, lean protein, and whole grains. Cut out any processed foods and be physically active to keep your weight in check.',
        average_ecg='An electrocardiogram is a quick test to check the heartbeat. It records the electrical signals in the heart. Test results can help diagnose heart attacks and irregular heartbeats, called arrhythmias. You may need an ECG if you have: chest pain, dizziness, lightheadedness or confusion, skipping or fluttering heartbeat, shortness of breath, or reduced ability to exercise.',
        average_max_hr='Max heart rate is when your heart is working its hardest to meet your oxygen needs. A high aerobic capacity is associated with a lower risk of heart attack and death. A commonly used formula to determine your maximum heart rate is 220 minus your age in years. Vigorous exercise is the best way to both lower your resting heart rate and increase your maximum heart rate and aerobic capacity.',
        average_exercise_angina='Angina is pain in the chest that comes on with exercise, stress, or other things that make the heart work harder. It is an extremely common symptom of coronary artery disease, which is caused by cholesterol-clogged coronary arteries. Lifestyles changes to reduce angina include stopping smoking, losing weight, and lowering high blood pressure. If certain kinds of activity regularly cause angina, try performing the activity more slowly.',
        average_oldpeak='',
        average_st_slope='The ST/heart rate slope, is a more accurate ECG criterion for diagnosing significant coronary artery disease. A flat or downward-sloping ST segment on an ECG, especially during exercise testing, is a strong indicator of coronary artery disease (CAD).'
    )
    db_session.add(heart_stats)

    # commit all and close session
    db_session.commit()
    db_session.close()